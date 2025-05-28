from document_store import DocumentStore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize document store
store = DocumentStore(os.getenv("MONGO_URI", "mongodb://localhost:27017"))

# Run inspection
store.inspect_database()