# PDF Auto-Summarizer API

Bu proje, kullanıcılardan alınan PDF dosyalarının içeriğini işleyerek kısa ve anlaşılır bir özetini üreten bir API uygulamasıdır. Hedef kitlesi, freelance çalışanlar, akademisyenler, öğrenciler ve iş dünyasında yoğun doküman trafiği yaşayan profesyonellerdir.

## Proje Amacı

PDF belgeleri genellikle uzun ve zaman alıcıdır. Bu proje ile kullanıcılar bir PDF dosyası yükleyerek, dosya içeriğinin 5-6 cümlelik özetine hızlıca ulaşabilirler. Temel amaç, belge okuma ve anlama sürecini kolaylaştırmaktır.

## Kullanılan Teknolojiler

| Amaç | Teknoloji | Açıklama |
|:----|:----------|:---------|
| API geliştirme | FastAPI | Python tabanlı modern ve hızlı API framework'ü |
| Sunucu yönetimi | Uvicorn | FastAPI uygulamasını çalıştırmak için |
| PDF işleme | pdfplumber | PDF dosyasından sayfa bazlı metin çıkarımı |
| LLM ile özetleme | Google Gemini API | OpenAI alternatifi olarak kullanılan güçlü bir LLM |
| Ortam değişkenleri yönetimi | python-dotenv + os | API key'lerini güvenli şekilde yönetmek için |
| Hata ve süreç takibi | loguru | Uygulama loglarının kaydı |
| Web arayüzü (opsiyonel) | Gradio | Kullanıcı dostu bir yükleme ve özet görüntüleme arayüzü |

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
keyim=BURAYA_GEMINI_API_KEYINIZI_YAZIN
```

> `.env` dosyası `.gitignore` içerisinde belirtilmiş olup GitHub'a yüklenmez.

## Proje Yapısı

```
pdf-summarizer-api/
├── logs/                 # Log dosyalarının kaydedildiği klasör
├── .env                  # Ortam değişkenleri dosyası (GitHub'a yüklenmedi.)
├── .gitignore            # Git tarafından yok sayılacak dosyalar
├── error_handlers.py     # API hata yönetimi
├── gemini_test.py        # Gemini API test dosyası
├── gradio_ui.py          # Opsiyonel Gradio arayüzü
├── language_utils.py     # Dil ile ilgili yardımcı işlemler
├── logger.py             # Loglama işlemleri
├── main.py               # FastAPI uygulaması başlangıç dosyası
├── pdf_utils.py          # PDF'ten metin çıkarma işlemleri
├── requirements.txt      # Gerekli kütüphaneler listesi
├── response_models.py    # API için Pydantic modelleri
└── summarizer.py         # Metni özetleme işlemleri
```

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

## Gelecekteki Geliştirme Fikirleri

- Otomatik cümle başı algılama ve daha doğal özet oluşturma
- Çok dilli özet desteği (language detection)
- Özetin madde madde (bullet points) şeklinde sunulması
- Kullanıcı authentication ve istek limitleri eklenmesi

---

Bu proje, temel API geliştirme, PDF işleme, LLM entegrasyonu, loglama ve bulut sunucu yönetimi becerilerini kapsayacak şekilde hazırlanmıştır.
