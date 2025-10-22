import os
import gradio as gr
from dotenv import load_dotenv
import gradio.themes as themes

# Hem JSON hem de TXT dosyalarını okumak için gerekli Loader'lar
from langchain_community.document_loaders import JSONLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

#  1. Kurulum ve Ayarlar
load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY bulunamadı.")

llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#  2. Veritabanını Kontrol Et veya Oluştur
persist_directory = "./chroma_db"
if not os.path.exists(persist_directory):
    print("Veritabanı bulunamadı, sıfırdan oluşturuluyor... Bu işlem birkaç dakika sürebilir.")


    #  JSONL dosyasını yükle
    print("1. Kaynak (nutuk_lora_dataset.jsonl) yükleniyor...")
    json_loader = JSONLoader(file_path='nutuk_lora_dataset.jsonl', jq_schema='.content', json_lines=True,
                             text_content=False)
    json_documents = json_loader.load()

    #  TXT dosyasını yükle
    print("2. Kaynak (ekveriler.txt) yükleniyor...")
    text_loader = TextLoader("ekveriler.txt", encoding="utf-8")
    text_documents = text_loader.load()

    # İki kaynaktan gelen dokümanları birleştir
    all_documents = json_documents + text_documents
    print(f"Toplam {len(all_documents)} doküman veritabanına eklenecek.")


    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    texts = text_splitter.split_documents(all_documents)

    vector_store = Chroma.from_documents(texts, embeddings, collection_name="nutuk-final-chat",
                                         persist_directory=persist_directory)
    print("Veritabanı oluşturuldu ve diske kaydedildi.")
else:
    print("Mevcut veritabanı yüklendi.")
    vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# Soru Cevap
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())


# Gradio Arayüzü
def get_rag_response(question):
    result = qa_chain.invoke({"query": question})
    return result['result']


example_questions = [
    "Nutuk'un yazarı kimdir?",
    "Atatürk'ün doğum yılı nedir?",
    "Bandırma vapuruyla Samsun'a çıkılma tarihi ?",
    "Amasya Genelgesi'nin önemi nedir?"
]
soft_theme = themes.Soft(primary_hue="neutral", secondary_hue="neutral")

iface = gr.Interface(
    fn=get_rag_response,
    inputs=gr.Textbox(lines=10, placeholder="Nutuk ile ilgili bir soru sorun...", label="Soru"),
    outputs=gr.Textbox(lines=10, label="Cevap"),
    title="📜 Nutuk Danışmanı Chatbot",
    description="Bu chatbot, nutuk metinleri dataseti ve ek temel bilgiler ile eğitilmiştir.",


    theme=soft_theme,

    examples=example_questions,
    submit_btn="Gönder",
    clear_btn="Temizle",
    allow_flagging="never"
)

iface.launch()