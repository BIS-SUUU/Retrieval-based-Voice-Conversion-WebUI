    def _load_user_config(self):
        """تحميل config.json: أولاً من جذر المشروع، ثم من داخل مجلد configs كخطة احتياط.
        هذه الدالة تحاول قراءة ملف config.json من جذر الريبو (مناسب عندما يكون الملف في root)
        وإذا لم تجده فستم تجرب الموقع داخل مجلد configs (CONFIGS_DIR/config.json).
        تعود بقيم افتراضية إن لم يوجد الملف في أي موقع.
        """
        repo_root_path = Path(__file__).resolve().parent.parent / "config.json"
        local_configs_path = CONFIGS_DIR / "config.json"

        for p in (repo_root_path, local_configs_path):
            try:
                if p.exists():
                    with open(p, "r", encoding="utf-8") as f:
                        return json.load(f)
            except Exception as e:
                logger.warning(f" Failed to read {p}: {e}")

        logger.warning("config.json not found in repo root or configs/, using defaults (v3/48k)")
        return {"model_version": "v3", "sample_rate": 48000}
