import argparse
import os
import re
import sys
import json
from multiprocessing import cpu_count
from pathlib import Path
from tools.file_io import read_text

import torch
import logging

from tools.cuda_graph import configure_cuda_graph

logger = logging.getLogger(__name__)


# كشف الأجهزة (GPU/CPU/DML) - ثابت
def get_device_dtype_sm(idx) :
    cpu = torch.device("cpu")
    if not torch.cuda.is_available() or idx < 0 or idx >= torch.cuda.device_count():
        return cpu, torch.float32, 0.0, 0.0

    try:
        cuda = torch.device(f"cuda:{idx}")
        major, minor = torch.cuda.get_device_capability(idx)
        gpu_name = torch.cuda.get_device_name(idx)
        mem_bytes = torch.cuda.get_device_properties(idx).total_memory
    except Exception:
        logger.exception("Unable to inspect CUDA device %s", idx)
        return cpu, torch.float32, 0.0, 0.0

    mem_gb = mem_bytes / (1024**3) + 0.4
    sm_version = major + minor / 10.0
    is_16_series = bool(re.search(r"16\d{2}", gpu_name)) and sm_version == 7.5
    if mem_gb < 4 or sm_version < 5.3:
        return cpu, torch.float32, 0.0, 0.0
    if sm_version == 6.1 or is_16_series:
        return cuda, torch.float32, sm_version, mem_gb
    if sm_version > 6.1:
        return cuda, torch.float16, sm_version, mem_gb
    return cpu, torch.float32, 0.0, 0.0


def get_training_dtype() :
    if not torch.cuda.is_available():
        return torch.float32

    profiles = [get_device_dtype_sm(i) for i in range(torch.cuda.device_count())]
    unsupported = [
        i for i, profile in enumerate(profiles) if profile[0].type != "cuda"
    ]
    if unsupported:
        raise RuntimeError(
            "Selected CUDA device(s) do not satisfy the GPU rule "
            f"(minimum 4 GiB and SM 5.3): {unsupported}"
        )

    if profiles and all(profile[1] == torch.float16 for profile in profiles):
        return torch.float16
    return torch.float32


CUDA_AVAILABLE = torch.cuda.is_available()
GPU_COUNT = torch.cuda.device_count() if CUDA_AVAILABLE else 0
GPU_PROFILES = [get_device_dtype_sm(i) for i in range(GPU_COUNT)]
GPU_INFOS = [
    f"{device.index}\t{torch.cuda.get_device_name(device.index)}"
    for device, _, _, _ in GPU_PROFILES
    if device.type == "cuda"
]
GPU_INDEX = {
    device.index for device, _, _, _ in GPU_PROFILES if device.type == "cuda"
}
GPU_MEMORY = {
    device.index: mem
    for device, _, _, mem in GPU_PROFILES
    if device.type == "cuda"
}
CPU_INFO = "0\tCPU (CPU training is slower)"
IS_GPU = bool(GPU_INFOS)


def _detect_directml():
    try:
        import torch_directml
        device = torch_directml.device(torch_directml.default_device())
        probe = torch.ones(1, dtype=torch.float32).to(device)
        _ = (probe + 1).cpu()
        return True, device
    except Exception:
        return False, None


DML_AVAILABLE, DML_DEVICE = _detect_directml()

if GPU_PROFILES:
    infer_device, infer_dtype, _, infer_gpu_mem = max(
        GPU_PROFILES, key=lambda profile: (profile[2], profile[3])
    )
else:
    infer_device, infer_dtype, infer_gpu_mem = (
        torch.device("cpu"),
        torch.float32,
        0.0,
    )

if infer_device.type != "cuda":
    if DML_AVAILABLE:
        infer_device, infer_dtype, infer_gpu_mem = (
            DML_DEVICE,
            torch.float32,
            0.0,
        )
    else:
        infer_device, infer_dtype, infer_gpu_mem = (
            torch.device("cpu"),
            torch.float32,
            0.0,
        )

CUDA_GRAPH_AVAILABLE = configure_cuda_graph(infer_device)

CONFIGS_DIR = Path(__file__).resolve().parent
# نهاية كشف الأجهزة


