# RAG System for The Abandoned Properties (Management) Act, 1975

## 1. Introduction and Problem Statement

Legal documents can be difficult to search because they contain a lot of information divided into different sections and clauses. Finding the answer to a specific question manually can take a lot of time.

For this project, we built a **Retrieval-Augmented Generation (RAG)** system using **The Abandoned Properties (Management) Act, 1975**.

The main goal of the system is to allow a user to ask questions about the Act in normal language and receive an answer based on the actual content of the document.

For example, a user can ask:

> "What can the Administrator do if a person refuses to surrender abandoned property?"

Instead of asking the LLM to answer from its own knowledge, our system first searches the Act for relevant information. The retrieved information is then given to the LLM, which generates the final answer.

The system also provides the source information, such as the relevant section and page, so that the user can understand where the answer came from.

### Main steps of our system

1. Load the legal PDF.
2. Extract the text.
3. Identify and preserve section information.
4. Split the document into smaller chunks.
5. Generate embeddings for the chunks.
6. Store the embeddings in ChromaDB.
7. Convert the user's question into an embedding.
8. Retrieve relevant chunks.
9. Use a Cross-Encoder reranker to improve the retrieved results.
10. Send the strongest sources to the Qwen LLM.
11. Generate the final answer with source information.

---

# 2. Which LLM Did We Choose?

## Qwen 2.5:3B using Ollama

Initially, we experimented with the **Qwen model using the Transformers library**. Later, we switched to **Qwen 2.5:3B running through Ollama**.

### Why did we choose Qwen 2.5:3B?

We selected Qwen 2.5:3B because:

* It is relatively small and lightweight.
* It can run locally using Ollama.
* It does not require sending our legal document to an external API.
* It does not require a paid API key.
* It is suitable for generating answers from retrieved context.
* It is fast enough for our RAG application.

Using Ollama also made the setup easier because the model could be downloaded and run locally.

In our system, the LLM is responsible for **generating the final answer**. It does not directly search the legal document. The retrieval system finds the relevant information first and then passes it to Qwen.

---

# 3. Which Embedding Model Did We Choose?

## all-MiniLM-L6-v2

For creating embeddings, we used the **all-MiniLM-L6-v2** model from Sentence Transformers.

An embedding converts text into numbers called a **vector**. These vectors represent the meaning of the text.

For example, the document may contain:

> "The Administrator may use such force as is necessary for taking possession of such property."

A user might ask:

> "Can the Administrator forcefully take abandoned property?"

Even though the wording is different, the embedding model can understand that the two pieces of text are semantically related.

### Why did we choose all-MiniLM-L6-v2?

We selected this model because:

* It is free to use.
* It can run locally.
* It is lightweight and fast.
* It works well for semantic search.
* It produces 384-dimensional embeddings.
* It does not require an external API.
* It is suitable for a small legal-document dataset.

The same embedding model is used for both the document chunks and the user's questions so that they can be compared in the same vector space.

---

# 4. Which Vector Database Did We Choose?

## ChromaDB

We used **ChromaDB** as our vector database.

After the document is divided into chunks, each chunk is converted into an embedding and stored in ChromaDB along with its metadata.

The metadata includes information such as:

* Section
* Title
* Page
* Source

### Why did we choose ChromaDB?

We selected ChromaDB because:

* It is easy to use with Python.
* It is designed for storing and searching embeddings.
* It works well with RAG applications.
* It supports metadata.
* It provides persistent storage.
* We can save the vector database to disk instead of rebuilding it every time.
* It is lightweight and suitable for our project.

### Why was persistence important?

Without persistent storage, the embeddings would have to be generated again every time the application starts.

With ChromaDB persistence, the generated embeddings can be stored on disk and reused later.

This makes the application faster and avoids unnecessary reprocessing of the legal document.

---

# 5. Chunk Size and Chunking Strategy

## RecursiveCharacterTextSplitter

We used **RecursiveCharacterTextSplitter** for chunking.

Chunking means dividing a large document into smaller pieces so that the retrieval system can find the most relevant information.

Our configuration was:

* **Chunk Size:** 1000 characters
* **Chunk Overlap:** 150 characters

### Why did we use a chunk size of 1000?

A chunk size of 1000 provides enough information for the model to understand the context while keeping the chunks small enough for accurate retrieval.

If the chunks were too small, important context could be lost.

If the chunks were too large, they could contain too much unrelated information, making retrieval less accurate.

Therefore, 1000 characters provided a reasonable balance between context and retrieval accuracy for our document.

### Why did we use 150 overlap?

The overlap means that the end of one chunk is repeated at the beginning of the next chunk.

For example:

```text
Chunk 1:
A B C D E F G H I J

Chunk 2:
I J K L M N O P Q R
```

Here, `I J` appears in both chunks.

This helps prevent important information from being lost when a sentence or idea falls near the boundary between two chunks.

### Section-aware chunking

Before chunking, we also preserved the legal section information.

For example:

```text
Section: 7
Title: Power of Administrator to take possession
Page: 5
```

This information is stored as metadata with the chunk.

This is especially useful for a legal RAG system because we can tell the user exactly which section and page were used.

---

# 6. Reranking Using Cross-Encoder

