import ollama
from modules.vec_store import search_chunks



def ask_llm(question):

    relevant_chunks = search_chunks(question)

    context = "\n\n".join(relevant_chunks)

    prompt = f"""

Answer ONLY from the provided study notes.

Study Notes:
{context}

Question:
{question}

If the answer is not present in the notes, say:
"I could not find this information in the uploaded notes."
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