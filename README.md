# Pakistan Legal Documents RAG System

## Overview

This project is a Retrieval-Augmented Generation (RAG) system designed to answer questions from legal documents and PDFs obtained from the Pakistan Code website.

The user provides legal documents in PDF format, and the system processes these documents so that users can ask questions and receive answers based on the information available in the documents.

The main goal is to make it easier to search and understand large legal documents using natural language questions.

## How the System Works

The system follows this pipeline:

```text
Pakistan Code PDF
        ↓
   Text Extraction
        ↓
      Chunking
        ↓
    Embeddings
        ↓
   Vector Database
        ↓
    User Question
        ↓
 Question Embedding
        ↓
  Similarity Search
        ↓
 Relevant Legal Chunks
        ↓
        LLM
        ↓
    Final Answer
```

## Main Components

### 1. Legal PDF Documents

The system uses legal documents in PDF format obtained from the Pakistan Code website.

These documents may contain:

* Acts
* Ordinances
* Rules
* Regulations
* Other legal documents

The PDFs are provided as the knowledge source for the RAG system.

### 2. Text Extraction

The text is extracted from the uploaded PDF documents.

The extracted text is then prepared for further processing.

### 3. Chunking

Large legal documents are divided into smaller chunks.

Chunking is important because sending an entire legal document to an LLM at once is inefficient and can make retrieving the correct information difficult.

The project will experiment with different chunking approaches to find an effective method for legal documents.

### 4. Embeddings

Each text chunk is converted into a numerical vector using an embedding model.

The initial implementation uses:

```text
all-MiniLM-L6-v2
```

These vectors represent the semantic meaning of the legal text and allow similar questions and document sections to be matched.

### 5. Vector Search

The embeddings are stored in a vector search system.

The initial implementation uses:

```text
FAISS
```

ChromaDB will also be explored as a vector database during the project.

### 6. Retrieval

When the user asks a question, the question is converted into an embedding using the same embedding model.

The system searches the vector store and retrieves the most relevant sections of the legal documents.

### 7. Large Language Model

The retrieved legal context is provided to an LLM along with the user's question.

The project currently uses:

```text
Qwen
```

The LLM generates the answer based on the retrieved context.

### 8. Source Information

The system is intended to provide information about the source of the retrieved content, such as:

```text
Document: [Legal Document Name]
Page: [Page Number]
```

This helps users identify where the information used for the answer came from.

## Example

A user may upload a legal PDF and ask:

```text
What is the punishment for this offence?
```

The system will:

1. Convert the PDF into text.
2. Split the text into chunks.
3. Generate embeddings for the chunks.
4. Store the embeddings in the vector store.
5. Convert the user's question into an embedding.
6. Retrieve the most relevant legal sections.
7. Pass the retrieved sections and question to Qwen.
8. Generate an answer based on the retrieved legal text.
9. Provide the relevant source information.

## Technologies

* Python
* PyPDF
* Sentence Transformers
* FAISS
* ChromaDB
* Hugging Face Transformers
* Qwen
* PyTorch
* Google Colab
* Flask and React (Planned)

## Project Structure

```text
Pakistan-Code-RAG/
│
├── documents/
│   └── legal PDFs
│
├── notebooks/
│   └── RAG experiments
│
├── src/
│   ├── document_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retrieval.py
│   └── generation.py
│
├── app.py
├── requirements.txt
└── README.md
```

## Project Progress

* [x] PDF text extraction
* [x] Basic text chunking
* [x] Generate embeddings
* [x] FAISS vector search
* [x] Retrieve relevant document chunks
* [x] Qwen LLM integration
* [ ] Improve chunking for legal documents
* [ ] ChromaDB integration
* [ ] Store document metadata
* [ ] Add page/document references
* [ ] Improve retrieval quality
* [ ] Evaluate RAG responses
* [ ] Build user interface


## Important Note

This system is designed to retrieve and explain information from the provided legal documents.

The generated responses should not be considered a substitute for professional legal advice. Users should refer to the original legal documents for authoritative information.

## Goal

The goal of this project is to build a practical RAG system for searching and answering questions about Pakistani legal documents while maintaining a clear connection between generated answers and their original sources.
