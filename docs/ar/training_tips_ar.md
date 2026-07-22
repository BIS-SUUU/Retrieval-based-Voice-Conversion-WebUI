<div dir="rtl" lang="ar">

# نصائح وإرشادات لتدريب RVC (النسخة العربية)

## سير عمل التدريب (مفصّل)
1. إعداد اسم التجربة وتحديد خيارات النغمة (pitch) إن رغبت.
2. معالجة البيانات:
   - تقسيم الملفات الطويلة، وإزالة الصمت، وتحويلها إلى 16k/32k/48k حسب الاختيار.
   - حفظ النواتج في:
     - `logs/<exp>/0_gt_wavs`
     - `logs/<exp>/1_16k_wavs`
     - `logs/<exp>/2a_f0` و `logs/<exp>/2b_f0nsf`
     - `logs/<exp>/3_feature256`
3. تدريب النموذج:
   - ضبط `batch_size` بحسب ذاكرة GPU.
   - عند مواجهة `CUDA out of memory` خفّض `batch_size` أو استخدم نموذجًا بمعدل عينة أقل.

## إعداد بيئة سريعة (Ubuntu مثال)
```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev ffmpeg unzip libsndfile1 libportaudio2
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirments_cpu_py312.txt
```

## نصائح لتحسين جودة التدريب
- استخدم بيانات نظيفة وخالية من الضوضاء كلما أمكن.
- تأكد من تنوع النغمات في مجموعة التدريب.
- ابدأ بحجم دفعة متوسط ثم زد عندما تتوافر ذاكرة.
- استخدم الإعدادات المسبقة المناسبة لمعدل العينة (configs/v3/*k.json).

## أخطاء شائعة وحلولها
- `RuntimeError: CUDA out of memory` → خفّض `batch_size` أو استخدم 32k.
- `Expecting value: line 1 column 1 (char 0)` → تحقق من ملفات JSON أو تعطيل Proxy.
- mismatch في حجم التنسور → لا تغيّر معدل العينة واستأنف التدريب بنفس اسم التجربة.

## ملاحظات
- لا تنسَ استخراج نموذج صغير (export) للمشاركة بدلًا من نشر ملف checkpoint كبير.

</div>
