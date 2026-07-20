import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer


import streamlit as st

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

dimension = 384

INDEX_FILE = "database/faiss_index.bin"
DOC_FILE = "database/documents.pkl"


def store_chunks(chunks):

    print("✅ store_chunks started")

    if not chunks:
        raise ValueError("No text chunks found from PDF")


    os.makedirs("database", exist_ok=True)


    
    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True
    )


    
    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )


    
    if len(embeddings.shape) == 1:
        embeddings = embeddings.reshape(1, -1)


    print("Embedding shape:", embeddings.shape)


    
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)



    faiss.write_index(
        index,
        INDEX_FILE
    )



    with open(DOC_FILE, "wb") as f:
        pickle.dump(chunks, f)


    print("✅ Vector database created successfully")



def search_chunks(query, k=3):

    if not os.path.exists(INDEX_FILE):
        return []


    index = faiss.read_index(INDEX_FILE)


    with open(DOC_FILE, "rb") as f:
        documents = pickle.load(f)


    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )


    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )


    distances, indices = index.search(
        query_embedding,
        k
    )


    results = []

    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])


    return results