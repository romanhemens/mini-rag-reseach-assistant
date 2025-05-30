# Mini RAG Research Assistant

A lightweight Research Assistant using RAG (Retrieval-Augmented Generation) to answer questions about uploaded documents.

## Features

- Document upload and processing
- Efficient document caching using MongoDB and FAISS
- Question answering using Groq LLM
- API usage tracking and rate limiting
- Secure document storage and retrieval

## Security Considerations

- All sensitive data (API keys, database credentials) are stored in `.env` file
- MongoDB connection is local by default
- Document processing includes hash verification
- FAISS indices are stored locally with proper security measures

## Setup

### Option 1: Local Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env-template` to `.env` and fill in your credentials:
   ```bash
   cp .env-template .env
   ```
4. Set up MongoDB locally or update the `MONGO_URI` in `.env`
5. Run the application:
   ```bash
   python app.py
   ```

### Option 2: Docker Setup

1. Clone the repository
2. Copy `.env-template` to `.env` and fill in your credentials:
   ```bash
   cp .env-template .env
   ```
3. Make sure MongoDB is running locally
4. Build and run the containers:
   ```bash
   docker-compose up --build
   ```
   The application will be available at:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:5000

## Environment Variables

Required environment variables in `.env`:
- `GROQ_API_KEY`: Your Groq API key
- `GROQ_MODEL_NAME`: The Groq model to use
- `MONGO_URI`: MongoDB connection string (default: mongodb://localhost:27017)
- `REQUEST_LIMIT_MINUTE`: API request limit per minute
- `TOKEN_LIMIT_MINUTE`: Token limit per minute
- `REQUEST_LIMIT_DAY`: API request limit per day
- `TOKEN_LIMIT_DAY`: Token limit per day

## Project Structure

- `app.py`: Main Flask application
- `rag_chain.py`: RAG pipeline implementation
- `utils.py`: Utility functions for document processing
- `document_store.py`: Document storage and retrieval
- `frontend/`: Frontend application files
- `Dockerfile.backend`: Backend Docker configuration
- `frontend/Dockerfile`: Frontend Docker configuration
- `docker-compose.yml`: Docker services orchestration

## TODO / Roadmap

Here are some features and improvements planned for future versions:

### Core Features
- [ ] Support multi-document querying (merge multiple PDFs into a single context)
- [ ] Chunk size and overlap tuning for better embedding performance
- [ ] Add support for other document types (e.g., `.docx`, `.txt`)

### Data & Storage
- [ ] Add deduplication to avoid re-uploading the same file
- [ ] Move from FAISS to a persistent vector DB (e.g., ChromaDB, Qdrant, Weaviate)
- [ ] Store embeddings alongside metadata in the DB

### 🔍 Search & Retrieval
- [ ] Hybrid search (vector + keyword-based scoring)
- [ ] Re-ranking answers using an LLM (e.g., via Groq or OpenAI)

### Frontend / UX
- [ ] Drag & drop file upload
- [ ] Highlight source chunks used in answers
- [ ] Document preview after upload

### Testing & Dev Experience
- [ ] Add backend unit tests (e.g., using Pytest)
- [ ] Add integration tests for upload + query
- [ ] Set up GitHub Actions for CI/CD

### Stretch Goals / Ideas
- [ ] Real-time collaboration / shared documents
- [ ] User auth (e.g., email or GitHub OAuth)
- [ ] Embedding model selection (e.g., OpenAI vs HuggingFace)

## Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.  
Check out [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines and ideas on what to work on.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
