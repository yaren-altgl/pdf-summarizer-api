import gradio as gr
from main import extract_text_from_pdf, summarize_text, model
from language_utils import detect_language

def summarize_pdf_with_preview(file, summary_lang_label):
    text = extract_text_from_pdf(file)

    if len(text) < 20:
        return "PDF'den yeterli metin çıkarılamadı.", ""

    # Dil kodunu belirle
    lang_map = {
        "Otomatik (PDF dili neyse)": "auto",
        "Türkçe (Her durumda Türkçe özetle)": "tr",
        "İngilizce (Her durumda İngilizce özetle)": "en"
    }
    selected_lang = lang_map.get(summary_lang_label, "auto")

    # Özetle
    summary = summarize_text(text, model, selected_lang)

    # 2 çıktı: metnin tamamı (ön izleme) ve özet
    return text[:3000], summary  # metni kesip gösteriyoruz

# Arayüz
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

iface.launch(server_name="0.0.0.0", server_port=7860, share=True)
