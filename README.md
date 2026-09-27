# Final Day — Modular RAG Application & Flask Integration

## Overview

On the final day, the RAG pipeline developed and tested in Google Colab was converted into a **modular application in VS Code**.

The main focus was on moving from a notebook-based RAG prototype to a structured application that can be executed as a complete pipeline through a Flask backend and a browser-based frontend.

The existing RAG components were separated into reusable modules for document processing, chunking, embeddings, vector search, retrieval, and answer generation.

The original Qwen model implementation using Hugging Face Transformers was also replaced with **Qwen running through Ollama** because loading and running the model directly through Transformers resulted in high latency on the available CPU-based environment.

---

# Final Day Objectives

The main objectives were to:

1. Convert the Colab RAG pipeline into a modular VS Code project.
2. Separate RAG functionality into reusable Python modules.
3. Create helper functions for document processing and retrieval.
4. Integrate the existing FAISS-based retrieval pipeline.
5. Replace direct Transformers-based Qwen inference with Ollama.
6. Reduce model-loading overhead during multiple questions.
7. Create a Flask backend for the RAG application.
8. Create a browser-based frontend using HTML, CSS, and JavaScript.
9. Connect the frontend question form with the Flask API.
10. Return generated answers and source information to the frontend.
11. Test the complete RAG workflow through the web application.

---

# From Colab Prototype to Application

The initial RAG pipeline was developed and tested in Google Colab.

The pipeline was then converted into a modular VS Code implementation.

### Colab Prototype

```text
PDF
 │
 ▼
Preprocessing
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
FAISS
 │
 ▼
Retrieval
 │
 ▼
Qwen
 │
 ▼
Answer
```

### Modular VS Code Application

```text
                    ┌──────────────────┐
                    │   Web Frontend   │
                    │ HTML/CSS/JavaScript│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Flask Backend  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   RAG Pipeline   │
                    └────────┬─────────┘
                             │
             ┌───────────────┼────────────────┐
             ▼               ▼                ▼
       Document          Retrieval         Generation
       Processing           │                │
             │              ▼                ▼
             │            FAISS           Ollama
             │                               │
             │                               ▼
             │                          Qwen 2.5 3B
             │
             └───────────────┬────────────────┘
                             ▼
                          Answer
                             │
                             ▼
                       Flask Response
                             │
                             ▼
                         Frontend
```

---

# 1. Modular Project Structure

Instead of keeping the complete RAG workflow inside a single notebook or Python file, the functionality was separated into modular components.

A simplified structure is:

```text
RAG Project/
│
├── app.py
│
├── config/
│   └── config.py
│
├── helpers/
│   ├── document_loader.py
│   ├── text_cleaner.py
│   ├── section_parser.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── generator.py
│
├── data/
│   └── legal_document.pdf
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── requirements.txt
```

The exact modules may vary, but the main objective was to separate individual responsibilities rather than maintaining one large script.

---

# 2. Reusing the RAG Pipeline

The logic developed during the earlier stages was reused in the modular application.

The pipeline continues to perform:

```text
PDF Loading
     ↓
Text Cleaning
     ↓
Section Detection
     ↓
Section-Aware Chunking
     ↓
Metadata
     ↓
Embeddings
     ↓
FAISS
     ↓
Retrieval
     ↓
Context Construction
     ↓
LLM Generation
```

This allowed the work completed in Colab to become the foundation of the final application instead of rebuilding the RAG system from scratch.

---

# 3. Qwen Model Migration

## Previous Approach

Initially, Qwen was loaded directly using Hugging Face Transformers:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
```

The model was loaded and used directly for text generation.

However, loading the model through Transformers on the available CPU environment introduced significant latency.

A major issue was that model loading could occur whenever an answer was requested, resulting in an inefficient workflow:

```text
Question 1
   ↓
Load Qwen
   ↓
Generate Answer

Question 2
   ↓
Load Qwen again
   ↓
