from modules.llm import get_llm, handle_llm_exception
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Any

def generate_pdf_summary(pages_data: List[Dict[str, Any]], model_name: str = "llama3.2:3b") -> str:
    """
    Generates a concise study summary (~150 words) from extracted PDF text using Ollama.
    Combines text up to a safe context length to avoid slow processing on local hardware.
    """
    if not pages_data:
        return "No text available in this document to summarize."

    # Concatenate page texts up to a safe threshold (approx 8000 characters / 1500-2000 words)
    # This prevents the LLM from running slowly on a standard laptop CPU
    combined_text = ""
    for page in pages_data:
        combined_text += f"\n--- Page {page['page_num']} ---\n{page['text']}"
        if len(combined_text) > 8000:
            combined_text = combined_text[:8000] + "\n\n[Content truncated for length limitations...]"
            break

    # Streamlined summary prompt to reduce processing time
    prompt_template = """Summarize the study notes in ~150 words.
Rules:
- Format in bullet points.
- Include a brief 'Topic Overview' section.
- Include a list of 'Key Concepts'.

Notes:
{text}

Summary:"""

    prompt = PromptTemplate(
        input_variables=["text"],
        template=prompt_template
    )

    llm = get_llm(model_name)
    formatted_prompt = prompt.format(text=combined_text)
    
    try:
        response = llm.invoke(formatted_prompt)
        return response.strip()
    except Exception as e:
        return handle_llm_exception(e, model_name)
