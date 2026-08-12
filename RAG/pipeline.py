from config.config import INITIAL_TOP_K, FINAL_TOP_K
from RAG.document_loader import load_pdf
from RAG.text_cleaner import clean_pages
from RAG.section_extractor import (
    extract_sections,
    add_page_metadata
)
from RAG.chunker import create_chunks
from RAG.vector_store import create_vector_store
from RAG.retriever import retrieve_chunks
from RAG.reranker import rerank_chunks
from RAG.generator import generate_answer
from config.config import PDF_PATH


def build_rag_pipeline():
    """
    Build the complete RAG pipeline.

    This loads the PDF, processes it, creates chunks,
    generates embeddings, and stores them in ChromaDB.
    """

    # Step 1 — Load PDF
    pages = load_pdf(PDF_PATH)

    # Step 2 — Clean pages
    cleaned_pages = clean_pages(pages)

    # Step 3 — Combine pages
    document = "\n\n".join(cleaned_pages)

    # Step 4 — Extract sections
    sections = extract_sections(document)

    # Step 5 — Add page metadata
    sections = add_page_metadata(
        sections,
        cleaned_pages
    )

    # Step 6 — Create chunks
    chunks = create_chunks(sections)

    # Step 7 — Create vector store
    collection = create_vector_store(chunks)

    return collection


def rag_pipeline(question, collection):
    """
    Run retrieval, reranking, and generation
    for a user question.

    Args:
        question: User's question.
        collection: ChromaDB collection.

    Returns:
        Dictionary containing answer and sources.
    """

    # Step 8 — Retrieve
    results = retrieve_chunks(
        question,
        collection,
        top_k=INITIAL_TOP_K
    )

    # Step 9 — Rerank
    reranked_results = rerank_chunks(
        question,
        results,
        top_k=FINAL_TOP_K
    )

    # Step 10 — Generate
    answer = generate_answer(
        question,
        reranked_results
    )

    # Prepare sources for frontend
    sources = []

    for score, document, metadata in reranked_results:
        if score<0:
            continue

        sources.append({
            "section": metadata["section"],
            "title": metadata["title"],
            "page": metadata["page"],
            "source": metadata["source"],
            "score": float(score)
        })

    if not sources:
        return {
        "answer": answer,
        "sources": [
            {
                "message": "No Strong Source Available"
            }
        ]
    }


    return {
        "answer": answer,
        "sources": sources
    }