from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # daha tutarlı sonuçlar için

def detect_language(text: str) -> str:
    try:
        lang_code = detect(text)
        return lang_code
    except:
        return "unknown"
