from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent


# Data
PDF_PATH = BASE_DIR / "PDF" / "ACT-1975.pdf"


# ChromaDB
CHROMA_PATH = "chroma_db"


# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# Reranker
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"





# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


# Retrieval
INITIAL_TOP_K = 10
FINAL_TOP_K = 3