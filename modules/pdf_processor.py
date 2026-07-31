import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
from modules.utils import clean_text_whitespace

def extract_text_from_pdf(pdf_stream: bytes) -> List[Dict[str, Any]]:
    """
    Extracts text from PDF bytes page by page.
    Returns a list of dictionaries, each containing:
      - 'text': The cleaned text content of the page
      - 'page_num': The page number (1-indexed)
    """
    pages_data = []
    try:
        # Open the PDF directly from the byte stream in memory
        with fitz.open(stream=pdf_stream, filetype="pdf") as doc:
            for index, page in enumerate(doc):
                # Extract text from the page
                page_text = page.get_text()
                
                # Clean the text using our utility function
                cleaned_text = clean_text_whitespace(page_text)
                
                # Only add pages that contain actual text
                if cleaned_text:
                    pages_data.append({
                        "text": cleaned_text,
                        "page_num": index + 1  # 1-indexed for user friendly display
                    })
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
                
    return pages_data

def chunk_extracted_text(pages_data: List[Dict[str, Any]], chunk_size: int = 800, chunk_overlap: int = 150) -> List[Dict[str, Any]]:
    """
    Splits the extracted page text into smaller chunks using LangChain's RecursiveCharacterTextSplitter.
    Attaches metadata (page number) to each chunk to keep track of where the text came from.
    """
    # Define splitter configurations
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = []
    
    for page in pages_data:
        text = page["text"]
        page_num = page["page_num"]
        
        # Split text of the current page
        split_texts = splitter.split_text(text)
        
        for index, chunk_text in enumerate(split_texts):
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "page_num": page_num,
                    "chunk_id": f"p{page_num}_c{index}"
                }
            })
            
    return chunks
