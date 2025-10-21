# Bu kod, veritabanının var olup olmadığını kontrol eder.
# Eğer yoksa oluşturur, varsa direkt yükler.
import os
import gradio as gr
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY bulunamadı.")

llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# --- YENİ MANTIK BURADA ---
persist_directory = "./chroma_db"
if not os.path.exists(persist_directory):
    print("Veritabanı bulunamadı, sıfırdan oluşturuluyor... Bu işlem birkaç dakika sürebilir.")
    loader = JSONLoader(file_path='nutuk_lora_dataset.jsonl', jq_schema='.content', json_lines=True, text_content=False)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    texts = text_splitter.split_documents(documents)
    vector_store = Chroma.from_documents(texts, embeddings, collection_name="nutuk-lora-chat", persist_directory=persist_directory)
    print("Veritabanı oluşturuldu ve diske kaydedildi.")
else:
    print("Mevcut veritabanı yüklendi.")
    vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
# --- YENİ MANTIK SONU ---

qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

def get_rag_response(question):
    result = qa_chain.invoke({"query": question})
    return result['result']

iface = gr.Interface(fn=get_rag_response, inputs=gr.Textbox(lines=5, placeholder="Nutuk ile ilgili bir soru sorun..."), outputs="text", title="📜 Nutuk Danışmanı Chatbot")
iface.launch()