# PDF Auto-Summarizer API

Bu proje, kullanıcılardan alınan PDF dosyalarının içeriğini işleyerek kısa ve anlaşılır bir özetini üreten bir API uygulamasıdır. Hedef kitlesi, freelance çalışanlar, akademisyenler, öğrenciler ve iş dünyasında yoğun doküman trafiği yaşayan profesyonellerdir.

## 🚀 Demo
[PDF Summarizer](http://54.226.220.99:7860)

⚠️
- Tarayıcıda **“Güvenli değil” (Not Secure)** uyarısı çıkabilir. Bu, uygulamanın **HTTP üzerinden** çalışmasından kaynaklıdır (henüz HTTPS/SSL sertifikası eklenmediği için).  
  **Bu bir güvenlik riski değildir; uygulamayı normal şekilde açıp test edebilirsiniz.**
- Bu link bir **AWS EC2 instance** üzerinde çalışmaktadır. Instance yeniden başlatılırsa IP adresi değişebilir.  
  - IP’nin sabit kalmasını istersen AWS’de **Elastic IP** ayırıp bu instance’a bağlayabilirsin. (Running durumunda bağlı EIP ücretsizdir.)
    
## Proje Amacı

PDF belgeleri genellikle uzun ve zaman alıcıdır. Bu proje ile kullanıcılar bir PDF dosyası yükleyerek, dosya içeriğinin 5-6 cümlelik özetine hızlıca ulaşabilirler. Temel amaç, belge okuma ve anlama sürecini kolaylaştırmaktır.

## Kullanılan Teknolojiler

# Kullanılan Teknolojiler

| Amaç | Teknoloji | Açıklama |
|:----|:----------|:---------|
| Web arayüzü | Gradio | Kullanıcı dostu yükleme & özetleme arayüzü |
| PDF işleme | PyMuPDF (fitz) | PDF dosyasından metin çıkarımı |
| LLM ile özetleme | Google Gemini API | Özet üretimi için güçlü LLM |
| Ortam değişkenleri | python-dotenv | API key’lerini güvenli yönetmek için |
| Hata ve log yönetimi | loguru | Hataların kaydı ve takip |
| Dil algılama | langdetect | PDF içeriğinin dilini otomatik algılama |
| Cloud deployment | AWS EC2 + systemd | Uygulamanın bulutta barındırılması ve yeniden başlatıldığında otomatik çalışması |

## Gereksinimler

- Python 3.9+

### Gerekli Kütüphaneler

Tüm bağımlılıklar `requirements.txt` dosyasında tanımlıdır.

```
pip install -r requirements.txt
```

## Ortam Değişkenleri

Proje, bir `.env` dosyası üzerinden API anahtarlarını yönetir. `.env` dosyasına aşağıdaki satır eklenmelidir:

```
keyim=BURAYA_GEMINI_API_KEYINIZ
ENV=prod
PDF_PAGE_LIMIT=10
```

> `.env` dosyası `.gitignore` içerisinde belirtilmiş olup GitHub'a yüklenmez.

## Proje Yapısı

```
pdf-summarizer/
├── logs/               # Log dosyaları
├── .env                # Ortam değişkenleri (repo dışı)
├── .gitignore          # Git ignore kuralları
├── app.py              # Gradio arayüzü (ana giriş noktası)
├── error_handlers.py   # Hata yönetimi
├── gemini_test.py      # Gemini API test dosyası
├── language_utils.py   # Dil algılama fonksiyonları
├── logger.py           # Loglama altyapısı
├── main.py             # (Opsiyonel FastAPI başlangıç noktası)
├── pdf_utils.py        # PDF’ten metin çıkarımı
├── requirements.txt    # Gereken kütüphaneler
├── response_models.py  # Özet modelleri
└── summarizer.py       # Özetleme fonksiyonları

```
## ☁️ Deployment  

Aşağıdaki ekran görüntüsü, uygulamanın **AWS EC2 üzerinde canlı olarak çalıştırıldığını** göstermektedir:  
<img width="1895" height="390" alt="Screenshot 2025-08-28 033925" src="https://github.com/user-attachments/assets/92563839-a858-4178-9695-ca3d40102903" />


## Kurulum ve Çalıştırma Adımları

1. Proje klasörüne geçin.
2. Sanal ortam oluşturun ve aktif edin:

```
python -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)
```

3. Gerekli paketleri yükleyin:

```
pip install -r requirements.txt
```

4. `.env` dosyasını oluşturun ve API anahtarınızı ekleyin.

5. Uygulamayı başlatın:

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

6. Tarayıcı üzerinden test etmek için:

```
http://localhost:8000/docs
```

## Loglama

Proje içerisinde `loguru` kütüphanesi kullanılarak kapsamlı bir loglama altyapısı kurulmuştur. Sunucu başlatıldığında ve her istek alındığında işlemler `logs/` klasörü altında günlük dosyalarına kaydedilir.

Kayıt altına alınanlar:
- API'ye gelen istekler ve dosya bilgileri
- Özetleme sürecindeki hatalar ve başarı mesajları
- LLM API çağrıları ve cevapları

Bu sistem, hataların hızlı tespiti ve operasyonel izleme kolaylığı sağlar.

## Gradio Web Arayüzü (Opsiyonel)

İsteyen kullanıcılar için Gradio ile basit bir web arayüzü hazırlanmıştır.

Çalıştırmak için:

```
python gradio_ui.py
```

Başarılı çalışırsa bir gradio.live linki üretilecek ve kullanıcılar PDF yükleyerek özetleri görebileceklerdir.

## Canlı Yayına Alma (Deployment)

Proje AWS EC2 üzerinde test edilmiştir.

- EC2 instance başlatıldı ve gerekli portlar (8000) açıldı.
- SSH ile bağlantı kurularak proje sunucuya taşındı.
- Uygulama sanal ortamda kuruldu ve çalıştırıldı.
- `.env` gibi hassas bilgiler sunucu üzerinde gizli tutuldu.

İleri aşamada Docker container ile deployment yapılması tavsiye edilir.


Bu proje, temel API geliştirme, PDF işleme, LLM entegrasyonu, loglama ve bulut sunucu yönetimi becerilerini kapsayacak şekilde hazırlanmıştır.
