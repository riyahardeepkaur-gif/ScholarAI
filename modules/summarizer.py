
import streamlit as st
import ollama


@st.cache_data(show_spinner=False)
def generate_summary(chunks):

    
    context = "\n\n".join(chunks[:2])

    prompt = f"""
Summarize these study notes.

Requirements:
- Topic Overview
- Key Points
- Important Concepts
- Keep it under 150 words.
- Use bullet points.
- Answer only from the notes.

Notes:
{context}
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]