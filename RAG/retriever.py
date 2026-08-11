from sentence_transformers import SentenceTransformer

from config.config import EMBEDDING_MODEL,INITIAL_TOP_K


def retrieve_chunks(question,collection,top_k=INITIAL_TOP_K):
    """
    Convert the question into an embedding
    and retrieve the most relevant chunks
    from ChromaDB.
    """

    # Load the same embedding model
    # used for the document embeddings
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Convert question into embedding
    question_embedding = model.encode(question)

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=top_k
    )

    return results
