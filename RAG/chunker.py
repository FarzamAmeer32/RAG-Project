from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.config import CHUNK_SIZE, CHUNK_OVERLAP


def create_chunks(sections):
    """
    Split each legal section into smaller chunks
    while preserving section metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            " ",
            ""
        ]
    )

    chunks = []

    for section in sections:

        section_chunks = splitter.split_text(
            section["text"]
        )

        for chunk_text in section_chunks:

            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "section": section["section"],
                    "title": section["title"],
                    "page": section["page"],
                    "source": "Abandoned Properties (Management) Act, 1975"
                }
            })

    return chunks