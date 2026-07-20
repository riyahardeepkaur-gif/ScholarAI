import streamlit as st
from modules.llm import ask_llm
from modules.pdf_processor import chunk_text
from modules.pdf_processor import extract_text_from_pdf
from modules.vec_store import store_chunks
from modules.summarizer import generate_summary
from modules.quiz_generator import generate_quiz

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="ScholarAI", page_icon="🎓", layout="wide")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🎓 ScholarAI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📄 Upload Notes",
        "💬 Ask Questions",
        "📝 Summary",
        "❓ Quiz",
        "ℹ️ About",
    ],
)

# -----------------------------
# Home Page
# ----------------------------- 
if page == "🏠 Home":

    st.title("🎓 ScholarAI")

    st.subheader("Your AI-Powered Learning Companion")

    st.markdown("---")

    st.write("""
Welcome to ScholarAI!

This application helps students:

✅ Understand PDFs

✅ Ask AI Questions

✅ Generate Summaries

✅ Generate Quiz Questions

Built using Artificial Intelligence.
""")

# -----------------------------
## -----------------------------
# Upload Page
# -----------------------------
elif page == "📄 Upload Notes":

    st.title("📄 Upload Notes")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success("📄 PDF Uploaded Successfully!")

        extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text.strip():

            chunks = chunk_text(extracted_text)

            with st.spinner("Processing PDF..."):

                store_chunks(chunks)

            # Save for other pages
            st.session_state["chunks"] = chunks

            # Clear old cached results
            st.session_state.pop("summary", None)
            st.session_state.pop("quiz", None)

            st.success("✅ Notes stored in Vector Database!")

            st.info(f"📑 Total Chunks Created: {len(chunks)}")

        else:

            st.error("❌ This PDF doesn't contain readable text.")

    else:

        st.info("📄 Upload a PDF to get started.")
# -----------------------------
# Chat Page
# -----------------------------
elif page == "💬 Ask Questions":

    st.title("💬 Ask ScholarAI")

    question = st.text_input(
        "Ask any question"
    )

    if st.button("Ask AI"):

        if question:

            with st.spinner("Thinking..."):

                answer = ask_llm(question)

            st.subheader("Answer")

            st.write(answer)
            

# -----------------------------
# Summary Page
# -----------------------------
elif page == "📝 Summary":

    st.title("📝 Generate Summary")

    if "chunks" not in st.session_state:

        st.warning("Please upload a PDF first.")

    else:

        if st.button("Generate Summary"):

            with st.spinner("Creating summary..."):

                st.session_state["summary"] = generate_summary(
                    st.session_state["chunks"]
                )

        if "summary" in st.session_state:

            st.subheader("📚 Summary")

            st.write(st.session_state["summary"])
# -----------------------------
# Quiz Page
# -----------------------------
elif page == "❓ Quiz":

    st.title("❓ AI Quiz Generator")


    if "chunks" not in st.session_state:

        st.warning("Please upload a PDF first.")


    else:


        if st.button("Generate Quiz"):

            with st.spinner("Creating quiz..."):

                quiz = generate_quiz(
                    st.session_state["chunks"]
                )


                st.session_state["quiz"] = quiz



        if "quiz" in st.session_state:


            quiz = st.session_state["quiz"]


            if not quiz:

                st.error(
                    "Quiz generation failed. Try again."
                )


            else:


                score = 0


                st.success(
                    f"Generated {len(quiz)} questions"
                )


                for i, q in enumerate(quiz):

                    st.markdown("---")


                    st.subheader(
                        f"Question {i+1}"
                    )


                    answer = st.radio(
                        q["question"],
                        q["options"],
                        key=f"question_{i}"
                    )


                    if st.button(
                        f"Check Answer {i+1}",
                        key=f"check_{i}"
                    ):
                        
                        selected_index = q["options"].index(answer) + 1

                        if selected_index == q["answer"]:

                             st.success("✅ Correct Answer!")

                        else:

                            st.error("❌ Wrong Answer")

                            st.info(
                                   f"Correct Answer: {q['options'][q['answer']-1]}"
                               )
                        



# -----------------------------
# About
# -----------------------------
elif page == "ℹ️ About":

    st.title("ℹ️ About ScholarAI")

    st.write("""
ScholarAI is an AI-powered learning assistant.

Technologies Used:

- Python
- Streamlit
- LangChain
- ChromaDB
- Ollama
""")