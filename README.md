# Day 1 — RAG Pipeline Exploration

## Overview

This branch contains the Day 1 work for the Retrieval-Augmented Generation (RAG) project.

The goal of Day 1 was to understand and implement the basic RAG pipeline from document processing to answer generation.

A simple **Machine Learning Basics PDF** was used as a test document to explore the complete pipeline before working with the actual legal documents from Pakistan Code.

---

## What Was Implemented

The following RAG pipeline was implemented:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Vector Search
 ↓
Relevant Chunks
 ↓
Qwen LLM
 ↓
Generated Answer
```

---

## 1. PDF Text Extraction

A sample Machine Learning Basics PDF was used.

The PDF text was extracted and prepared for further processing.

The sample document contained topics such as:

* Machine Learning
* Supervised Learning
* Unsupervised Learning
* Reinforcement Learning
* Classification
* Regression
* Clustering

The PDF was used only as a test document for learning the RAG workflow.

---

## 2. Text Chunking

The extracted text was divided into smaller chunks.

A basic character-based chunking approach was used for the initial implementation.

The purpose was to understand:

* Why documents need to be chunked
* How chunk size affects retrieval
* How chunks are later converted into embeddings

---

## 3. Text Embeddings

The chunks were converted into numerical vectors using the Sentence Transformers library.

Embedding model used:

```text
all-MiniLM-L6-v2
```

The model generates **384-dimensional embeddings**.

For example:

```text
Number of chunks = 100
Embedding dimension = 384

Embedding matrix:
(100, 384)
```

This means each chunk is represented by a vector containing 384 numerical values.

---

## 4. FAISS Vector Search

FAISS was used for storing and searching the chunk embeddings.

The following index was used:

```python
faiss.IndexFlatL2(dimension)
```

`IndexFlatL2` performs an exact similarity search using **L2 (Euclidean) distance**.

The embeddings were added to the FAISS index:

```python
index.add(chunk_embeddings)
```

When a user asks a question:

1. The question is converted into an embedding.
2. FAISS compares the question vector with the stored chunk vectors.
3. The most similar chunks are retrieved.

Example:

```text
User Question
      ↓
Question Embedding
      ↓
FAISS Search
      ↓
Top K Relevant Chunks
```

---

## 5. Retrieval Testing

Several questions were tested against the sample document.

Example:

```text
What is supervised learning?
```

The system successfully retrieved chunks containing information about supervised learning.

Questions unrelated to the document were also tested to observe how the system behaves when the required information is not available in the knowledge base.

---

## 6. Qwen LLM Integration

The retrieved chunks were passed to a Qwen language model to generate the final answer.

Model used:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

The LLM receives:

```text
Retrieved Context
+
User Question
```

through a prompt such as:

```text
Answer the question using ONLY the provided context.

Context:
[Retrieved chunks]

Question:
[User question]

Answer:
```

This allows the LLM to generate an answer based on the retrieved document information.

---

## 7. Tokenization and Generation

The Qwen tokenizer converts the prompt into token IDs that can be processed by the model.

The general flow is:

```text
Prompt
 ↓
Tokenizer
 ↓
Token IDs
 ↓
Qwen
 ↓
Generated Token IDs
 ↓
Tokenizer
 ↓
Text Answer
```

Only the newly generated tokens are decoded so that the final output contains the answer rather than the original prompt.

---

## Testing

The RAG pipeline was tested with questions such as:

```text
What is machine learning?

What is supervised learning?

What is unsupervised learning?

What is the difference between classification and regression?

What is an example of clustering?

What is a convolutional neural network?
```

The first questions can be answered using information from the sample PDF.

The last question is not covered by the sample document and was used to test the system's behavior when the required information is not present in the retrieved context.

---

## Technologies Used

* Python
* Google Colab
* PyPDF
* Sentence Transformers
* FAISS
* Hugging Face Transformers
* Qwen
* PyTorch
* NumPy

---

## Files in This Branch

```text
Day-1/
│
├── RAG.ipynb
├── requirements.txt
└── README.md
```

### `RAG.ipynb`

Contains the complete Day 1 implementation, including:

* PDF text extraction
* Chunking
* Embedding generation
* FAISS index creation
* Similarity search
* Retrieval
* Qwen model loading
* Prompt creation
* Answer generation
* RAG testing

### `requirements.txt`

Contains the Python dependencies required to run the notebook.

```text
pypdf
sentence-transformers
faiss-cpu
transformers
accelerate
torch
numpy
```

---

## Result

By the end of Day 1, a basic end-to-end RAG pipeline was successfully implemented:

```text
Document
   ↓
Chunks
   ↓
Embeddings
   ↓
FAISS
   ↓
Retrieval
   ↓
Qwen
   ↓
Answer
```

This implementation serves as the foundation for the next stage, where the pipeline can be tested with actual legal documents from Pakistan Code and improved with better chunking, metadata, retrieval, and source tracking.
