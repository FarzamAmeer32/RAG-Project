# Day 2 — RAG Pipeline Implementation

## Overview

On Day 2, the basic RAG concepts explored on Day 1 were applied to a real-world legal document:

**The Abandoned Properties (Management) Act, 1975**

The focus was on building the core Retrieval-Augmented Generation (RAG) pipeline, with particular attention to document preprocessing, section-aware chunking, metadata, embeddings, vector search, retrieval, and answer generation.

The web interface was not the focus of this stage.

---

## Document

**Document:** The Abandoned Properties (Management) Act, 1975

**Pages:** 12

The document contains 30 sections covering topics such as:

* Definitions
* Vesting of abandoned property
* Board of Trustees
* Appointment of Administrators
* Claims by interested persons
* Appeals and revision
* Penalties
* Powers of the Federal Government

---

## Day 2 Objectives

The main objectives were to:

1. Load and extract text from the legal PDF.
2. Clean the extracted text.
3. Remove unnecessary contents-page information.
4. Detect the 30 legal sections.
5. Split large sections into smaller chunks.
6. Attach metadata to each chunk.
7. Generate embeddings for the chunks.
8. Store embeddings in FAISS.
9. Perform similarity-based retrieval.
10. Pass retrieved context to an LLM.
11. Generate answers grounded in the retrieved context.
12. Use metadata to provide source citations.

---

## RAG Pipeline

```text
                Legal PDF
                    │
                    ▼
             PDF Text Extraction
                    │
                    ▼
               Text Cleaning
                    │
                    ▼
          Remove Contents Pages
                    │
                    ▼
             Detect Sections
                    │
                    ▼
          Section-Aware Chunking
                    │
                    ▼
               Add Metadata
                    │
                    ▼
            Generate Embeddings
                    │
                    ▼
                  FAISS
                    │
                    ▼
             User Question
                    │
                    ▼
           Question Embedding
                    │
                    ▼
            Similarity Search
                    │
                    ▼
            Relevant Chunks
                    │
              ┌─────┴─────┐
              ▼           ▼
           Context     Metadata
              │           │
              ▼           ▼
             Qwen      Source Info
              │           │
              └─────┬─────┘
                    ▼
              Final Answer
                    │
                    ▼
                Citation
```

---

## 1. PDF Loading

The PDF was loaded using `pypdf`.

Text was extracted **page-by-page** instead of treating the entire document as one string. This allowed page information to be preserved for later source citation.

Example structure:

```python
{
    "page": 5,
    "text": "..."
}
```

---

## 2. Text Cleaning

The extracted PDF text contained formatting artifacts caused by PDF extraction.

Basic preprocessing was performed to:

* Remove `Page X of Y` markers.
* Remove excessive spaces.
* Fix escaped section numbers.
* Remove excessive blank lines.
* Normalize the extracted text.

The cleaning was intentionally kept simple to avoid accidentally modifying the meaning of legal text.

---

## 3. Removing Contents Pages

The first two pages contained the table of contents rather than the actual legal text.

Therefore, pages 1 and 2 were excluded from the RAG knowledge base.

The actual Act begins from page 3.

Page markers were retained internally in the document:

```text
[PAGE 3]
[PAGE 4]
[PAGE 5]
...
```

This helped identify the source page of each section.

---

## 4. Section Detection

The legal document has **30 sections**.

A regular expression was used to identify section headings such as:

```text
1. Short title, extent and commencement
2. Definitions
3. Vesting of abandoned property in Government
...
30. Power to make rules
```

Each detected section was stored separately.

Example:

```python
{
    "section": "6",
    "title": "Holding of abandoned property and its surrender, etc.",
    "text": "..."
}
```

This section-aware approach was preferred over blindly splitting the entire document because legal documents have meaningful structural boundaries.

---

## 5. Chunking Strategy

A combination of **section-aware chunking** and `RecursiveCharacterTextSplitter` was used.

The approach was:

```text
Section
   │
   ├── ≤ 1000 characters → Keep as one chunk
   │
   └── > 1000 characters → Recursive splitting
```

Configuration:

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)
```

### Why 1000 characters?

The goal was to keep enough legal context inside each chunk while preventing chunks from becoming unnecessarily large.

### Why 150-character overlap?

Overlap helps preserve context when a sentence or important information falls near a chunk boundary.

---

## 6. Metadata

Metadata was attached to every chunk.

Example:

```python
{
    "text": "...",

    "metadata": {
        "source": "Abandoned Properties (Management) Act, 1975",
        "page": 5,
        "section": "6",
        "title": "Holding of abandoned property and its surrender, etc.",
        "chunk_id": 5
    }
}
```

Metadata is not embedded into the vector.

Instead:

```text
Chunk Text
    │
    ▼
Embedding Model
    │
    ▼
