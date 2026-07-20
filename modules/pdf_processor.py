import fitz


def extract_text_from_pdf(pdf_file):
    text = ""

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks