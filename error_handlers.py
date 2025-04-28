# error_handlers.py

from fastapi import HTTPException

def invalid_file_type():
    raise HTTPException(status_code=400, detail="Lütfen geçerli bir PDF dosyası yükleyin.")

def insufficient_text():
    raise HTTPException(status_code=422, detail="PDF'den yeterli metin çıkarılamadı.")

def language_detection_error():
    raise HTTPException(status_code=500, detail="Dil tespiti sırasında bir hata oluştu.")

def summarization_error():
    raise HTTPException(status_code=502, detail="Özetleme işlemi sırasında bir hata oluştu.")

def unknown_error(e):
    raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")
