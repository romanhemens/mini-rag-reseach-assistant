# Build the RAG pipeline
from dotenv import load_dotenv
load_dotenv()

import faiss
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from utils import build_faiss_store
import os

def build_rag_chain(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    vector_store = build_faiss_store(chunks, embeddings)
    retriever = vector_store.as_retriever()
    
    # Initialize the LLM with the API key and model name
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192")
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa
