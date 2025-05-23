# Build the RAG pipeline
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
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
        model_name="llama3-70b-8192",
        temperature=0.1, #  For a research assistant, you want highly factual, precise, and consistent answers that stick strictly to the provided context.
        top_p=0.9, #  This setting can help in generating more focused and relevant responses.
        max_tokens=500, #  Set a reasonable limit to ensure the model doesn't generate excessively long responses.
        #stop=["\n\n"] #  (optional) This will help in stopping the generation at the end of the answer.    
        )
    
    system_prompts = (
        "You are an expert research assistant, tasked with providing accurate and concise answers "
        "based solely on the provided document context. "
        "Your responses should directly address the user's question by extracting relevant information from the context. "
        "If the context contains the answer, synthesize and summarize it to provide a clear and direct response. "
        "If the context does not contain the answer, or is insufficient to form a complete answer, "
        "you MUST respond with 'I don't know'. "
        "Do not use any outside knowledge. Do not fabricate information. "
        "Maintain a professional and objective tone, focusing on factual accuracy from the given text."
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompts),
            ("human", "Answer the following question based on the provided context:\n\nContext: {context}\n\nQuestion: {input}")
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    qa = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=question_answer_chain
    )
    return qa