Generate Answer
```

This made interactive usage slow.

---

# 4. Ollama Integration

To improve the local inference workflow, Qwen was moved to **Ollama**.

The Qwen model was downloaded and managed by Ollama rather than being loaded directly through Transformers.

The Python application communicates with the local Ollama server using the Python `ollama` client.

Example:

```python
import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    options={
        "temperature": 0.2,
        "num_predict": 200
    }
)
```

The generated response is then extracted from:

```python
response["message"]["content"]
```

---

# 5. Why Ollama Was Used

Ollama was selected primarily because of the latency experienced with direct Transformers-based inference on CPU.

The new architecture separates model serving from the Flask application's Python process:

```text
Flask Application
       │
       │ ollama.chat()
       ▼
Ollama Server
       │
       ▼
Qwen 2.5 3B
```

This means the Flask application no longer needs to manually initialize the Qwen tokenizer and model.

It also avoids repeatedly loading the model through `AutoModelForCausalLM` for each user request.

---

# 6. Generation Pipeline

The final generation process is:

```text
User Question
      │
      ▼
Question Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
Context Construction
      │
      ▼
Legal Prompt
      │
      ▼
Ollama
      │
      ▼
Qwen 2.5 3B
      │
      ▼
Generated Answer
```

The prompt instructs Qwen to:

* Use only the retrieved context.
* Avoid making up information.
* State when the requested information is not available.
* Answer as a legal document assistant.

---

# 7. Flask Backend

A Flask backend was created to expose the RAG pipeline through an HTTP API.

The backend is responsible for:

1. Receiving the user's question.
2. Passing the question to the RAG pipeline.
3. Performing retrieval.
4. Constructing the context.
5. Calling Qwen through Ollama.
6. Returning the generated answer.
7. Returning relevant source metadata.

The basic application flow is:

```text
Browser
   │
   │ POST /ask
   ▼
Flask
   │
   ▼
RAG Pipeline
   │
   ├── Embedding
   ├── FAISS Retrieval
   ├── Context Construction
   └── Ollama / Qwen
   │
   ▼
JSON Response
   │
   ▼
Browser
```

---

# 8. Frontend

A simple browser interface was created using:

* HTML
* CSS
* JavaScript

The frontend provides a question input and an **Ask Question** button.

The JavaScript sends the question to the Flask backend and receives the generated response.

Conceptually:

```text
User enters question
        │
        ▼
Ask Question
        │
        ▼
JavaScript fetch()
        │
        ▼
Flask /ask endpoint
        │
        ▼
RAG + Qwen
        │
        ▼
JSON response
        │
        ▼
JavaScript
        │
        ▼
Display answer
```

---

# 9. Source Information

The existing metadata-based citation approach was retained.

Retrieved chunks contain information such as:

```text
Source
Page
Section
Title
Chunk ID
```

The LLM generates the answer from the retrieved context, while the application can use the retrieved metadata to display the source.

Example:

```text
Answer:
The Administrator may take necessary measures to
secure and manage abandoned property.

Source:
Abandoned Properties (Management) Act, 1975
Section 16
Page 7
```

Keeping source information separate from the generated answer reduces the possibility of the LLM inventing page or section information.

---

# 10. Final RAG Architecture

The final system can be represented as:

```text
                         ┌─────────────────────┐
                         │   Abandoned         │
                         │   Properties Act    │
                         │       PDF           │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Document Processing │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Section Detection   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Chunking       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Embeddings       │
                         │ all-MiniLM-L6-v2    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       FAISS         │
                         └──────────┬──────────┘
                                    │
                                    │
                         ┌──────────▼──────────┐
                         │    User Question    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Question Embedding  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Similarity Search   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Relevant Chunks    │
                         │    + Metadata       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Context + Question  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Ollama         │
                         │    Qwen 2.5 3B      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Answer + Sources    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Flask Backend    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ HTML/CSS/JavaScript │
                         │      Frontend       │
                         └─────────────────────┘
