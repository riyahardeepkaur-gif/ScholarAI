import os

# Define project directories relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
NOTES_DIR = os.path.join(BASE_DIR, "notes")

# Ensure necessary directories exist
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(NOTES_DIR, exist_ok=True)

def is_pdf(filename: str) -> bool:
    """
    Check if the uploaded file has a PDF extension.
    """
    return filename.lower().endswith(".pdf")

def clean_text_whitespace(text: str) -> str:
    """
    Perform basic NLP cleaning: remove extra whitespace and duplicate newlines.
    Preserves single newlines and paragraph structure for better splitting.
    """
    if not text:
        return ""
    import re
    # Clean leading/trailing spaces per line
    lines = [line.strip() for line in text.splitlines()]
    # Re-join lines with newlines
    cleaned = "\n".join(lines)
    # Replace 3 or more consecutive newlines with exactly 2 newlines (a clean paragraph break)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    # Replace multiple horizontal spaces with a single space
    cleaned = re.sub(r" {2,}", " ", cleaned)
    return cleaned.strip()
