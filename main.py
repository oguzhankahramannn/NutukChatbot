import os
import gradio as gr
from dotenv import load_dotenv

from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

print("Kurulum ve ayarlar yapılıyor...")
load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY ortam değişkeni bulunamadı. .env dosyanızı kontrol edin.")

llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("Modeller yüklendi.")

print("Nutuk veri seti (.jsonl) yükleniyor ve vektör veritabanı oluşturuluyor... Bu işlem biraz zaman alabilir.")

loader = JSONLoader(
    file_path='nutuk_lora_dataset.jsonl',
    jq_schema='.content',
    json_lines=True,
    text_content=False)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
texts = text_splitter.split_documents(documents)

vector_store = Chroma.from_documents(texts, embeddings, collection_name="nutuk-lora-chat")
print("Veritabanı hazır!")

# --- DEĞİŞİKLİK BURADA: Retriever'ı daha esnek ayarlarla yapılandırıyoruz ---
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'score_threshold': 0.5, 'k': 3}
)
# Açıklama:
# search_type="similarity_score_threshold": Arama tipini "benzerlik skoru eşiği" olarak ayarlar.
# score_threshold: 0.5: Benzerlik skoru 0.5'in üzerindeki sonuçları 'ilgili' olarak kabul etmesini sağlar. (Bu eşiği düşürdük).
# k: 3: En fazla 3 adet ilgili doküman getirmesini söyler.
# --------------------------------------------------------------------------------
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever  # Yeni ve daha akıllı retriever'ımızı kullanıyoruz
)


def get_rag_response(question):
    print(f"Sorgu alındı: {question}")
    result = qa_chain.invoke({"query": question})
    return result['result']

iface = gr.Interface(
    fn=get_rag_response,
    inputs=gr.Textbox(lines=5, placeholder="Nutuk ile ilgili bir soru sorun..."),
    outputs="text",
    title="📜 Nutuk Danışmanı Chatbot",
    description="Bu chatbot, Nutuk metinleri ile eğitilmiştir. Sorularınıza bu kaynaktan cevaplar üretecektir."
)

iface.launch()