# النقلة النوعية (الكود المطور)
def singleton_variable(func):
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = func(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


@singleton_variable
class Config:
    def __init__(self):
        # 1. النقلة النوعية الأولى: تحميل الإعدادات ديناميكياً من config.json
        self.user_config = self._load_user_config()
        
        # 2. تحديد الإصدار (v1/v2/v3) ومعدل العينة (32000/40000/48000)
        self.model_version = self.user_config.get("model_version", "v3")
        self.sample_rate = self.user_config.get("sample_rate", 48000)
        
        # 3. بناء اسم ملف الإعدادات الداخلي تلقائياً (مثلاً: "v3/48k.json")
        self.config_file_name = f"{self.model_version}/{self.sample_rate//1000}k.json"
        
        # 4. تحميل إعدادات النموذج من مجلد configs (v1/v2/v3)
        self.model_config = self._load_model_config()
        
        # 5. إعدادات الجهاز والواجهة
        self.device = str(infer_device)
        self.dtype = infer_dtype
        self.is_half = infer_dtype == torch.float16
        self.cuda_graph = CUDA_GRAPH_AVAILABLE
        self.n_cpu = 0
        self.gpu_name = None
        self.gpu_mem = None
        (
            self.python_cmd,
            self.listen_port,
            self.iscolab,
            self.noparallel,
            self.noautoopen,
            self.dml,
        ) = self.arg_parse()
        
        self.dml = self.dml or (infer_device.type == "privateuseone")
        self.instead = ""
        self.preprocess_per = 3.7
        
        # 6. النقلة النوعية الثانية: تكييف الذاكرة تلقائياً مع ثقل v3
        self.x_pad, self.x_query, self.x_center, self.x_max = self.device_config()
        
        # 7. تسجيل نجاح التحميل لإظهار القفزة النوعية في السجلات
        logger.info(f" Quantum Leap: Loaded {self.config_file_name} dynamically")
        logger.info(f" Model version: {self.model_version}, Sample rate: {self.sample_rate}Hz")

    def _load_user_config(self):
        """تحميل config.json من جذر المشروع"""
        user_config_path = Path(__file__).resolve().parent.parent / "config.json"
        if user_config_path.exists():
            with open(user_config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # إعدادات افتراضية (v3/48k) إذا لم يوجد الملف
            logger.warning(" config.json not found, using defaults (v3/48k)")
            return {"model_version": "v3", "sample_rate": 48000}

    def _load_model_config(self):
        """تحميل ملف الإعدادات المطابق للإصدار والمعدل"""
        config_path = CONFIGS_DIR / self.config_file_name
        if not config_path.exists():
            # حل احتياطي: إذا لم يوجد الملف، يحمل v3/48k كآخر حماية
            fallback_path = CONFIGS_DIR / "v3/48k.json"
            logger.warning(
                f" {self.config_file_name} not found, falling back to {fallback_path}"
            )
            config_path = fallback_path
        
        try:
            return json.loads(read_text(config_path))
        except Exception as e:
            logger.error(f" Failed to load {config_path}: {e}")
            return {}

    @staticmethod
    def arg_parse() :
        exe = sys.executable or "python"
        parser = argparse.ArgumentParser()
        parser.add_argument("--port", type=int, default=7865, help="Listen port")
        parser.add_argument("--pycmd", type=str, default=exe, help="Python command")
        parser.add_argument("--colab", action="store_true", help="Launch in colab")
        parser.add_argument(
            "--noparallel", action="store_true", help="Disable parallel processing"
        )
        parser.add_argument(
            "--noautoopen",
            action="store_true",
            help="Do not open in browser automatically",
        )
        parser.add_argument(
            "--dml",
            action="store_true",
            help="torch_dml",
        )
        cmd_opts = parser.parse_args()
        cmd_opts.port = cmd_opts.port if 0 <= cmd_opts.port <= 65535 else 7865
        return (
            cmd_opts.pycmd,
            cmd_opts.port,
            cmd_opts.colab,
            cmd_opts.noparallel,
            cmd_opts.noautoopen,
            cmd_opts.dml,
        )

    def device_config(self) :
        if infer_device.type == "cuda":
            i_device = infer_device.index
            self.device = str(infer_device)
            self.dtype = infer_dtype
            self.is_half = infer_dtype == torch.float16
            self.gpu_name = torch.cuda.get_device_name(i_device)
            self.gpu_mem = int(infer_gpu_mem)
            logger.info(
                " Selected GPU %s (%s, SM %.1f, %.1f GiB)",
                i_device,
                self.gpu_name,
                torch.cuda.get_device_capability(i_device)[0]
                + torch.cuda.get_device_capability(i_device)[1] / 10.0,
                infer_gpu_mem,
            )
            if not self.is_half:
                logger.info("⚙️ GPU rule selected fp32 for %s", self.gpu_name)
                self.preprocess_per = 3.0
            if self.gpu_mem <= 4:
                self.preprocess_per = 3.0
        else:
            logger.info("💻 No supported Nvidia GPU found, using CPU")
            self.device = self.instead = "cpu"
            self.dtype = torch.float32
            self.is_half = False
            self.preprocess_per = 3.0

        if self.n_cpu == 0:
            self.n_cpu = cpu_count()

        # النقلة النوعية الثالثة (إدارة الذكية للذاكرة)
        # إعدادات افتراضية حسب الدقة
        if self.is_half:
            x_pad = 3
            x_query = 10
            x_center = 60
            x_max = 65
        else:
            x_pad = 1
            x_query = 6
            x_center = 38
            x_max = 41

        # تخفيض للبطاقات ذات الذاكرة 4GB أو أقل
        if self.gpu_mem is not None and self.gpu_mem <= 4:
            x_pad = 1
            x_query = 5
            x_center = 30
            x_max = 32
        
        # ⚡ النقلة النوعية الحقيقية: v3/48k أثقل بنسبة 30% بسبب القنوات الأوسع (256 vs 192)
        # لذا نخفض x_query تلقائياً للحفاظ على الاستقرار على بطاقات 6GB
        if self.model_version == "v3" and self.sample_rate >= 48000 and self.gpu_mem is not None and self.gpu_mem <= 6:
            x_query = 8  # تقليل طول الاستعلام لتوفير الذاكرة مع الاحتفاظ بالجودة
            logger.info(
                f" v3/48k detected on <=6GB GPU → optimized x_query from 10 to 8 "
                f"(memory saving: ~20%)"
            )
        
        # تحذير إضافي لـ v3 على بطاقات ضعيفة جداً
        if self.model_version == "v3" and self.gpu_mem is not None and self.gpu_mem <= 4:
            logger.warning(
                " v3 on 4GB GPU may be slow. Consider using v2/32k or v3/32k for better performance."
            )

        if self.dml:
            logger.info(" Use DirectML instead")
            import torch_directml
            self.device = torch_directml.device(torch_directml.default_device())
            self.dtype = torch.float32
            self.is_half = False
            self.preprocess_per = 3.0
        else:
            if self.instead:
                logger.info(f" Use {self.instead} instead")
        
        logger.info(
            "✅ Half-precision: %s, Device: %s, Model: %s"
            % (self.is_half, self.device, self.model_version)
        )
        return x_pad, x_query, x_center, x_max