Vector
```

while the metadata remains associated with the original chunk.

This allows the system to identify the source after retrieval.

---

## 7. Embedding Model

### Model

`all-MiniLM-L6-v2`

The model was used through the `sentence-transformers` library.

Each chunk is converted into a **384-dimensional vector**.

Conceptually:

```text
Text Chunk
    ↓
all-MiniLM-L6-v2
    ↓
[0.021, -0.184, 0.073, ..., 0.112]
    ↓
384-dimensional vector
```

The same embedding model is used to embed the user's question during retrieval.

---

## 8. Vector Database

### FAISS

FAISS was selected for vector similarity search.

The index used was:

```python
faiss.IndexFlatL2(dimension)
```

### Why FAISS?

* Simple to implement.
* Fast similarity search.
* Works well for a relatively small document collection.
* Runs locally.
* Does not require an external database service.
* Suitable for learning and demonstrating the core RAG retrieval process.

The embeddings are stored in FAISS while the original chunks and their metadata remain in Python data structures.

---

## 9. Retrieval

When a user asks a question:

```text
User Question
      ↓
Embedding Model
      ↓
Question Vector
      ↓
FAISS Similarity Search
      ↓
Top-k Relevant Chunks
```

For example:

```text
Question:
"What happens if a person refuses to surrender abandoned property?"
```

The question is converted into a vector and compared against the stored chunk vectors.

The most relevant chunks are then retrieved.

---

## 10. Context Construction

The text from the retrieved dictionaries was extracted and joined together:

```python
context = "\n\n".join(
    chunk["text"]
    for chunk in retrieved_chunks
)
```

This context was then provided to the LLM.

Metadata was kept separately so that it could later be used for source citation.

---

## 11. LLM Generation

Qwen was used to generate the final answer.

The LLM receives:

```text
User Question
+
Retrieved Context
```

The goal is to instruct the model to answer using only the retrieved legal context.

The generation configuration included:

```python
with torch.no_grad():
    outputs = model.generate(
        **input,
        max_new_tokens=512,
        temperature=0.1
    )
```

A low temperature was used to encourage more deterministic responses.

---

## 12. Source Citation

The LLM is responsible for generating the answer, but it does **not** need to generate the source metadata itself.

The retrieved chunks already contain:

```text
Source
Page
Section
Title
Chunk ID
```

Therefore, the application can produce citations from the retrieved metadata.

Example:

```text
Answer:
According to Section 7, the Administrator may use necessary
force to take possession of abandoned property if the person
does not surrender it.

Source:
Abandoned Properties (Management) Act, 1975
Section 7, Page 5
```

This approach reduces the risk of the LLM inventing source information.

---

## Day 2 Results

The following components were successfully implemented:

* PDF ingestion
* Page-wise text extraction
* Text cleaning
* Contents removal
* Detection of 30 legal sections
* Section-aware chunking
* Recursive chunking for larger sections
* 1000-character target chunk size
* 150-character chunk overlap
* Chunk metadata
* `all-MiniLM-L6-v2` embeddings
* 384-dimensional vectors
* FAISS vector index
* Similarity-based retrieval
* Context construction
* Qwen-based answer generation
* Metadata-based source citation

---

## Key Findings

### 1. Document structure matters

Legal documents have meaningful sections. Preserving those sections before chunking provides more useful context than blindly splitting the entire document.

### 2. Smaller chunks are not always better

Very small chunks can lose important legal context. A balance between chunk size and contextual completeness is necessary.

### 3. Metadata is separate from embeddings

The embedding represents the semantic information of the chunk, while metadata provides information such as the source, page, and section.

### 4. Retrieval quality affects answer quality

The LLM can only generate a grounded answer if the relevant information is successfully retrieved.

### 5. FAISS is sufficient for the current dataset

For a small legal-document collection, FAISS provides a simple and efficient way to perform vector similarity search without introducing unnecessary infrastructure.

---

## Current Architecture

```text
                    ┌──────────────┐
                    │  Legal PDF   │
                    └──────┬───────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Text Extraction │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Text Cleaning   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Section Parsing │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Chunking        │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    Metadata     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ MiniLM Embedding│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │      FAISS      │
                  └────────┬────────┘
                           │
                           │
                    User Question
                           │
                           ▼
                  ┌─────────────────┐
                  │Question Embedding│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ FAISS Retrieval │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Retrieved Context│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │      Qwen       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Answer + Source │
                  └─────────────────┘
```

---

## Day 2 Conclusion

Day 2 focused on moving from theoretical RAG concepts to a working retrieval and generation pipeline using a real legal document.

The system can now ingest the **Abandoned Properties (Management) Act, 1975**, preserve its legal section structure, create searchable embeddings, retrieve relevant sections using FAISS, provide the retrieved context to Qwen, and associate the generated answer with source metadata.

The next stage will focus on **improving and evaluating the RAG system**, including retrieval quality, answer grounding, source citation, and potentially improving the user interaction layer.