```

---

# Final Day Results

The following components were implemented:

* Modular RAG pipeline in VS Code
* Reusable helper modules
* Legal document preprocessing
* Section-aware chunking
* Metadata preservation
* `all-MiniLM-L6-v2` embeddings
* FAISS vector search
* Similarity-based retrieval
* Context construction
* Qwen 2.5 3B integration
* Ollama-based local model serving
* Replacement of direct Transformers inference
* Flask backend
* HTML frontend
* CSS styling
* JavaScript frontend-backend communication
* Source metadata handling
* End-to-end RAG application structure

---

# Issues Encountered

During the final integration, several issues were identified and addressed during development.

### 1. High Qwen inference latency

The initial Transformers implementation was slow on CPU and introduced significant delay during generation.

**Solution:**

Qwen was moved to Ollama to provide a separate local model-serving layer and avoid repeatedly loading the model directly inside the Python application.

### 2. Model loading on every question

The initial implementation called the model-loading function from the answer-generation function.

This meant that each question could trigger model initialization again.

The generation code was redesigned so that Flask communicates with the already-running Ollama service instead of directly loading the Transformers model.

### 3. Frontend not displaying responses

During frontend integration, clicking the **Ask Question** button did not immediately display a response in the browser.

This required debugging the communication between:

```text
JavaScript
    ↓
Flask API
    ↓
RAG Pipeline
    ↓
Ollama
    ↓
Qwen
```

The frontend and backend were therefore treated as separate components during debugging to identify where the request/response flow was stopping.

### 4. CPU-based inference limitations

Since inference was performed locally on CPU, response generation can still take noticeable time depending on the retrieved context and model workload.

This highlighted the importance of efficient model serving and frontend feedback during generation.

---

# Key Findings

### 1. Modularization improves maintainability

Separating the RAG pipeline into individual modules makes the system easier to understand, test, debug, and extend.

### 2. Notebook code can be converted into reusable application components

The Colab prototype provided the foundation for the final application. The same RAG concepts were reorganized into reusable helper functions and backend components.

### 3. Model serving affects application performance

The choice of how an LLM is loaded and served can significantly affect response latency, especially on CPU-based systems.

### 4. Ollama simplifies local LLM integration

Using Ollama allowed the application to communicate with Qwen through a local API instead of manually handling tokenizer and model initialization inside the Flask application.

### 5. Backend and frontend integration introduces additional failure points

A RAG pipeline can work correctly in isolation while the web application still fails to display the result. Therefore, the complete system needs to be tested across the entire request-response chain.

### 6. Retrieval remains critical

Changing the LLM does not solve poor retrieval. The quality of the final answer still depends heavily on whether the correct legal sections are retrieved from FAISS.

---

# Final Project Architecture

The final application consists of three major layers:

```text
┌─────────────────────────────────────────┐
│              Frontend                   │
│        HTML + CSS + JavaScript          │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│              Backend                    │
│                 Flask                   │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│              RAG Layer                  │
│                                         │
│  Chunking → Embeddings → FAISS          │
│  → Retrieval → Context Construction     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│           Local LLM Layer               │
│                                         │
│             Ollama                     │
│          Qwen 2.5 3B                   │
└─────────────────────────────────────────┘
```

---

# Final Conclusion

The final day focused on converting the RAG pipeline developed during the earlier stages into a more structured and usable application.

The **Abandoned Properties (Management) Act, 1975** is processed into section-aware chunks, embedded using `all-MiniLM-L6-v2`, indexed using FAISS, and retrieved based on semantic similarity.

The retrieved legal context is passed to **Qwen 2.5 3B through Ollama**, replacing the slower direct Transformers implementation.

The RAG pipeline was then integrated with a **Flask backend** and a **HTML/CSS/JavaScript frontend**, creating the foundation of a complete local legal-document question-answering application.

The project demonstrated the complete flow from:

```text
Legal Document
      ↓
Preprocessing
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector Database
      ↓
Retrieval
      ↓
Context
      ↓
Local LLM
      ↓
Flask API
      ↓
Web Interface
      ↓
Grounded Answer + Source
```

This completed the transition from a RAG experimentation notebook to a modular application architecture suitable for further improvement and evaluation.