After the initial retrieval from ChromaDB, we added a **Cross-Encoder reranker**.

The purpose of the reranker is to improve the order of the retrieved results.

### Why do we need reranking?

The embedding search retrieves chunks that are generally similar to the question.

However, the first retrieved chunk is not always the most useful one.

The Cross-Encoder looks at the **question and retrieved chunk together** and calculates a relevance score.

The results can then be sorted according to these scores.

The process is:

```text
User Question
      ↓
Embedding
      ↓
ChromaDB
      ↓
Initial Retrieved Chunks
      ↓
Cross-Encoder
      ↓
Reranked Chunks
      ↓
Strongest Sources
      ↓
Qwen 2.5:3B
      ↓
Final Answer
```

This additional step helps improve retrieval quality before the information is sent to the LLM.

We also added a check for weak retrieval results. If the retrieved results do not contain a sufficiently strong source, the system can return:

> "No Strong Source Available"

instead of generating an answer based on weak or irrelevant information.

---

# 7. Architecture Diagram

The complete architecture of our RAG system is:

```text
                 ┌──────────────────────────┐
                 │  Abandoned Properties    │
                 │      Act PDF             │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     Text Extraction      │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Section-aware Processing │
                 │ + Metadata               │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ RecursiveCharacter       │
                 │ TextSplitter             │
                 │                          │
                 │ Chunk Size: 1000         │
                 │ Overlap: 150             │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ all-MiniLM-L6-v2         │
                 │ Embedding Model          │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │       ChromaDB           │
                 │   Persistent Vector DB   │
                 └──────────────────────────┘


              USER ASKS A QUESTION
                       │
                       ▼
             ┌──────────────────────┐
             │ Query Embedding      │
             │ all-MiniLM-L6-v2     │
             └──────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │      ChromaDB        │
             │ Retrieve Candidates  │
             └──────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ Cross-Encoder        │
             │ Reranker             │
             └──────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ Strong Sources       │
             │ Section + Page       │
             └──────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ Qwen 2.5:3B          │
             │ Ollama                │
             └──────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ Final Answer +        │
             │ Source Information    │
             └──────────────────────┘
```

---

# 8. Findings and Results

After implementing the complete RAG pipeline, we found that the system was able to answer questions about the legal document using the information retrieved from the Act.

### 8.1 Better than simple keyword search

The embedding-based retrieval allowed the system to find relevant information even when the user's wording was different from the wording used in the Act.

For example, a user can ask about the Administrator's ability to take possession of property without using the exact wording from Section 7.

The semantic search can still retrieve the relevant section.

### 8.2 Section and page information improved source tracking

Keeping section and page metadata with every chunk made it easier to identify where the retrieved information came from.

The system can provide information such as:

```text
Section: 7
Title: Power of Administrator to take possession
Page: 5
```

This is particularly useful for legal documents because users can verify the answer against the original Act.

### 8.3 Reranking improved retrieval

The Cross-Encoder reranker provided an additional relevance check after the initial ChromaDB retrieval.

Instead of directly sending all retrieved chunks to the LLM, the system first evaluates their relevance and selects the stronger sources.

This helps reduce the possibility of giving the LLM unrelated context.

### 8.4 Persistent vector storage improved efficiency

Using ChromaDB with persistent storage meant that embeddings did not need to be generated again every time the application started.

Once the document was processed and stored, the existing vector database could be reused.

### 8.5 Source filtering improved reliability

The system does not blindly generate an answer for every question.

If the retrieved sources are not strong enough, the system can return:

> "No Strong Source Available"

This is useful because generating an answer from irrelevant sources can lead to incorrect information, especially in a legal application.

### 8.6 Overall Result

The complete pipeline successfully demonstrated the main RAG workflow:

```text
Document
   ↓
Chunking
   ↓
Embeddings
   ↓
ChromaDB
   ↓
Retrieval
   ↓
Cross-Encoder Reranking
   ↓
Relevant Context
   ↓
Qwen 2.5:3B
   ↓
Grounded Answer
```

The project showed that RAG can be effectively used to build a question-answering system for a specific legal document.

---

# 9. Conclusion

In this project, we developed a RAG system for **The Abandoned Properties (Management) Act, 1975**.

The system combines several components, where each component has a specific role.

**RecursiveCharacterTextSplitter** was used to divide the document into manageable chunks with a chunk size of **1000 characters** and an overlap of **150 characters**.

**all-MiniLM-L6-v2** was used to convert the chunks and user questions into embeddings.

**ChromaDB** was used as the vector database because it supports efficient similarity search and persistent storage.

A **Cross-Encoder reranker** was added to improve the relevance of the retrieved chunks before sending them to the LLM.

Finally, **Qwen 2.5:3B through Ollama** was used to generate the final answer based on the retrieved legal context.

The system also keeps source metadata such as section, title, page, and source, allowing users to understand where the answer came from.

Overall, the project helped demonstrate how RAG can be used to build a legal question-answering system that is more grounded in the source document. Instead of relying only on the LLM's existing knowledge, the system retrieves relevant information from the actual legal document and uses that information to generate the answer.

This approach can be further improved in the future by testing different embedding models, chunk sizes, reranking models, retrieval strategies, and LLMs to achieve better accuracy and reliability.
