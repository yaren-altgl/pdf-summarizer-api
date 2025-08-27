def summarize_text(text, model, language="auto"):
    # Gelişmiş ve dile duyarlı prompt üreten yardımcı fonksiyon
    def create_structured_prompt(content, lang="auto"):
        if lang == "tr":
            return (
                "Aşağıdaki metni dikkatlice oku ve Türkçe olarak 3-5 cümleyle sade, anlaşılır bir özet çıkar:\n\n"
                f'"""\n{content}\n"""'
            )
        elif lang == "en":
            return (
                "Read the following text carefully and summarize it in English in 3 to 5 clear and concise sentences:\n\n"
                f'"""\n{content}\n"""'
            )
        else:
            return (
                "Read the following text and generate a clear and informative summary in 3 to 5 sentences, using the original language of the text:\n\n"
                f'"""\n{content}\n"""'
            )

    def safe_generate(prompt):
        """Model çağrısını güvenli yap, hata olursa açıklama döndür."""
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Özetleme sırasında hata oluştu: {str(e)}"

    # 3000 karakterden kısa metinleri doğrudan özetle
    if len(text) <= 3000:
        prompt = create_structured_prompt(text, language)
        return safe_generate(prompt)
    
    # Uzun metinleri parçalara ayırarak özetle
    chunks = [text[i:i+3000] for i in range(0, len(text), 3000)]
    partial_summaries = []

    for chunk in chunks:
        prompt = create_structured_prompt(chunk, language)
        partial_summaries.append(safe_generate(prompt))

    # Tüm özetleri birleştirip yeniden özet al
    combined_summary = "\n".join(partial_summaries)
    final_prompt = create_structured_prompt(combined_summary, language)
    return safe_generate(final_prompt)
