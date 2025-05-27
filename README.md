# Mini RAG Research Assistant

A powerful Research Assistant that uses RAG (Retrieval-Augmented Generation) to help you analyze and query PDF documents. This application combines the power of Groq's LLM with efficient document processing to provide accurate and context-aware responses to your questions.

## Features

- PDF document upload and processing
- Intelligent text chunking and embedding
- RAG-based question answering
- Usage metrics tracking
- RESTful API endpoints
- Modern web interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mini-rag-reseach-assistant.git
cd mini-rag-reseach-assistant
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env-template .env
```
Edit the `.env` file and add your Groq API key and other configuration values.

## Running the Application

1. Start the backend server:
```bash
python app.py
```
The server will start on `http://localhost:5000`

2. In a separate terminal, start the frontend development server:
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`

## API Endpoints

- `POST /upload`: Upload a PDF file for processing
- `POST /ask`: Ask questions about the uploaded document

## Usage Limits

The application implements rate limiting to manage API usage:
- Requests per minute
- Tokens per minute
- Requests per day
- Tokens per day

These limits can be configured in the `.env` file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
