import fitz

def extract_text_from_pdf(file):
    doc = fitz.open(file.name)  # doğrudan yolu veriyoruz
    full_text = ""

    for page in doc:
        text = page.get_text()
        lines = text.splitlines()
        cleaned_lines = [
            line.strip().replace(" ", " ")
            for line in lines
            if line.strip() and not all(char in "-–—·•*" for char in line.strip())
        ]
        page_text = "\n".join(cleaned_lines)
        full_text += page_text + "\n\n"

    return full_text.strip()

