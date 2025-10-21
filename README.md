---
title: Nutuk Danışmanı Chatbot
emoji: 📜
colorFrom: pink
colorTo: yellow
sdk: gradio
app_file: app.py
python_version: "3.11"
license: mit
---

# 📜 Nutuk Danışmanı Chatbot

Nutuk Danışmanı, Mustafa Kemal Atatürk'ün Nutuk eseri ve ilgili temel tarihsel bilgiler üzerinde eğitilmiş, yapay zeka tabanlı bir Soru-Cevap uygulamasıdır. Retrieval Augmented Generation (RAG) mimarisi kullanılarak geliştirilen bu proje, tarih araştırmacılarının, öğrencilerin ve meraklıların Nutuk'un zengin içeriğinde kolayca arama yapmasını ve sorularına doğrudan metinden kanıta dayalı cevaplar almasını sağlar.

RAG mimarisi adımmları :
* **Veri Yükleme:** `.jsonl` ve `.txt` formatındaki Nutuk metinleri ve ek bilgiler `LangChain` document loader'ları ile yüklenir.
* **Parçalama (Chunking):** Uzun metinler, anlamsal bütünlüğü korunarak daha küçük parçalara ayrılır.
* **Vektör Gömme (Embedding):** Metin parçacıkları, `Hugging Face sentence-transformers` modeli ile anlamsal vektörlere dönüştürülür.
* **Vektör Depolama:** Vektörler, hızlı ve verimli anlamsal arama için `ChromaDB` veritabanında saklanır.
* **Getirme ve Cevap Üretme:** Kullanıcının sorusu üzerine, `RetrievalQA` zinciri en alakalı metin parçalarını bulur ve `Gemini` bu bağlama göre en doğru cevabı üretir.

### 🚀 Canlı Demo Linki

Uygulamayı Hugging Face Spaces üzerinden deneyimleyebilirsiniz:
**https://huggingface.co/spaces/oguzhankahraman/NutukChatbot**

### 📚 Veri Seti

Bu uygulama iki ana veri kaynağı kullanır:

1.  **`sinankarip/nutuk-chat-dataset`:** Projenin ana bilgi kaynağı olan bu veri seti, [Sinan Karip](https://huggingface.co/sinankarip) tarafından oluşturulmuş ve Hugging Face üzerinde paylaşılmıştır. Kendisine bu değerli emeği ve veri seti için teşekkürler.
2.  **`ek_bilgiler.txt`:** Verisette doğrudan geçmeyen (yazar, doğum yılı, eserin yapısı vb.) temel bilgileri içeren, manuel olarak oluşturulmuş bir metin dosyası.

### ✨ Özellikler ve Kullanım Alanları

* **Bağlama Dayalı Cevaplar:** Sadece Nutuk ve sağlanan ek bilgiler dahilinde cevaplar üreterek halüsinasyonu (bilgi uydurmayı) engeller.
* **Anlamsal Arama:** Kelime eşleşmesi yerine, cümlenin anlamına göre arama yaparak ilgili metinleri bulur.
* **Basit ve Kullanıcı Dostu Arayüz:** Gradio ile geliştirilmiş, herkesin kolayca kullanabileceği bir web arayüzü sunar.

**Kimler İçin ?:**
* Milli Mücadele dönemi üzerine çalışan tarih öğrencileri ve araştırmacılar.
* Nutuk'un belirli bir bölümü hakkında hızlıca bilgi almak isteyen herkes.


### 🛠️ Kullanılan Teknolojiler

* **Backend:** Python
* **GenAI:** Google Gemini 2.0 Flash, LangChain, Hugging Face Transformers
* **Vektör Veritabanı:** ChromaDB
* **Arayüz:** Gradio

### 💻 Yerel Kurulum Adımları

1.  Depoyu klonlayın:
    ```bash
    git clone [https://github.com/oguzhankahramannn/NutukChatbot.git](https://github.com/oguzhankahramannn/NutukChatbot.git)
    cd NutukChatbot
    ```
2.  Sanal bir ortam oluşturun ve aktive edin:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate     # Windows
    ```
3.  Gerekli paketleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
4.  `.env` adında bir dosya oluşturun ve içine Google API anahtarınızı ekleyin:
    ```
    GOOGLE_API_KEY="apikeyiniz"
    ```
5.  Uygulamayı çalıştırın:
    ```bash
    python app.py
    ```
6.  Tarayıcınızda `http://127.0.0.1:7860` adresine gidin.

