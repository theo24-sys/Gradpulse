import PyPDF2
from openai import OpenAI
from django.conf import settings
import json

def extract_text_from_pdf(file_obj):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def parse_transcript_with_ai(text):
    if not text.strip():
        return []
        
    try:
        client = OpenAI(api_key=settings.env('OPENAI_API_KEY', default=''))
        
        prompt = """
        You are an AI that extracts academic grades from raw university transcript text.
        Extract the courses, grades, credits, semester, and year if available.
        Map the grades to the standard scale if possible (A, A-, B+, B, B-, C+, C, C-, D+, D, E).
        Return the output ONLY as a valid JSON array of objects. Do not include markdown codeblocks like ```json .
        Format:
        [
          {
            "unit_name": "Course Title",
            "grade": "A",
            "credit_hours": 3,
            "semester": "Fall",
            "year": 2024
          }
        ]
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Transcript text:\n{text[:6000]}"}
            ],
            temperature=0.1,
            max_tokens=1500,
        )
        content = response.choices[0].message.content.strip()
        
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        grades_data = json.loads(content)
        return grades_data
    except Exception as e:
        print(f"OpenAI parsing error: {e}")
        return []
