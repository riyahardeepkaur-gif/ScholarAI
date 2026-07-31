import json
import re
from typing import List, Dict, Any
from modules.llm import get_llm
from langchain_core.prompts import PromptTemplate

def clean_json_output(raw_output: str) -> str:
    """
    Cleans LLM response by stripping out markdown blocks (like ```json ... ```)
    and returning only the raw JSON string.
    """
    cleaned = raw_output.strip()
    
    # Remove markdown code blocks if present
    if cleaned.startswith("```"):
        # Match ```json or ``` and strip it
        cleaned = re.sub(r"^```(?:json)?\n", "", cleaned, flags=re.IGNORECASE)
        # Strip ending code block
        cleaned = re.sub(r"\n```$", "", cleaned)
        
    cleaned = cleaned.strip()
    
    # If the LLM still wrapped it with text before/after, find the first '[' and last ']'
    try:
        start_idx = cleaned.find("[")
        end_idx = cleaned.rfind("]")
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx : end_idx + 1]
    except Exception:
        pass
        
    return cleaned

def generate_quiz(pages_data: List[Dict[str, Any]], num_retries: int = 2, model_name: str = "llama3.2:3b") -> List[Dict[str, Any]]:
    """
    Generates exactly 5 MCQs from the PDF notes text.
    Sends a chunk of notes to Ollama and requests a clean JSON array of MCQs.
    Retries if the JSON parsing fails. Propagates exceptions to show custom errors in UI.
    """
    if not pages_data:
        return []

    # Combine text up to a safe length for CPU processing
    combined_text = ""
    for page in pages_data:
        combined_text += f"\n{page['text']}"
        if len(combined_text) > 8000:
            combined_text = combined_text[:8000]
            break

    # Concise and direct quiz generation prompt
    prompt_template = """Generate 5 MCQs based ONLY on the study notes.
Return ONLY a valid JSON list of objects matching this schema:
[
  {{
    "question": "question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_option": "Option A"
  }}
]
Rules:
- Give exactly 4 options.
- The correct_option MUST match one of the options exactly.
- No markdown formatting, no explanations, no wrapping code blocks.

Notes:
{text}

JSON Output:"""

    prompt = PromptTemplate(
        input_variables=["text"],
        template=prompt_template
    )

    llm = get_llm(model_name)
    formatted_prompt = prompt.format(text=combined_text)

    last_error = None
    for attempt in range(num_retries + 1):
        try:
            response = llm.invoke(formatted_prompt)
            json_str = clean_json_output(response)
            
            # Attempt to parse
            quiz_data = json.loads(json_str)
            
            # Validate structured array
            if isinstance(quiz_data, list) and len(quiz_data) > 0:
                valid_quizzes = []
                for item in quiz_data:
                    if "question" in item and "options" in item and "correct_option" in item:
                        options = item["options"]
                        if isinstance(options, list) and len(options) == 4:
                            cleaned_options = [o.strip() for o in options]
                            item["options"] = cleaned_options
                            
                            correct_opt = item["correct_option"].strip()
                            if correct_opt in cleaned_options:
                                item["correct_option"] = correct_opt
                            else:
                                # Fallback mapping: digits
                                if correct_opt.isdigit():
                                    idx = int(correct_opt) - 1
                                    if 0 <= idx < len(cleaned_options):
                                        correct_opt = cleaned_options[idx]
                                # Fallback mapping: letter indices
                                elif correct_opt.upper() in ["A", "B", "C", "D"]:
                                    idx = ["A", "B", "C", "D"].index(correct_opt.upper())
                                    correct_opt = cleaned_options[idx]
                                # Fallback mapping: "Option A" style
                                elif correct_opt.upper().startswith("OPTION"):
                                    parts = correct_opt.split()
                                    if len(parts) > 1:
                                        val = parts[-1].upper()
                                        if val in ["A", "B", "C", "D"]:
                                            idx = ["A", "B", "C", "D"].index(val)
                                            correct_opt = cleaned_options[idx]
                                        elif val.isdigit():
                                            idx = int(val) - 1
                                            if 0 <= idx < len(cleaned_options):
                                                correct_opt = cleaned_options[idx]
                                                
                            item["correct_option"] = correct_opt
                            valid_quizzes.append(item)
                
                if len(valid_quizzes) >= 1:
                    return valid_quizzes[:5]
            
            print(f"Attempt {attempt + 1}: Parsed output but failed schema validation. Retrying...")
            
        except Exception as e:
            last_error = e
            print(f"Attempt {attempt + 1}: Failed to generate/parse JSON. Error: {e}. Retrying...")
            
    # Propagate the last exception if all attempts fail
    if last_error:
        raise last_error
        
    return []
