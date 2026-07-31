# 🎓 ScholarAI – AI Powered Study Assistant

ScholarAI is a beginner-friendly AI-based educational web application developed to help students study their notes more efficiently.

The application allows students to upload PDF study material and interact with it using AI. It can extract text from notes, create summaries, generate quizzes, answer questions from the uploaded material, and also accept voice-based questions.

The project was developed as a college project to gain practical experience with Artificial Intelligence, Natural Language Processing, embeddings, vector databases, and Large Language Models.

---

## 📌 Problem Statement

Students often have to read through long PDF notes and study materials to find specific information. Preparing summaries and revision questions manually can also take a lot of time.

ScholarAI aims to make this process easier by allowing students to upload their study material and use AI to interact with it.

---

## ✨ Features

- 📄 Upload PDF study notes
- 🔍 Extract text from PDF files
- ✂️ Split extracted text into smaller chunks
- 🧠 Generate embeddings for document chunks
- 🗄️ Store and search document embeddings using ChromaDB
- 💬 Ask questions from uploaded notes
- 🤖 Generate answers using a local LLM
- 📝 Generate AI-based summaries
- ❓ Generate multiple-choice quizzes
- 🎤 Ask questions using voice input
- 📚 Retrieve relevant information from uploaded documents
- 💻 Simple Streamlit-based interface
- 🔒 Local AI model support using Ollama

---

## 🛠️ Technologies Used

### Frontend / User Interface

- **Streamlit**
  - Used to create the web interface.
  - Provides PDF upload, question answering, summary, quiz and voice interaction features.

### Programming Language

- **Python**
  - Main programming language used for the project.

### PDF Processing

- **PyMuPDF (fitz)**
  - Used to extract text from PDF documents.

### Natural Language Processing

- **NLP**
  - Used for basic text cleaning and document chunking.

### Embeddings

- **Sentence Transformers**
- **all-MiniLM-L6-v2**

These are used to convert text chunks into numerical vector representations.

### Vector Database

- **ChromaDB**

Used to store document embeddings and retrieve relevant chunks using semantic similarity.

### AI / LLM

- **Ollama**
- **Llama 3.2**

Ollama is used to run the AI model locally for question answering, summarization and quiz generation.

### LangChain

LangChain is used for:

- Prompt handling
- Text splitting
- Document processing
- Connecting different AI components

### Voice Input

- **SpeechRecognition**

Used to convert spoken questions into text.

### Development Tools

- Visual Studio Code
- Python Virtual Environment (`venv`)
- Git / GitHub

---

## 🧠 How ScholarAI Works

The basic workflow of ScholarAI is:

            Upload PDF
                ↓
        PDF Text Extraction
                ↓
          Text Cleaning
                ↓
          Text Chunking
                ↓
       Generate Embeddings
                ↓
            ChromaDB
                ↓
       Semantic Search / Retrieval
                ↓
       Relevant Note Chunks
                ↓
          Ollama LLM
                ↓
          AI Generated Answer
