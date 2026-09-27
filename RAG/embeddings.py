from sentence_transformers import SentenceTransformer

from config.config import EMBEDDING_MODEL


def load_embedding_model():
    """
    Load the embedding model.
    """

    model = SentenceTransformer(EMBEDDING_MODEL)

    return model


def create_embeddings(documents, model):
    """
    Convert documents into vector embeddings.

    Args:
        documents: List of text documents.
        model: Loaded SentenceTransformer model.

    Returns:
        List of embeddings.
    """

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    )

    return embeddings.tolist()