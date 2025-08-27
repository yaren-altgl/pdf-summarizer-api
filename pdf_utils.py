# pdf_utils.py
import os
import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    """
    PDF -> temiz düz metin.
    - file: dosya yolu (str) / path-like / UploadFile.file / file-like (read()'i olan obje)
    - .env içinde PDF_PAGE_LIMIT varsa, o kadar sayfa okunur.
    """

    # 1) PDF'i güvenli aç (yol veya stream)
    try:
        doc = _open_pdf(file)
    except Exception as e:
        # Uygulama genelinde hata yakalansın diye açıklayıcı raise
        raise RuntimeError(f"PDF okunamadı: {e}")

    # 2) Opsiyonel sayfa limiti
    page_limit = os.getenv("PDF_PAGE_LIMIT")
    try:
        limit = int(page_limit) if page_limit else None
    except ValueError:
        limit = None

    pages_iter = list(doc)[:limit] if limit else doc

    # 3) Sayfa sayfa metni çıkar ve temizle
    chunks = []
    for page in pages_iter:
        text = page.get_text() or ""
        lines = text.splitlines()

        cleaned_lines = [
            line.strip().replace("\xa0", " ")  # kırılmaz boşluk -> normal boşluk
            for line in lines
            if line.strip()                                   # boş satırları at
            and not all(ch in "-–—·•*.:_ " for ch in line)    # çizgi/madde/ayraç çöplüğü
        ]

        if cleaned_lines:
            chunks.append("\n".join(cleaned_lines))

    return "\n\n".join(chunks).strip()


def _open_pdf(file):
    """
    Dosyayı açmayı soyutlar:
    - Yol varsa: fitz.open(path)
    - file-like (read()) ise: fitz.open(stream=..., filetype='pdf')
    """
    # UploadFile ise .file vardır; onu içeri çevir
    if hasattr(file, "file"):  # FastAPI UploadFile
        file = file.file

    # file-like (stream) mi?
    if hasattr(file, "read"):
        # read() pointer'ı bozmasın diye geri sar
        data = file.read()
        try:
            file.seek(0)
        except Exception:
            pass
        return fitz.open(stream=data, filetype="pdf")

    # Yol / path-like / nesne.name
    path = None
    if isinstance(file, (str, os.PathLike)):
        path = str(file)
    elif hasattr(file, "name"):
        path = file.name

    if not path:
        raise ValueError("Geçersiz PDF dosyası/nesnesi (yol ya da read() gerekli).")

    return fitz.open(path)


