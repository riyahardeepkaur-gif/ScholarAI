import streamlit as st
import os
from streamlit_mic_recorder import mic_recorder

from modules import pdf_processor, vector_store, llm, summarizer, quiz_generator, voice, utils

# -----------------------------------------------------------------------------
# Configuration and UI Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ScholarAI - AI-Powered Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    """
    Injects custom CSS for a premium, modern student look:
    Gradient backgrounds, Outfit typography, and glowing glassmorphism cards.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Apply font family globally */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        /* App Background with beautiful space-like gradient and radial ambient glow */
        .stApp {
            background-color: #0b0d16;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(244, 114, 182, 0.1) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(120, 119, 198, 0.06) 0px, transparent 50%);
            background-attachment: fixed;
        }
        
        /* Premium background and glassmorphism styling */
        .glass-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }
        
        /* Top line gradient to add premium touch */
        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #a78bfa, #f472b6);
            opacity: 0.6;
            transition: opacity 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255, 255, 255, 0.14);
            box-shadow: 0 16px 40px 0 rgba(99, 102, 241, 0.18);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        }
        
        .glass-card:hover::before {
            opacity: 1;
        }
        
        /* Vibrant gradients */
        .gradient-title {
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 2.8rem;
            margin-bottom: 10px;
        }
        .gradient-subtitle {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 20px;
        }
        
        /* Header titles inside cards styling */
        .glass-card h3 {
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            margin-top: 0;
        }
        .glass-card h4 {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
            margin-top: 0;
        }
        
        /* Custom buttons styling */
        div.stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.3) !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px 0 rgba(99, 102, 241, 0.5) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
        }
        div.stButton > button:active {
            transform: translateY(0px) !important;
        }
        
        /* Custom containers */
        .source-box {
            background: rgba(99, 102, 241, 0.05);
            border-left: 4px solid #6366f1;
            border-radius: 6px;
            padding: 15px;
            margin-top: 10px;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }
        
        /* Sidebar styling - matching the main theme with gradients and borders */
        [data-testid="stSidebar"] {
            background-color: #0b0d16 !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 60%),
                radial-gradient(at 100% 100%, rgba(244, 114, 182, 0.08) 0px, transparent 60%) !important;
            background-attachment: fixed !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
        }
        [data-testid="stSidebar"] > div {
            background-color: transparent !important;
        }
        
        /* Turn radio controls in sidebar into navigation button list */
        [data-testid="stSidebar"] .stRadio > div {
            gap: 8px !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            background-color: rgba(255, 255, 255, 0.01) !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            border-radius: 10px !important;
            padding: 10px 16px !important;
            margin-bottom: 6px !important;
            color: #cbd5e1 !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            cursor: pointer !important;
            width: 100% !important;
            display: flex !important;
        }
        [data-testid="stSidebar"] .stRadio label:hover {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-color: rgba(99, 102, 241, 0.3) !important;
            color: #ffffff !important;
            transform: translateX(4px) !important;
        }
        [data-testid="stSidebar"] label[data-checked="true"] {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(167, 139, 250, 0.08) 100%) !important;
            border-color: rgba(99, 102, 241, 0.5) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px 0 rgba(99, 102, 241, 0.15) !important;
        }
        /* Hide default circular radio button indicators */
        [data-testid="stSidebar"] .stRadio label div[role="presentation"] {
            display: none !important;
        }
        [data-testid="stSidebar"] .stRadio label div[class*="RadioFieldStyle"] {
            display: none !important;
        }
        
        /* Style text inputs, file uploader, selects */
        .stTextInput input, .stSelectbox [data-baseweb="select"], .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            transition: all 0.3s ease !important;
        }
        .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus, .stTextArea textarea:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
            background-color: rgba(255, 255, 255, 0.04) !important;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Helper Session State Initialization
# -----------------------------------------------------------------------------
if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = {}  # Cache doc_name -> list of page_data dicts
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "voice_transcript" not in st.session_state:
    st.session_state.voice_transcript = ""
