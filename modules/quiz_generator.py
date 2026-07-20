import ollama
import json
import re


def generate_quiz(chunks):

    context = "\n\n".join(chunks[:5])

    prompt = f"""
You are ScholarAI.

Create exactly 5 multiple choice questions (MCQ) from these study notes.

Rules:
- Each question must have exactly 4 distinct options (these options must be meaningful answers based on the notes, NOT numbers or generic placeholders).
- The answer must be the index of the correct option (should be 1, 2, 3, or 4 only).
- Return ONLY a JSON list of questions matching the format below.
- Do not include any explanation or markdown formatting.

Format:
[
  {{
    "question": "Question text",
    "options": [
      "Actual choice A",
      "Actual choice B",
      "Actual choice C",
      "Actual choice D"
    ],
    "answer": 2
  }}
]

Study Notes:
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

    quiz_text = response["message"]["content"]

    try:
        
        start_idx = min(
            [i for i in [quiz_text.find('['), quiz_text.find('{')] if i != -1],
            default=-1
        )
        end_idx = max(
            [quiz_text.rfind(']'), quiz_text.rfind('}')]
        )
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = quiz_text[start_idx:end_idx+1]
        else:
            json_str = quiz_text

        data = json.loads(json_str)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            
            for key in ["questions", "quiz", "results"]:
                if key in data and isinstance(data[key], list):
                    return data[key]
            
            
            questions = []
            if "question" in data and "options" in data:
                return [data]
                
            for key in sorted(data.keys()):
                val = data[key]
                if isinstance(val, dict) and "question" in val and "options" in val:
                    questions.append(val)
            if questions:
                return questions
        return []

    except Exception as e:
        print("AI OUTPUT:")
        print(quiz_text)
        print(f"Error parsing quiz JSON: {e}")
        return []