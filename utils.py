# Load and Split Text
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import faiss
import time
from datetime import datetime, timedelta
import os
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# --- API Usage Tracking Variables ---
# Define your API limits
REQUEST_LIMIT_MINUTE = int(os.getenv("REQUEST_LIMIT_MINUTE", 30))  # Default to 30 if not set
TOKEN_LIMIT_MINUTE = int(os.getenv("TOKEN_LIMIT_MINUTE", 6000))  # Default to 6000 if not set
REQUEST_LIMIT_DAY = int(os.getenv("REQUEST_LIMIT_DAY", 14400))  # Default to 14400 if not set
TOKEN_LIMIT_DAY = int(os.getenv("TOKEN_LIMIT_DAY", 500000))  # Default to 500000 if not set

# Initialize counters and last reset times
request_count_minute = 0
token_count_minute = 0
last_minute_reset_time = time.time() # Unix timestamp

request_count_day = 0
token_count_day = 0
# Initialize daily reset time to the start of the current day
last_day_reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_text(text)

def build_faiss_store(chunks, embeddings):
    dim = len(embeddings.embed_query(chunks[0]))
    index = faiss.IndexFlatL2(dim)

    vectorstore = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    vectorstore.add_texts(chunks)
    return vectorstore

# --- Helper function to update and display usage metrics ---
def update_usage_metrics(estimated_tokens_for_current_call=0):
    global request_count_minute, token_count_minute, last_minute_reset_time
    global request_count_day, token_count_day, last_day_reset_time
    global REQUEST_LIMIT_MINUTE, TOKEN_LIMIT_MINUTE, REQUEST_LIMIT_DAY, TOKEN_LIMIT_DAY
    
    current_time_unix = time.time()
    current_datetime = datetime.now()

    # Reset minute counters if a minute has passed
    if current_time_unix - last_minute_reset_time >= 60:
        request_count_minute = 0
        token_count_minute = 0
        last_minute_reset_time = current_time_unix

    # Reset day counters if a new day has started
    if current_datetime.date() > last_day_reset_time.date():
        request_count_day = 0
        token_count_day = 0
        last_day_reset_time = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        
    # Increment counters for the current API call
    request_count_minute += 1
    token_count_minute += estimated_tokens_for_current_call
    request_count_day += 1
    token_count_day += estimated_tokens_for_current_call

    # Calculate remaining
    req_min_rem = max(0, REQUEST_LIMIT_MINUTE - request_count_minute)
    tok_min_rem = max(0, TOKEN_LIMIT_MINUTE - token_count_minute)
    req_day_rem = max(0, REQUEST_LIMIT_DAY - request_count_day)
    tok_day_rem = max(0, TOKEN_LIMIT_DAY - token_count_day)

    # Format for display
    return (
        f"**API Usage Status:**\n"
        f"- Requests (Minute): `{request_count_minute}/{REQUEST_LIMIT_MINUTE}` (`{req_min_rem}` remaining)\n"
        f"- Tokens (Minute): `{token_count_minute}/{TOKEN_LIMIT_MINUTE}` (`{tok_min_rem}` remaining)\n"
        f"- Requests (Day): `{request_count_day}/{REQUEST_LIMIT_DAY}` (`{req_day_rem}` remaining)\n"
        f"- Tokens (Day): `{token_count_day}/{TOKEN_LIMIT_DAY}` (`{tok_day_rem}` remaining)\n"
    )

    