if "summaries" not in st.session_state:
    st.session_state.summaries = {}  # Cache doc_name -> summary text
if "last_voice_audio_bytes" not in st.session_state:
    st.session_state.last_voice_audio_bytes = None
if "indexed_files" not in st.session_state:
    # Query ChromaDB only once on startup and cache it
    st.session_state.indexed_files = vector_store.get_all_uploaded_files()

def load_doc_text_if_needed(filename: str) -> list:
    """
    Checks if text is cached in session state. If not, reads it from the notes/ folder.
    This guarantees reliability on tab changes and refreshes.
    """
    if filename in st.session_state.processed_docs:
        return st.session_state.processed_docs[filename]
        
    file_path = os.path.join(utils.NOTES_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        pages_data = pdf_processor.extract_text_from_pdf(pdf_bytes)
        st.session_state.processed_docs[filename] = pages_data
        return pages_data
    return []

# -----------------------------------------------------------------------------
# Main Application Structure
# -----------------------------------------------------------------------------
inject_custom_css()

# Sidebar Setup
st.sidebar.markdown("<h2 style='text-align: center;'>🎓 ScholarAI</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #94a3b8;'>Your RAG Learning Buddy</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate to:", [
    "🏠 Home",
    "📄 Upload Notes",
    "💬 Ask Questions",
    "📝 Summary",
    "❓ Quiz",
    "🎤 Voice Input",
    "ℹ About"
])

st.sidebar.markdown("---")
# Use cached indexed documents list to save ChromaDB connection overhead on rerun
uploaded_files_list = st.session_state.indexed_files
if uploaded_files_list:
    st.sidebar.markdown("📁 **Indexed Documents:**")
    for f in uploaded_files_list:
        st.sidebar.markdown(f"- `{f}`")
else:
    st.sidebar.info("No documents uploaded yet.")

st.sidebar.markdown("---")
st.sidebar.markdown("⚙️ **Settings**")
model_choice = st.sidebar.selectbox(
    "Active Ollama Model:",
    ["llama3.2:3b", "llama3.2:1b"],
    help="llama3.2:1b is smaller and much faster on CPUs. llama3.2:3b is more accurate."
)

# -----------------------------------------------------------------------------
# PAGE RENDERERS
# -----------------------------------------------------------------------------

# 🏠 HOME PAGE
if page == "🏠 Home":
    st.markdown("<h1 class='gradient-title'>ScholarAI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='gradient-subtitle'>AI-Powered Local Study Assistant</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        <h3>Welcome to ScholarAI! 🎓</h3>
        <p>ScholarAI is an intelligent, offline learning assistant designed to streamline your study process. By combining <b>Natural Language Processing (NLP)</b>, local <b>Sentence Embeddings</b>, and a local <b>Llama LLM</b> via <b>Retrieval-Augmented Generation (RAG)</b>, ScholarAI allows you to study notes and generate learning resources instantly—without sending your data to the cloud.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h4>⚡ Key Features</h4>
            <ul>
                <li><b>📄 Document indexing:</b> Upload standard PDF notes. ScholarAI chunks them and stores semantic embeddings in a local vector database.</li>
                <li><b>💬 Contextual Q&A:</b> Ask questions about your notes. The system fetches the exact matching sections and generates answers <i>only</i> from your notes.</li>
                <li><b>📝 Study Summaries:</b> Generate clean, structured bullet-point summaries of your notes, summarizing key concepts.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h4>⚙️ Interactive Tools</h4>
            <ul>
                <li><b>❓ Interactive Quizzes:</b> Generate 5 custom Multiple-Choice Questions (MCQs) automatically from notes. Test your knowledge and get immediate scores!</li>
                <li><b>🎤 Voice Search:</b> Click the microphone to ask questions by voice, automatically transcribing speech to text.</li>
                <li><b>🔒 100% Local & Private:</b> Runs fully on Ollama and sentence-transformers. Zero external API calls, zero usage charges.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# 📄 UPLOAD NOTES PAGE
elif page == "📄 Upload Notes":
    st.markdown("<h2>📄 Upload Notes</h2>", unsafe_allow_html=True)
    st.write("Upload your study notes (PDF format) to segment them and index them into the local vector database.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a PDF notes file", type=["pdf"])
        
        if uploaded_file is not None:
            filename = uploaded_file.name
            
            # Action button
            if st.button("🚀 Process & Index notes"):
                # Initialize visual progress bar & status container
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Step 1/3: Extracting text from PDF (PyMuPDF)...")
                progress_bar.progress(10)
                
                pdf_bytes = uploaded_file.read()
                pages_data = pdf_processor.extract_text_from_pdf(pdf_bytes)
                
                if not pages_data:
                    st.error("No extractable text found in this PDF file. Make sure it is not empty or scanned/image-only.")
                    progress_bar.empty()
                    status_text.empty()
                else:
                    # Save PDF to local notes folder persistently
                    file_save_path = os.path.join(utils.NOTES_DIR, filename)
                    with open(file_save_path, "wb") as f:
                        f.write(pdf_bytes)
                        
                    # Cache text extraction in session state
                    st.session_state.processed_docs[filename] = pages_data
                    
                    progress_bar.progress(40)
                    status_text.text("Step 2/3: Splitting text into semantic chunks...")
                    chunks = pdf_processor.chunk_extracted_text(pages_data)
                    
                    progress_bar.progress(70)
                    status_text.text("Step 3/3: Creating embeddings & storing in ChromaDB (offline)...")
                    success = vector_store.add_pdf_chunks(chunks, filename)
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    if success:
                        # Refresh the cached list of indexed files
                        st.session_state.indexed_files = vector_store.get_all_uploaded_files()
                        st.success(f"Success! {filename} processed, split into {len(chunks)} chunks, and saved in ChromaDB.")
                    else:
                        st.error("An error occurred while adding embeddings to ChromaDB.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Database Controls</h4>", unsafe_allow_html=True)
        st.write("Current Indexed Documents:")
        files = st.session_state.indexed_files
        if files:
            for f in files:
                st.write(f"- `{f}`")
                
            st.markdown("---")
            if st.button("🗑️ Clear Database", help="This deletes all stored vectors and documents."):
                # Delete files in notes/ folder
                for f in os.listdir(utils.NOTES_DIR):
                    file_path = os.path.join(utils.NOTES_DIR, f)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)
                        
                st.session_state.processed_docs.clear()
                vector_store.clear_vector_store()
                
                # Invalidate application cache states
                st.session_state.indexed_files = []
                st.session_state.summaries.clear()
                st.session_state.quiz_questions = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.voice_transcript = ""
                st.session_state.last_voice_audio_bytes = None
                
                st.success("Vector store and notes folder cleared successfully!")
                st.rerun()
        else:
            st.info("ChromaDB collection is currently empty.")
        st.markdown("</div>", unsafe_allow_html=True)

# 💬 ASK QUESTIONS PAGE
elif page == "💬 Ask Questions":
    st.markdown("<h2>💬 Ask Questions (RAG Pipeline)</h2>", unsafe_allow_html=True)
    
    files = st.session_state.indexed_files
    if not files:
        st.warning("⚠️ No documents indexed yet. Please go to the 'Upload Notes' tab and upload your PDF files first.")
    else:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # Doc selector
        doc_choice = st.selectbox("Select document context:", ["All Documents"] + files)
        doc_filter = None if doc_choice == "All Documents" else doc_choice
        
        # User Question Input
        question = st.text_input("Enter your question:", placeholder="Ask about terms, formulas, or concepts in your notes...")
        
        if st.button("Search & Answer"):
            if not question.strip():
                st.info("Please enter a question.")
            else:
                with st.spinner("Retrieving relevant document chunks (semantic search)..."):
                    # 1. Similarity Search (retrieving k=3 chunks by default)
                    matching_chunks = vector_store.search_relevant_chunks(question, filename=doc_filter, k=3)
                    
                if not matching_chunks:
                    st.warning("No relevant information found in the database. Trying to generate answer...")
                    
                st.markdown("### Answer")
                # Use st.write_stream to draw the response generator live!
                with st.spinner("Synthesizing answer..."):
                    st.write_stream(llm.stream_answer(question, matching_chunks, model_name=model_choice))
                
                # Show retrieved chunks for viva verification
                if matching_chunks:
                    st.markdown("---")
                    with st.expander("🔍 RAG Debugger: View Retrieved Chunks (ChromaDB)"):
                        st.info("This section shows the exact text chunks retrieved from ChromaDB using semantic similarity search. This proves the RAG pipeline operates properly.")
                        for idx, chunk in enumerate(matching_chunks):
                            page_num = chunk.metadata.get("page_num", "N/A")
                            source = chunk.metadata.get("source", "N/A")
                            st.markdown(f"<div class='source-box'><b>Chunk {idx+1} | Source: {source} (Page {page_num})</b><br/>{chunk.page_content}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# 📝 SUMMARY PAGE
elif page == "📝 Summary":
    st.markdown("<h2>📝 Generate Summary</h2>", unsafe_allow_html=True)
    
    files = st.session_state.indexed_files
    if not files:
        st.warning("⚠️ No documents indexed yet. Please upload PDF notes first.")
    else:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        selected_file = st.selectbox("Select document to summarize:", files)
        
        # Display existing summary if already cached
        cached_summary = st.session_state.summaries.get(selected_file)
        
        if st.button("Generate Study Summary"):
            with st.spinner("Reading document and generating outline with Ollama..."):
                # Load pages data (from cache or disk)
                pages_data = load_doc_text_if_needed(selected_file)
                
                if pages_data:
                    # Summarize
                    summary = summarizer.generate_pdf_summary(pages_data, model_name=model_choice)
                    st.session_state.summaries[selected_file] = summary
                    cached_summary = summary
                else:
                    st.error("Could not load text for the selected document.")
                    
        if cached_summary:
            st.markdown("### Study Notes Summary")
            st.write(cached_summary)
            
            st.markdown("---")
            st.download_button(
                label="📥 Download Summary as Text",
                data=cached_summary,
                file_name=f"{selected_file}_summary.txt",
                mime="text/plain"
            )
        st.markdown("</div>", unsafe_allow_html=True)

# ❓ QUIZ PAGE
elif page == "❓ Quiz":
    st.markdown("<h2>❓ Interactive Quiz</h2>", unsafe_allow_html=True)
    
    files = st.session_state.indexed_files
    if not files:
        st.warning("⚠️ No documents indexed yet. Please upload PDF notes first.")
    else:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        selected_file = st.selectbox("Select document to test yourself on:", files)
        
        # Reset quiz state if selected file changes
        if "quiz_file" not in st.session_state or st.session_state.quiz_file != selected_file:
            st.session_state.quiz_file = selected_file
            st.session_state.quiz_questions = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
        
        # We need a clear button to trigger a new quiz
        if st.button("🎯 Generate New Quiz (5 MCQs)"):
            with st.spinner("Extracting concepts and drafting quiz (Ollama)..."):
                pages_data = load_doc_text_if_needed(selected_file)
                if pages_data:
                    try:
                        quiz = quiz_generator.generate_quiz(pages_data, model_name=model_choice)
                        if quiz:
                            st.session_state.quiz_questions = quiz
                            st.session_state.quiz_answers = {}
                            st.session_state.quiz_submitted = False
                            st.success("Quiz generated successfully! Answer the questions below.")
                        else:
                            st.error("Failed to generate a valid quiz JSON. Please try again.")
                    except Exception as e:
                        st.error(llm.handle_llm_exception(e, model_choice))
                else:
                    st.error("Could not read text for the selected document.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Render quiz if it exists
        if st.session_state.quiz_questions:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### Test Your Knowledge")
            
            # Render questions
            for idx, q_item in enumerate(st.session_state.quiz_questions):
                st.markdown(f"**Q{idx+1}. {q_item['question']}**")
                
                # Check options
                options = q_item["options"]
                
                # Render radio buttons
                choice = st.radio(
                    f"Select an option for Q{idx+1}:",
                    options,
                    key=f"q_{idx}",
                    index=None if not st.session_state.quiz_submitted else options.index(st.session_state.quiz_answers.get(idx, options[0]))
                )
                
                # Store choice
                if not st.session_state.quiz_submitted:
                    st.session_state.quiz_answers[idx] = choice
                    
                st.markdown("---")
                
            # Submit button
            if not st.session_state.quiz_submitted:
                if st.button("Submit Answers"):
                    # Check if all answered
                    unanswered = [i for i in range(len(st.session_state.quiz_questions)) if st.session_state.quiz_answers.get(i) is None]
                    if unanswered:
                        st.warning("Please answer all questions before submitting.")
                    else:
                        st.session_state.quiz_submitted = True
                        st.rerun()
            else:
                # Score check
                score = 0
                for idx, q_item in enumerate(st.session_state.quiz_questions):
                    correct = q_item["correct_option"]
                    user_ans = st.session_state.quiz_answers.get(idx)
                    
                    st.write(f"**Q{idx+1} feedback:**")
                    if user_ans == correct:
                        score += 1
                        st.success(f"✓ Correct! Your choice: '{user_ans}'")
                    else:
                        st.error(f"✗ Incorrect. Your choice: '{user_ans}' | Correct: '{correct}'")
                
                st.markdown("### Quiz Results")
                pct = int((score / len(st.session_state.quiz_questions)) * 100)
                st.metric("Final Score", f"{score} / {len(st.session_state.quiz_questions)}", f"{pct}% Correct")
                
                if score == len(st.session_state.quiz_questions):
                    st.success("Perfect score! You know your notes inside out!")
                elif score >= 3:
                    st.info("Good job! Review your mistakes to get a perfect score next time.")
                else:
                    st.warning("Keep studying! Re-read your notes and try again.")
            st.markdown("</div>", unsafe_allow_html=True)

# 🎤 VOICE INPUT PAGE
elif page == "🎤 Voice Input":
    st.markdown("<h2>🎤 Voice Q&A Search</h2>", unsafe_allow_html=True)
    st.write("Ask a question about your study materials using your voice. Your speech will be transcribed and run through the RAG pipeline.")
    
    files = st.session_state.indexed_files
    if not files:
        st.warning("⚠️ No documents indexed yet. Please upload PDF notes first.")
    else:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        doc_choice = st.selectbox("Select document context for voice query:", ["All Documents"] + files)
        doc_filter = None if doc_choice == "All Documents" else doc_choice
        
        st.markdown("#### Record Your Question:")
        st.write("Click record, speak your question, click stop when done, and wait for the transcription.")
        
        # Audio recording widget
        audio_record = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="🛑 Stop Recording",
            key="voice_page_mic",
            format="wav"
        )
        
        if audio_record:
            audio_bytes = audio_record["bytes"]
            last_bytes = st.session_state.get("last_voice_audio_bytes", None)
            
            # Convert speech to text EXACTLY ONCE per recording
            if audio_bytes and audio_bytes != last_bytes:
                st.session_state.last_voice_audio_bytes = audio_bytes
                try:
                    with st.spinner("Processing speech recognition (SpeechRecognition)..."):
                        transcribed_text = voice.transcribe_audio_bytes(audio_bytes)
                    st.session_state.voice_transcript = transcribed_text
                    st.success("Speech transcription completed!")
                except Exception as e:
                    st.error(f"Speech recognition error: {e}")
                    
        # If transcription exists
        if st.session_state.voice_transcript:
            st.markdown("---")
            st.markdown(f"**Transcribed Text:**")
            edited_question = st.text_input("Edit question if transcription has errors:", value=st.session_state.voice_transcript)
            
            if st.button("Ask AI"):
                with st.spinner("Running semantic search..."):
                    matching_chunks = vector_store.search_relevant_chunks(edited_question, filename=doc_filter, k=3)
                    
                st.markdown("### Answer")
                with st.spinner("Synthesizing answer..."):
                    st.write_stream(llm.stream_answer(edited_question, matching_chunks, model_name=model_choice))
                
                if matching_chunks:
                    with st.expander("🔍 View Retrieved Sources"):
                        for idx, chunk in enumerate(matching_chunks):
                            page_num = chunk.metadata.get("page_num", "N/A")
                            source = chunk.metadata.get("source", "N/A")
                            st.markdown(f"<div class='source-box'><b>Chunk {idx+1} | Source: {source} (Page {page_num})</b><br/>{chunk.page_content}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ℹ ABOUT PAGE
elif page == "ℹ About":
    st.markdown("<h2>ℹ About ScholarAI</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        <h3>Overview</h3>
        <p><b>ScholarAI</b> is a privacy-first, fully-local AI study assistant designed to transform how students interact with their learning materials. By leveraging advanced Retrieval-Augmented Generation (RAG) and natural language processing, the application acts as an offline learning buddy that processes, indexes, and answers questions about your notes without relying on internet connectivity or external APIs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin-top: 30px; margin-bottom: 20px;'>🎯 Core Capabilities</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='glass-card' style='height: 190px;'>
            <h4 style='margin-top: 0;'>📄 PDF Document Indexing</h4>
            <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0;'>Extracts text from PDF notes, segments it into semantic chunks, and indexes them in ChromaDB.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card' style='height: 190px;'>
            <h4 style='margin-top: 0;'>🎤 Hands-Free Voice Search</h4>
            <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0;'>Speech-to-text integration allowing hands-free voice-activated question queries.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='glass-card' style='height: 190px;'>
            <h4 style='margin-top: 0;'>💬 Intelligent Q&A (RAG)</h4>
            <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0;'>Retrieves relevant context chunks and synthesizes precise answers using a local LLM.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card' style='height: 190px;'>
            <h4 style='margin-top: 0;'>🔒 100% Local & Private</h4>
            <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0;'>Runs completely offline with zero external API calls, ensuring full data privacy.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='glass-card' style='height: 190px;'>
            <h4 style='margin-top: 0;'>📝 Automated Summarization</h4>
            <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0;'>Condenses large lecture notes and documents into concise, structured bulleted outlines.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card' style='height: 190px;'>
            <h4 style='margin-top: 0;'>❓ Interactive Quizzes</h4>
            <p style='font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0;'>Automatically drafts interactive multiple-choice quizzes to test your knowledge retention.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-card' style='margin-top: 20px;'>
        <h3>🏗️ System Architecture & Workflow</h3>
        <hr style='border-color: rgba(255,255,255,0.05); margin-bottom: 15px;'/>
        <p>ScholarAI functions through a clean pipeline of modular components:</p>
        <ol>
            <li><b>Document Extraction:</b> <code>PyMuPDF</code> reads text in-memory from PDFs.</li>
            <li><b>Segmentation:</b> A <code>RecursiveCharacterTextSplitter</code> processes text into context-rich blocks.</li>
            <li><b>Vector Storage:</b> <code>all-MiniLM-L6-v2</code> models convert blocks into 384-dimensional embeddings, indexed in a local <code>ChromaDB</code> instance.</li>
            <li><b>Local Generation:</b> <code>Ollama</code> hosts and runs low-latency, offline language models (e.g., Llama 3.2) to synthesize answers, summaries, and quizzes.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)