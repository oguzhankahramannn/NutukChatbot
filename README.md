---
title: Nutuk Danışmanı Chatbot
emoji: 📜
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
---

# Nutuk Danışmanı Chatbot

Nutuk Danışmanı Chatbot, Mustafa Kemal Atatürk'ün Nutuk eserine dayalı bir RAG (Retrieval Augmented Generation) tabanlı AI chatbot uygulamasıdır. Bu uygulama, Nutuk metinleri ve ek tarihi bilgileri kullanarak kullanıcıların Nutuk hakkındaki sorularını yanıtlar.

Uygulama, Nutuk'un tam metnini ve ek tarihi bilgileri içeren veri setlerini kullanarak, kullanıcıların Nutuk hakkındaki sorularını doğru ve kaynaklara dayalı şekilde yanıtlar. Chatbot, sadece verilen kaynaklara bağlı kalarak yanıt verir ve kendi bilgisini katmaz.

## Deploy Link

- https://huggingface.co/spaces/oguzhankahraman/nutuk-chatbot



## Dataset

Bu uygulama iki ana veri kaynağını kullanır:

1. **nutuk_lora_dataset.jsonl**: Nutuk'un tam metnini içeren JSONL formatındaki veri seti
2. **ekveriler.txt**: Nutuk hakkında ek tarihi bilgiler ve temel gerçekler

Her iki veri kaynağı da ChromaDB'ye embedding edilerek vektör veritabanında saklanır.

## Özellikler ve Kullanım Alanları

- **RAG Tabanlı Yanıtlama**: Sadece verilen kaynaklara dayalı yanıtlar
- **Çok Kaynaklı Bilgi**: Hem Nutuk metni hem de ek tarihi bilgiler
- **Strict Mode**: Chat kendi bilgisini katmaz, sadece kaynaklara bağlı kalır
- **Türkçe Arayüz**: Tamamen Türkçe kullanıcı arayüzü
- **Hızlı Yanıt**: ChromaDB vektör arama ile hızlı bilgi erişimi
- **Gradio Arayüzü**: Modern ve kullanıcı dostu web arayüzü

**İdeal Kullanım Alanları:**
- Tarih öğrencileri ve araştırmacıları
- Nutuk hakkında bilgi arayan kişiler
- Milli Mücadele dönemi hakkında sorular
- Atatürk ve Cumhuriyet tarihi araştırmaları
- Eğitim kurumlarında tarih dersleri

## Kullanılan Teknolojiler

- **Backend**: Python, Gradio
- **AI/ML**: Google Gemini 2.5 Flash, HuggingFace Embeddings
- **Vector Database**: ChromaDB
- **Framework**: LangChain
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Text Processing**: RecursiveCharacterTextSplitter

## RAG Pipeline

**Nutuk Danışmanı Chatbot tam bir RAG pipeline'ı uygular:**

1. **Veri Yükleme**: JSONL ve TXT dosyalarından metin çıkarma
2. **Metin Parçalama**: 1000 karakterlik chunk'lara bölme (150 karakter overlap)
3. **Embedding**: HuggingFace modeli ile vektör dönüşümü
4. **Vektör Depolama**: ChromaDB'de kalıcı saklama
5. **Benzerlik Arama**: Kullanıcı sorusuna en yakın 5 doküman bulma
6. **Yanıt Üretimi**: Gemini ile kaynaklara dayalı yanıt oluşturma

## Yerel Kurulum Adımları

1. Repository'yi klonlayın:
   ```bash
   git clone https://github.com/your-username/NutukChatbot.git
   cd NutukChatbot
   ```

2. Sanal ortam oluşturun ve aktifleştirin:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

4. `.env` dosyası oluşturun ve Google API anahtarınızı ekleyin:
   ```
   GOOGLE_API_KEY=your_api_key
   ```

5. Uygulamayı çalıştırın:
   ```bash
   python app.py
   ```

6. Tarayıcınızda `http://localhost:8080` adresine gidin

## Örnek Sorular

- "Nutuk'un yazarı kimdir?"
- "Atatürk'ün doğum yılı nedir?"
- "Bandırma vapuruyla Samsun'a çıkılma tarihi?"
- "Amasya Genelgesi'nin önemi nedir?"

## Proje Yapısı

```
NutukChatbot/
├── app.py                      # Ana uygulama dosyası
├── requirements.txt           # Python bağımlılıkları
├── nutuk_lora_dataset.jsonl   # Nutuk metni veri seti
├── ekveriler.txt              # Ek tarihi bilgiler
├── chroma_db/                 # ChromaDB vektör veritabanı
├── assets/                    # Demo görselleri
│   └── Ekran Kaydı 2025-10-22 20.45.44.gif
├── venv/                      # Python sanal ortamı
└── README.md                  # Proje dokümantasyonu
```

## API Kullanımı

Uygulama Gradio arayüzü üzerinden çalışır. API endpoint'i:
- **Local**: `http://localhost:8080`
- **Hugging Face Spaces**: Deploy edildikten sonra Spaces URL'i




## Teşekkür

* **Veri Seti Linki:** [https://huggingface.co/datasets/sinankarip/nutuk-chat-dataset](https://huggingface.co/datasets/sinankarip/nutuk-chat-dataset)