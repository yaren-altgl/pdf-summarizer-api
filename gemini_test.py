import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("keyim"))

# Model adı burada değiştirildi
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

response = model.generate_content("Bu metni 3 cümlede özetle: Yapay zeka son yıllarda hızla gelişiyor. Özellikle dil modelleme sistemleri dikkat çekiyor.")
print(response.text)











