from sentence_transformers import CrossEncoder

from config.config import RERANKER_MODEL, FINAL_TOP_K


def rerank_chunks(question, results, top_k=FINAL_TOP_K):
    """
    Rerank retrieved chunks using a Cross-Encoder.

    Args:
        question: User's question.
        results: Results returned by ChromaDB.
        top_k: Number of final chunks to keep.

    Returns:
        List of reranked chunks.
    """

    # Load Cross-Encoder
    model = CrossEncoder(RERANKER_MODEL)

    # Get retrieved documents
    documents = results["documents"][0]

    # Create question-document pairs
    pairs = [
        [question, document]
        for document in documents
    ]

    # Calculate relevance scores
    scores = model.predict(pairs)

    # Combine scores with documents and metadata
    ranked_results = sorted(
        zip(
            scores,
            documents,
            results["metadatas"][0]
        ),
        key=lambda x: x[0],
        reverse=True
    )

    # Keep only the top results
    final_results = ranked_results[:top_k]

    return final_results

