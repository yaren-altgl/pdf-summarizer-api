# test_api.py
import requests
url = "http://127.0.0.1:8000/upload-pdf/"
files = {"file": ("ornek.pdf", open("ornek.pdf", "rb"), "application/pdf")}
data = {"summary_language": "auto"}
r = requests.post(url, files=files, data=data, timeout=120)
print(r.status_code)
print(r.json())
