# app.py
import os
from dotenv import load_dotenv
import gradio as gr
import google.generativeai as genai

from pdf_utils import extract_text_from_pdf
from summarizer import summarize_text

# .env oku ve ENV'yi belirle
load_dotenv()
env = os.getenv("ENV", "dev")  # dev / prod

# Gemini yapılandır
genai.configure(api_key=os.getenv("keyim"))  # istersen GOOGLE_API_KEY'e geçir
model = genai.GenerativeModel("gemini-1.5-flash")

def summarize_pdf_with_preview(file, summary_lang_label):
    # PDF metnini al
    text = extract_text_from_pdf(file)

    if not text or len(text.strip()) < 20:
        return "PDF'den yeterli metin çıkarılamadı.", ""

    # Dil seçimi
    lang_map = {
        "Otomatik (PDF dili neyse)": "auto",
        "Türkçe (Her durumda Türkçe özetle)": "tr",
        "İngilizce (Her durumda İngilizce özetle)": "en"
    }
    selected_lang = lang_map.get(summary_lang_label, "auto")

    # Özetle
    summary = summarize_text(text, model, selected_lang)

    # Ön izleme (ilk 3000 karakter)
    return text[:3000], summary

# Gradio arayüzü
iface = gr.Interface(
    fn=summarize_pdf_with_preview,
    inputs=[
        gr.File(label="PDF Yükle (.pdf)"),
        gr.Radio(
            choices=[
                "Otomatik (PDF dili neyse)",
                "Türkçe (Her durumda Türkçe özetle)",
                "İngilizce (Her durumda İngilizce özetle)"
            ],
            value="Otomatik (PDF dili neyse)",
            label="Özet Dili"
        )
    ],
    outputs=[
        gr.Textbox(label="PDF'den Çıkarılan Metin (ön izleme)", lines=15),
        gr.Textbox(label="Özet", lines=8)
    ],
    title="PDF Otomatik Özetleyici",
    description="PDF içeriğini ön izle, özet dilini seç, 3-5 cümlede özet al!"
)

# ENV'ye göre public link
share_flag = (env == "dev")

iface.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=share_flag
)
