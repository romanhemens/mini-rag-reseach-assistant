import hashlib
import os
from typing import List, Optional
from pymongo import MongoClient
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json
from datetime import datetime

class DocumentStore:
    def __init__(self, mongo_uri: str, db_name: str = "rag_documents"):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.documents = self.db.documents
        self.faiss_dir = "faiss_indices"
        os.makedirs(self.faiss_dir, exist_ok=True)

    def inspect_database(self):
        """Print information about stored documents."""
        print("\n=== MongoDB Document Store Inspection ===")
        print(f"Total documents in database: {self.documents.count_documents({})}")
        
        print("\nStored Documents:")
        for doc in self.documents.find():
            print(f"\nDocument Hash: {doc['file_hash']}")
            print(f"Created at: {doc['created_at']}")
            print(f"Number of chunks: {len(doc['chunks'])}")
            print(f"First chunk preview: {doc['chunks'][0][:100]}...")
            
        print("\n=== FAISS Indices ===")
        if os.path.exists(self.faiss_dir):
            indices = os.listdir(self.faiss_dir)
            print(f"Total FAISS indices: {len(indices)}")
            for idx in indices:
                print(f"- {idx}")
        else:
            print("No FAISS indices directory found")

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def document_exists(self, file_hash: str) -> bool:
        """Check if a document with the given hash exists."""
        return self.documents.find_one({"file_hash": file_hash}) is not None

    def save_document(self, file_hash: str, chunks: List[str], vectorstore: FAISS):
        """Save document chunks and vectorstore."""
        # Save chunks to MongoDB
        self.documents.insert_one({
            "file_hash": file_hash,
            "chunks": chunks,
            "created_at": datetime.utcnow()
        })
        
        # Save FAISS index
        index_path = os.path.join(self.faiss_dir, f"{file_hash}")
        vectorstore.save_local(index_path)

    def load_document(self, file_hash: str) -> Optional[tuple[List[str], FAISS]]:
        """Load document chunks and vectorstore."""
        # Load chunks from MongoDB
        doc = self.documents.find_one({"file_hash": file_hash})
        if not doc:
            return None

        # Load FAISS index
        index_path = os.path.join(self.faiss_dir, f"{file_hash}")
        if not os.path.exists(index_path):
            return None

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        
        return doc["chunks"], vectorstore

    def process_file(self, file_path: str, chunks: List[str], vectorstore: FAISS) -> bool:
        """Process a file, checking if it exists and saving if it doesn't."""
        file_hash = self.calculate_file_hash(file_path)
        
        if self.document_exists(file_hash):
            return False  # File already exists
        
        self.save_document(file_hash, chunks, vectorstore)
        return True  # File was newly processed 