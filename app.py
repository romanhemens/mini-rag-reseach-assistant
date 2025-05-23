import gradio as gr
from utils import extract_text_from_pdf, split_text, update_usage_metrics
from rag_chain import build_rag_chain

qa_chain = None

# --- Gradio Functions --
def upload_pdf(file):
    global qa_chain
    # Ensure the file path is accessible
    if file is None:
        return "Please upload a PDF file.", ""
    
    try:
        text = extract_text_from_pdf(file.name)
        chunks = split_text(text)
        qa_chain = build_rag_chain(chunks)
        return "PDF processed. You can now ask questions!", ""
    except Exception as e:
        return f"Error processing PDF: {e}", ""

def ask_question(question):
    if qa_chain:
        try:            
            response = qa_chain.invoke({"input": question})
            response_text = response.get("answer", str(response))
        
            # Estimate tokens used for the current interaction
            # This is a rough estimate based on word count. => use a proper tokenizer later
            estimated_tokens = len(question.split()) + len(response_text.split()) + 50 # Add some overhead for prompt tokens
            
            # Update and get usage status from the helper in utils.py
            usage_status = update_usage_metrics(estimated_tokens)
            
            print("DEBUG RESPONSE:", response_text)
            return response_text, usage_status

        except Exception as e:
            return f"Error answering question: {e}"
    else:
        return "Please upload a PDF first."

# --- Gradio Interface Setup using gr.Blocks ---
with gr.Blocks(title="Mini-RAG Assistant") as demo:
    # Define the output component for API usage status once
    usage_display = gr.Markdown(label="API Usage Status", value=update_usage_metrics(0)) # Initialize with current status

    with gr.Tab("Upload"):
        gr.Markdown("Upload a PDF and process it for questions.")
        upload_file_input = gr.File(file_types=[".pdf"], label="Upload Your PDF")
        upload_output_text = gr.Textbox(label="Processing Status")
        
        # Link the upload function to the components
        upload_file_input.upload(
            fn=upload_pdf,
            inputs=[upload_file_input],
            outputs=[upload_output_text, usage_display] # Update both status text and usage display
        )

    with gr.Tab("Ask"):
        gr.Markdown("Ask questions about the uploaded PDF.")
        question_input = gr.Textbox(label="Ask a question")
        answer_output = gr.Textbox(label="Answer")
        
        # Link the ask_question function to the components
        question_input.submit(
            fn=ask_question,
            inputs=[question_input],
            outputs=[answer_output, usage_display] # Update both answer and usage display
        )

# Launch the Gradio application
demo.launch()
