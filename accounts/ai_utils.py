try:
    import google.generativeai as genai
except ImportError:
    genai = None

from django.conf import settings
import PyPDF2
import json
import logging

logger = logging.getLogger(__name__)

# Configure Gemini
try:
    if hasattr(settings, 'GOOGLE_API_KEY') and settings.GOOGLE_API_KEY:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
    else:
        logger.warning("GOOGLE_API_KEY not found in settings.")
except Exception as e:
    logger.error(f"Failed to configure Gemini: {e}")

def extract_text_from_pdf(pdf_file):
    """Extracts raw text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return None

def parse_transcript_with_gemini(pdf_file):
    """
    Uses Gemini 1.5 Flash to parse a student transcript and return a list of grades.
    """
    text = extract_text_from_pdf(pdf_file)
    if not text:
        return {"error": "Could not extract text from PDF"}

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Act as a transcript parser for a Kenyan University system. 
    Below is the raw text extracted from a student transcript. 
    Extract all course units and their respective grades into a structured JSON list.
    
    Format required:
    [
        {{"course_code": "CSC 101", "course_name": "Introduction to Programming", "grade": "A", "semester": "Semester 1", "year": "2023"}},
        ...
    ]
    
    Transcription Text:
    {text}
    
    Return ONLY JSON. Do not include markdown formatting or explanations.
    """

    try:
        response = model.generate_content(prompt)
        # Clean response (remove ```json wrappers if present)
        content = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(content)
        return data
    except Exception as e:
        logger.error(f"Gemini parsing error: {e}")
        return {"error": str(e)}

def generate_simulation_scenario(topic):
    """
    Generates a learning simulation scenario based on a specific topic.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Create a professional learning simulation scenario for a university student.
    Topic: {topic}
    
    Requirement:
    1. A 'Situation' description (2-3 paragraphs).
    2. A 'Task' to perform.
    3. Three 'Multiple Choice Options' (A, B, C) with explanations for each.
    
    Return as JSON:
    {{
        "title": "...",
        "situation": "...",
        "task": "...",
        "options": [
            {{"id": "A", "text": "...", "feedback": "..."}},
            ...
        ],
        "correct_option": "A"
    }}
    
    Return ONLY JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except Exception as e:
        logger.error(f"Gemini simulation generation error: {e}")
        return None
