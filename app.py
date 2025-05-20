import gradio as gr
from utils import extract_text_from_pdf, split_text
from rag_chain import build_rag_chain

qa_chain = None

def upload_pdf(file):
    global qa_chain
    text = extract_text_from_pdf(file.name)
    chunks = split_text(text)
    qa_chain = build_rag_chain(chunks)
    return "PDF processed. You can now ask questions!"

def ask_question(question):
    if qa_chain:
        response = qa_chain.invoke(question)
        return response['result']
    else:
        return "Please upload a PDF first."

iface = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="Ask a question"),
    outputs=gr.Textbox(label="Answer"),
    title="Mini-RAG Assistant",
    description="Upload a PDF and ask questions about it.",
    live=True
)

upload = gr.Interface(
    fn=upload_pdf,
    inputs=gr.File(file_types=[".pdf"]),
    outputs="text",
    title="Upload Your PDF"
)

gr.TabbedInterface([upload, iface], ["Upload", "Ask"]).launch()
