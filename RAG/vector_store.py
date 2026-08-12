import chromadb

from config.config import CHROMA_PATH

from RAG.embeddings import (
    load_embedding_model,
    create_embeddings
)


def create_vector_store(chunks):

    # Load embedding model
    model = load_embedding_model()

    # Create ChromaDB client
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    # Create collection
    collection = client.get_or_create_collection(
        name="abandoned_properties"
    )
    if collection.count()>0:
        return collection

    # Prepare documents
    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    # Prepare metadata
    metadatas = [
        chunk["metadata"]
        for chunk in chunks
    ]

    # Create unique IDs
    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    # Generate embeddings
    embeddings = create_embeddings(
        documents,
        model
    )

    # Store in ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return collection