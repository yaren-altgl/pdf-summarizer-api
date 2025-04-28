from logger import logger

from language_utils import detect_language
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai

from pdf_utils import extract_text_from_pdf
from summarizer import summarize_text

from response_models import SummaryResponse

from error_handlers import (
    invalid_file_type,
    insufficient_text,
    language_detection_error,
    summarization_error,
    unknown_error,
)

# FastAPI uygulamasını başlat
app = FastAPI()

# Ortam bilgisini .env'den al
load_dotenv()
env = os.getenv("ENV", "dev")  # varsayılan olarak 'dev'

# CORS ayarları
if env == "dev":
    origins = ["*"]
else:
    origins = [
        "https://benimsitem.com",
        "https://portfolio-sitesi.com"
    ]

# CORS middleware'i ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API yapılandırması
genai.configure(api_key=os.getenv("keyim"))
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# Ana sayfa
@app.get("/")
def root():
    return {"message": "PDF Auto-Summarizer API is running!"}

# PDF yükleme ve özetleme endpoint'i
@app.post("/upload-pdf/", response_model=SummaryResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    summary_language: str = Form("auto")
):
    logger.info(f"Yeni istek alındı. Dosya: {file.filename}, Dil tercihi: {summary_language}")

    if file.content_type != "application/pdf":
        logger.warning("Geçersiz dosya türü.")
        raise invalid_file_type()
    
    valid_langs = ["en", "tr"]
    if summary_language != "auto" and summary_language not in valid_langs:
        logger.warning(f"Geçersiz dil kodu: {summary_language}")
        raise HTTPException(status_code=400, detail="Unsupported summary language.")
    
    try:
        text = extract_text_from_pdf(file.file)
        logger.info("PDF'ten metin çıkarıldı.")

        if not text or len(text.strip()) < 20:
            logger.warning("PDF'den çıkarılan metin yetersiz.")
            raise insufficient_text()

        try:
            detected_lang = detect_language(text)
            logger.info(f"Tespit edilen dil: {detected_lang}")
        except Exception:
            logger.exception("Dil tespiti sırasında hata oluştu.")
            raise language_detection_error()

        final_lang = detected_lang if summary_language == "auto" else summary_language
        logger.info(f"Kullanılacak özet dili: {final_lang}")

        try:
            summary = summarize_text(text, model, final_lang)
            logger.success("Özet oluşturuldu.")
        except Exception:
            logger.exception("Özetleme işlemi sırasında hata oluştu.")
            raise summarization_error()

        return {
            "summary": summary,
            "detected_language": detected_lang,
            "used_language": final_lang
        }

    except Exception as e:
        logger.exception("Bilinmeyen bir sunucu hatası.")
        raise unknown_error(e)
