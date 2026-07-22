<div dir="rtl" lang="ar">

# نصائح ضبط FAISS

## نظرة عامة سريعة
FAISS هي مكتبة فعّالة للبحث عن الجيران الأقرب (approximate nearest neighbors) للمتجهات الكثيفة، وتُستخدم في RVC للبحث عن تضمينات HuBERT المشابهة.

## أين توجد البيانات؟
المسارات المهمة:
```
logs/<experiment>/3_feature256/    # ملفات npy لخصائص 256-d
logs/<experiment>/total_fea.npy    # ملف الخصائص المجمّع
```

## مثال مبسّط لإنشاء فهرس
```python
import faiss
import numpy as np

big_npy = np.load("logs/your-experiment/total_fea.npy")
N, dim = big_npy.shape
n_ivf = int(4 * np.sqrt(N))
index = faiss.index_factory(dim, f"IVF{n_ivf},PQ{dim//2}x4fs,RFlat")
index.train(big_npy)
index.add(big_npy)
faiss.write_index(index, "logs/your-experiment/trained_index.index")
```

## توصيات المعاملات
- n_ivf: بين `4*sqrt(N)` و `16*sqrt(N)` حسب حجم البيانات.
- n_probe (أثناء البحث): استخدم `1` للاستدلال الفوري و `4`–`8` لزيادة الدقة.
- PQ: استخدم `PQ128x4fs` لمتجهات 256-d إن كانت الذاكرة محدودة.

## نصائح عملية
1. إذا كانت بياناتك أقل من 10k متجه، قد يكون `Flat` أسرع وأسهل من IVF.
2. للاستدلال الفوري (Real-time) اختر `n_probe = 1` لتقليل زمن الاستجابة.
3. إذا واجهت أخطاء ذاكرة، جرّب تقليل `n_ivf` أو استخدام PQ أصغر (مثل `PQ64x4fs`).

## أدوات ومراجع
- دليل Index Factory: https://github.com/facebookresearch/faiss/wiki/The-index-factory
- شرح FastScan وRFlat في توثيق FAISS.

</div>
