# Build the RAG pipeline
from dotenv import load_dotenv
load_dotenv

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatGroq
import os

def build_rag_chain(chunks):
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_texts(chunks, embedding=embeddings)
    retriever = db.as_retriever()

    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192")
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa
