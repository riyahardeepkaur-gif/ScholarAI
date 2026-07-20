# 🎓 ScholarAI - AI Powered Learning Assistant

ScholarAI is an AI-powered learning assistant that helps students understand their study materials faster. It allows users to upload PDF notes, ask questions, generate summaries, and create quizzes using Artificial Intelligence.

The project uses **Retrieval-Augmented Generation (RAG)** to provide answers based on the user's uploaded study material instead of generating unrelated responses.

---

## 🚀 Problem Statement

Students often spend a lot of time searching through lengthy PDFs and notes to find important information. Manually reading and revising large study materials can be time-consuming and inefficient.

ScholarAI solves this problem by transforming static study documents into an interactive AI learning companion.

---

## ✨ Features

### 📄 PDF Understanding

* Upload study notes in PDF format
* Extract and process document content
* Convert documents into searchable knowledge

### 💬 AI Question Answering

* Ask questions directly from uploaded notes
* Get context-based answers using RAG
* Reduces the time needed to search through documents

### 📝 AI Summary Generation

* Generate quick summaries from study materials
* Helps students with faster revision

### ❓ AI Quiz Generation

* Automatically creates multiple-choice questions
* Allows students to test their understanding

### 🔍 Semantic Search

* Uses vector embeddings to find relevant information
* Provides better results than simple keyword matching

---

## 🧠 How It Works

```
PDF Upload
     |
     ↓
Text Extraction (PyMuPDF)
     |
     ↓
Text Chunking
     |
     ↓
Sentence Transformer Embeddings
     |
     ↓
FAISS Vector Search
     |
     ↓
Llama 3.2 LLM (Ollama)
     |
     ↓
Answer / Summary / Quiz
```

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Frontend

* Streamlit

### AI & Machine Learning

* Ollama
* Llama 3.2
* Sentence Transformers

### Database / Search

* FAISS Vector Index

### Document Processing

* PyMuPDF

### Libraries

* NumPy
* JSON
* Pickle

---

## 📂 Project Structure

```
ScholarAI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── llm.py
│   ├── pdf_processor.py
│   ├── vec_store.py
│   ├── summarizer.py
│   └── quiz_generator.py
│
└── database/
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone <repository-url>
```

### 2. Create virtual environment

```
python -m venv .venv
```

Activate environment:

Windows:

```
.venv\Scripts\activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Install Ollama

Download and install Ollama, then run:

```
ollama pull llama3.2:3b
```

---

### 5. Run Application

```
streamlit run app.py
```

---

## 🎯 Challenges Solved

* Building a complete RAG pipeline connecting documents, embeddings, vector search, and LLMs
* Handling PDF extraction and document processing
* Managing FAISS vector storage and similarity search
* Creating structured AI-generated quizzes
* Optimizing performance for local LLM execution

---

## 🔮 Future Improvements

* OCR support for scanned handwritten notes
* Voice-based AI learning assistant
* Multi-document support
* User accounts and learning progress tracking
* Flashcard generation
* Cloud deployment

---

## 🌟 Impact

ScholarAI makes learning more efficient by helping students quickly understand, revise, and interact with their study materials through AI.

---

## 👩‍💻 Built With

Built as part of **CodeStorm 2026 - FutureForge Hackathon**.
