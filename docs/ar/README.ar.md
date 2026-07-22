<div dir="rtl" lang="ar">

<!-- تم تنسيق هذا الملف لعرض من اليمين إلى اليسار وتحسين التنسيق العربي -->

# README (النسخة العربية)

Retrieval-based-Voice-Conversion-WebUI - إطار عمل بسيط وسهل الاستخدام لتحويل جرس الصوت / تغيير الصوت.

<div align="center">

[![صنع بحب](https://img.shields.io/badge/صُنِعَ_بـ-%E2%9D%A4-red?style=for-the-badge&labelColor=orange)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

<img src="https://counter.seku.su/cmoe?name=rvc&theme=r34" />

[![الرخصة](https://img.shields.io/github/license/RVC-Project/Retrieval-based-Voice-Conversion-WebUI?style=for-the-badge)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE)
[![Huggingface](https://img.shields.io/badge/🤗%20-النماذج-yellow.svg?style=for-the-badge)](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/)

</div>

## روابط سريعة
- [سجل التغييرات](./Changelog_AR.md)
- [الأسئلة الشائعة (FAQ)](./faq_ar.md)
- [الوثائق الإنجليزية](../en/README.en.md)

---

## الميزات
- تقليل تسرب النغمة عن طريق استبدال الخصائص المصدر بخصائص مجموعة التدريب باستخدام استرجاع top1.
- تدريب سهل وسريع، حتى على بطاقات الرسوميات الضعيفة.
- التدريب بكميات صغيرة من البيانات (يوصى بـ 10 دقائق على الأقل من الكلام منخفض الضوضاء).
- دمج النماذج لتغيير الجرس (باستخدام علامة تبويب معالجة ckpt ← دمج ckpt).
- واجهة ويب سهلة الاستخدام.
- نموذج UVR5 لفصل الغناء عن الآلات الموسيقية بسرعة.
- خوارزمية استخراج النغمة عالية الدقة RMVPE لمنع مشكلة كتم الصوت.

---

## إعداد البيئة
هذا الفرع يستهدف **Python 3.12 x64**. يُنَفّذ كل أمر من جذر المستودع. يوصى باستخدام Ubuntu 24.04 x86_64.

### Ubuntu 24.04
```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev ffmpeg unzip libsndfile1 libportaudio2
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

### Windows
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
```

### تثبيت التبعيات حسب الأجهزة
| الجهاز | طريقة التثبيت |
| --- | --- |
| CPU، AMD، Intel | استخدم `requirments_cpu_py312.txt`؛ يمكن لـ Windows استخدام DirectML، بينما يستخدم Linux CPU |
| سلسلة NVIDIA RTX 50 | ثبّت زوج Torch الخاص بـ CUDA 12.8 أولاً، ثم `requirments_cu128_py312.txt` |
| بطاقات NVIDIA قبل سلسلة RTX 50 | ثبّت زوج Torch الخاص بـ CUDA 11.8 أولاً، ثم `requirments_cu118_py312.txt` |

مثال (CPU):
```bash
python -m pip install -r requirments_cpu_py312.txt
```

---

## النماذج والأصول
هيكل المجلدات المتوقع:
```
assets/
├── hubert_base/
│   ├── config.json
│   ├── preprocessor_config.json
│   └── pytorch_model.bin
├── rmvpe/rmvpe.pt
├── pretrained/
├── pretrained_v2/
├── uvr5_weights/
├── weights/        # نماذج RVC .pth الخاصة بالمستخدم
└── indices/        # ملفات .index الخاصة بالمستخدم
logs/
└── mute/           # عينات تدريب الصمت
```

### تنزيل النماذج
```bash
python -m pip install --upgrade huggingface_hub
hf download lj1995/VoiceConversionWebUI --revision main --include "hubert_base/*" --local-dir assets
hf download lj1995/VoiceConversionWebUI rmvpe.pt --revision main --local-dir assets/rmvpe
```

---

## تشغيل واجهة الويب
```bash
python webui.py
# لخادم بدون واجهة:
python webui.py --noautoopen
```

المنفذ الافتراضي هو `7865`.

---

إذا رغبت، أستطيع الآن تنسيق باقي الملفات العربية (سجل التغييرات، FAQ، faiss_tips، training_tips) بشكل احترافي أكثر وإضافة توجيهات اتجاه النص (RTL) وإصلاح الروابط.

</div>
