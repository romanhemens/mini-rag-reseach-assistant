from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from utils import extract_text_from_pdf, split_text, update_usage_metrics
from rag_chain import build_rag_chain

app = Flask(__name__)
CORS(app)

# Global variable to store the QA chain
qa_chain = None

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global qa_chain
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
        
    if file:
        try:
            # Save the file temporarily
            filename = secure_filename(file.filename)
            temp_path = os.path.join('/tmp', filename)
            file.save(temp_path)
            
            # Process the PDF
            text = extract_text_from_pdf(temp_path)
            chunks = split_text(text)
            qa_chain = build_rag_chain(chunks)
            
            # Clean up
            os.remove(temp_path)
            
            return jsonify({'message': 'PDF processed successfully'}), 200
            
        except Exception as e:
            return jsonify({'message': f'Error processing PDF: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    global qa_chain
    
    if not qa_chain:
        return jsonify({'message': 'Please upload a PDF first'}), 400
        
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'message': 'No question provided'}), 400
        
    question = data['question']
    
    try:
        response = qa_chain.invoke({"input": question})
        response_text = response.get("answer", str(response))
        
        # Estimate tokens used for the current interaction
        estimated_tokens = len(question.split()) + len(response_text.split()) + 50
        
        # Update usage metrics
        usage_status = update_usage_metrics(estimated_tokens)
        
        return jsonify({
            'answer': response_text,
            'usage_status': usage_status
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error answering question: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
