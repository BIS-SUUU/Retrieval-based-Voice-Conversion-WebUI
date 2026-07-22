
<div align="center">

<h1>Retrieval-based-Voice-Conversion-WebUI</h1>
إطار عمل بسيط وسهل الاستخدام لتحويل جرس الصوت / تغيير الصوت.<br><br>

[![صنع بحب](https://img.shields.io/badge/صُنِعَ_بـ-%E2%9D%A4-red?style=for-the-badge&labelColor=orange
)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

<img src="https://counter.seku.su/cmoe?name=rvc&theme=r34" /><br>

[![الرخصة](https://img.shields.io/github/license/RVC-Project/Retrieval-based-Voice-Conversion-WebUI?style=for-the-badge)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE)
[![Huggingface](https://img.shields.io/badge/🤗%20-النماذج-yellow.svg?style=for-the-badge)](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/)

[**سجل التغييرات**](./Changelog_AR.md) | [**الأسئلة الشائعة (FAQ)**](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/wiki/FAQ-(Frequently-Asked-Questions))

[**English**](../en/README.en.md) | [**中文简体**](../../README.md) | [**日本語**](../jp/README.ja.md) | [**한국어**](../kr/README.ko.md) ([**韓國語**](../kr/README.ko.han.md)) | [**Français**](../fr/README.fr.md) | [**Türkçe**](../tr/README.tr.md) | [**Português**](../pt/README.pt.md) | [**العربية**](./README.ar.md)

</div>

> شاهد [فيديو العرض التوضيحي](https://www.bilibili.com/video/BV1pm4y1z7Gm/) هنا!

<table>
   <tr>
		<td align="center">واجهة الويب للتدريب والاستدلال</td>
		<td align="center">واجهة تغيير الصوت الفورية</td>
	</tr>
  <tr>
		<td align="center"><img src="https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/assets/129054828/092e5c12-0d49-4168-a590-0b0ef6a4f630"></td>
    <td align="center"><img src="https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/assets/129054828/730b4114-8805-44a1-ab1a-04668f3c30a6"></td>
	</tr>
	<tr>
		<td align="center">go-webui.bat</td>
		<td align="center">go-realtime_gui.bat</td>
	</tr>
  <tr>
    <td align="center">يمكنك اختيار الإجراء الذي تريد تنفيذه بحرية.</td>
		<td align="center">لقد حققنا زمن استجابة من طرف إلى طرف يبلغ 170 مللي ثانية. مع استخدام أجهزة الإدخال والإخراج ASIO، تمكنا من تحقيق زمن استجابة 90 مللي ثانية، لكن ذلك يعتمد بشكل كبير على دعم برامج تشغيل الأجهزة.</td>
	</tr>
</table>

> تستخدم مجموعة بيانات النموذج المدرب مسبقاً ما يقرب 50 ساعة من الصوت عالي الجودة من مجموعة بيانات VCTK مفتوحة المصدر.

> ستُضاف مجموعات بيانات الأغاني المرخصة عالية الجودة إلى مجموعة التدريب بشكل متكرر لاستخدامك، دون القلق بشأن انتهاك حقوق النشر.

> ترقبوا النموذج الأساسي المدرب مسبقاً لـ RVCv3، الذي يتمتع بمعاملات أكبر، وبيانات تدريب أكثر، ونتائج أفضل، وسرعة استدلال دون تغيير، ويتطلب بيانات تدريب أقل للتدريب.

## الميزات
+ تقليل تسرب النغمة عن طريق استبدال الخصائص المصدر بخصائص مجموعة التدريب باستخدام استرجاع top1.
+ تدريب سهل وسريع، حتى على بطاقات الرسوميات الضعيفة.
+ التدريب بكميات صغيرة من البيانات (يوصى بـ 10 دقائق على الأقل من الكلام منخفض الضوضاء).
+ دمج النماذج لتغيير الجرس (باستخدام علامة تبويب معالجة ckpt ← دمج ckpt).
+ واجهة ويب سهلة الاستخدام.
+ نموذج UVR5 لفصل الغناء عن الآلات الموسيقية بسرعة.
+ خوارزمية استخراج النغمة عالية الدقة [InterSpeech2023-RMVPE](#الإشادات) لمنع مشكلة كتم الصوت. تقدم أفضل النتائج (بشكل ملحوظ) وهي أسرع مع استهلاك موارد أقل من Crepe_full.
+ تستخدم أنظمة AMD/Intel مجموعة تبعيات CPU؛ يمكن لـ Windows استخدام DirectML بينما يستخدم Linux وحدة المعالجة المركزية.

## إعداد البيئة

هذا الفرع يستهدف **Python 3.12 x64**. نفذ كل أمر من جذر المستودع. يُوصى باستخدام Ubuntu 24.04 x86_64.

### Ubuntu 24.04

sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev ffmpeg unzip libsndfile1 libportaudio2

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

### Windows

ثبّت Python 3.12 x64، ثم أنشئ بيئة افتراضية:

py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel


### اختر التبعيات حسب الأجهزة

| الجهاز | طريقة التثبيت |
| --- | --- |
| CPU، AMD، Intel | استخدم `requirments_cpu_py312.txt`؛ يمكن لـ Windows استخدام DirectML، بينما يستخدم Linux CPU |
| سلسلة NVIDIA RTX 50 | ثبّت زوج Torch الخاص بـ CUDA 12.8 أولاً، ثم `requirments_cu128_py312.txt` |
| بطاقات NVIDIA قبل سلسلة RTX 50 | ثبّت زوج Torch الخاص بـ CUDA 11.8 أولاً، ثم `requirments_cu118_py312.txt` |

#### CPU، AMD، Intel

python -m pip install -r requirments_cpu_py312.txt

#### سلسلة NVIDIA RTX 50: على مرحلتين

python -m pip install torch==2.7.1+cu128 torchaudio==2.7.1+cu128 \
  --index-url https://download.pytorch.org/whl/cu128 \
  --extra-index-url https://pypi.org/simple
python -m pip install -r requirments_cu128_py312.txt


#### بطاقات NVIDIA قبل سلسلة RTX 50: على مرحلتين

python -m pip install torch==2.7.1+cu118 torchaudio==2.7.1+cu118 \
  --index-url https://download.pytorch.org/whl/cu118 \
  --extra-index-url https://pypi.org/simple
python -m pip install -r requirments_cu118_py312.txt


تحقق من تثبيت Torch و CUDA:

python -c "import torch; print('torch:', torch.__version__); print('cuda:', torch.version.cuda); print('cuda available:', torch.cuda.is_available())"


### فهارس الحزم

تحدد ملفات `requirments_*.txt` الثلاثة فهارس الحزم الخاصة بها في الأعلى. احتفظ بالمرايا الافتراضية في الصين القارية. لاستخدام الفهارس الرسمية، استبدل فقط `--index-url` و `--extra-index-url`؛ واحتفظ بإصدارات الحزم، ولواحق CUDA، وترتيب المرحلتين دون تغيير.

| المرآة الافتراضية | المصدر الرسمي |
| --- | --- |
| `https://mirrors.pku.edu.cn/pypi/simple` | `https://pypi.org/simple` |
| `https://mirrors.nju.edu.cn/pytorch/whl/cpu` | `https://download.pytorch.org/whl/cpu` |
| `https://mirrors.nju.edu.cn/pytorch/whl/cu118` | `https://download.pytorch.org/whl/cu118` |
| `https://mirrors.nju.edu.cn/pytorch/whl/cu128` | `https://download.pytorch.org/whl/cu128` |

## النماذج والأدلة الزمنية

تنشئ واجهة الويب الأدلة الزمنية تلقائياً. حمّل النماذج من [مستودع نماذج Hugging Face](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main) واحتفظ بهذا الهيكل:

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

# المسارات الدقيقة التي يستخدمها الكود
assets/hubert_base/config.json
assets/hubert_base/preprocessor_config.json
assets/hubert_base/pytorch_model.bin
assets/rmvpe/rmvpe.pt
assets/pretrained/*.pth
assets/pretrained_v2/*.pth
assets/uvr5_weights/*
assets/weights/*.pth
assets/indices/*.index
logs/mute/*


### تنزيل النماذج

python -m pip install --upgrade huggingface_hub

# مطلوب للاستدلال واستخراج الخصائص
hf download lj1995/VoiceConversionWebUI --revision main \
  --include "hubert_base/*" --local-dir assets
hf download lj1995/VoiceConversionWebUI rmvpe.pt --revision main \
  --local-dir assets/rmvpe

# مطلوب لتدريب v1/v2
hf download lj1995/VoiceConversionWebUI --revision main \
  --include "pretrained/*" "pretrained_v2/*" --local-dir assets
hf download lj1995/VoiceConversionWebUI mute.zip --revision main \
  --local-dir .model-downloads
python -m zipfile -e .model-downloads/mute.zip logs

# مطلوب فقط لفصل الغناء UVR5
hf download lj1995/VoiceConversionWebUI --revision main \
  --include "uvr5_weights/*" --local-dir assets

بيئات Windows AMD/Intel DirectML تحتاج أيضاً إلى:

hf download lj1995/VoiceConversionWebUI rmvpe.onnx --revision main \
  --local-dir assets/rmvpe

### FFmpeg

أمر إعداد Ubuntu أعلاه يثبّت FFmpeg. على Windows، ضع هذه الملفات في جذر المستودع:

- [ffmpeg.exe](https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/ffmpeg.exe?download=true)
- [ffprobe.exe](https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/ffprobe.exe?download=true)

## تشغيل واجهة الويب

python webui.py


لخادم Ubuntu بدون واجهة رسومية:

python webui.py --noautoopen


المنفذ الافتراضي هو `7865`. ضع نماذج `.pth` الشخصية في `assets/weights/` وملفات `.index` في `assets/indices/`.

## الإشادات
+ [ContentVec](https://github.com/auspicious3000/contentvec/)
+ [VITS](https://github.com/jaywalnut310/vits)
+ [HIFIGAN](https://github.com/jik876/hifi-gan)
+ [Gradio](https://github.com/gradio-app/gradio)
+ [FFmpeg](https://github.com/FFmpeg/FFmpeg)
+ [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)
+ [audio-slicer](https://github.com/openvpi/audio-slicer)
+ [استخراج النغمة الصوتية: RMVPE](https://github.com/Dream-High/RMVPE)
  + النموذج المدرب مسبقاً تم تدريبه واختباره بواسطة [yxlllc](https://github.com/yxlllc/RMVPE) و [RVC-Boss](https://github.com/RVC-Boss).

## شكر لكل المساهمين على جهودهم
<a href="https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=RVC-Project/Retrieval-based-Voice-Conversion-WebUI" />
</a>

