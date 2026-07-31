import os
import shutil
from typing import List, Dict, Any
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from modules.utils import DB_DIR

import streamlit as st

@st.cache_resource
def get_embeddings_model():
    """
    Load the sentence transformer model lazily and cache it using st.cache_resource.
    Uses 'all-MiniLM-L6-v2' which is fast, lightweight, and perfect for CPU/local running.
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@st.cache_resource
def get_vector_store() -> Chroma:
    """
    Returns a cached instance of the Chroma vector store.
    """
    try:
        embeddings = get_embeddings_model()
        return Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings
        )
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        return None

def add_pdf_chunks(chunks: List[Dict[str, Any]], filename: str) -> bool:
    """
    Converts chunk dictionaries into LangChain Document objects and adds them to ChromaDB.
    """
    try:
        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk["text"],
                metadata={
                    "source": filename,
                    "page_num": chunk["metadata"]["page_num"],
                    "chunk_id": chunk["metadata"]["chunk_id"]
                }
            )
            documents.append(doc)
            
        vector_store = get_vector_store()
        if vector_store is None:
            return False
        vector_store.add_documents(documents)
        return True
    except Exception as e:
        print(f"Error adding chunks to vector store: {e}")
        return False

def search_relevant_chunks(query: str, filename: str = None, k: int = 3) -> List[Document]:
    """
    Searches ChromaDB for the top k chunks matching the query (default k=3).
    If a filename is specified, filters results to only include chunks from that document.
    """
    try:
        vector_store = get_vector_store()
        if vector_store is None:
            return []
        
        # Define search filters if filename is provided
        search_filter = None
        if filename:
            search_filter = {"source": filename}
            
        # Perform similarity search
        results = vector_store.similarity_search(query, k=k, filter=search_filter)
        return results
    except Exception as e:
        print(f"Error searching vector store: {e}")
        return []

def get_all_uploaded_files() -> List[str]:
    """
    Scrapes the unique document sources stored in the vector database metadata.
    """
    try:
        vector_store = get_vector_store()
        if vector_store is None:
            return []
        # Access the underlying database collection to get all metadata
        collection = vector_store._collection
        metadata_list = collection.get(include=["metadatas"])["metadatas"]
        
        if not metadata_list:
            return []
            
        # Get unique source filenames
        unique_files = set()
        for meta in metadata_list:
            if meta and "source" in meta:
                unique_files.add(meta["source"])
                
        return sorted(list(unique_files))
    except Exception as e:
        print(f"Error getting files: {e}")
        return []

def clear_vector_store() -> bool:
    """
    Deletes the current database collection data natively.
    Falls back to clearing the directory if native deletion fails.
    Clears the cached streamlit resource for the database.
    """
    success = False
    try:
        # Attempt native database collection deletion first
        vector_store = get_vector_store()
        if vector_store is not None:
            vector_store.delete_collection()
            success = True
    except Exception as e:
        print(f"Error clearing database collection natively: {e}. Falling back to directory removal...")
        
    if not success:
        try:
            if os.path.exists(DB_DIR):
                shutil.rmtree(DB_DIR)
            os.makedirs(DB_DIR, exist_ok=True)
            success = True
        except Exception as e2:
            print(f"Error deleting database directory: {e2}")
            success = False
            
    # Clear the cached get_vector_store resource
    try:
        get_vector_store.clear()
    except Exception as e:
        print(f"Error clearing vector store cache: {e}")
        
    return success
