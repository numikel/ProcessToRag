from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

class TranslationTool:
    LANGUAGES_MAP = {
        "bg": "bul_Cyrl", "hr": "hrv_Latn", "cs": "ces_Latn", "da": "dan_Latn",
        "nl": "nld_Latn", "en": "eng_Latn", "et": "est_Latn", "fi": "fin_Latn",
        "fr": "fra_Latn", "de": "deu_Latn", "el": "ell_Grek", "hu": "hun_Latn",
        "ga": "gle_Latn", "it": "ita_Latn", "lv": "lav_Latn", "lt": "lit_Latn",
        "mt": "mlt_Latn", "pl": "pol_Latn", "pt": "por_Latn", "ro": "ron_Latn",
        "sk": "slk_Latn", "sl": "slv_Latn", "es": "spa_Latn", "sv": "swe_Latn",
        "zh": "zho_Hans", "ja": "jpn_Jpan", "ru": "rus_Cyrl", "ko": "kor_Hang",
        "ar": "arb_Arab"
    }

    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def translate_to_english(self, text: str):
        if not text:
            return None

        src_lang = self._detect_source_lang(text)
        if src_lang == "eng_Latn":
            return text

        translator = pipeline(
            "translation",
            model=self.model,
            tokenizer=self.tokenizer,
            src_lang=src_lang,
            tgt_lang="eng_Latn"
        )
        result = translator(text, max_length=1024)
        return result[0]['translation_text']

    def _detect_source_lang(self, text: str):
        try:
            lang = detect(text)
            return self.LANGUAGES_MAP.get(lang, "eng_Latn")
        except LangDetectException:
            return "eng_Latn"
