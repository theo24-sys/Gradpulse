try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

from django.conf import settings
import PyPDF2
import json
import logging

logger = logging.getLogger(__name__)

# Configure Gemini Client
client = None
try:
    if genai is not None and hasattr(settings, 'GOOGLE_API_KEY') and settings.GOOGLE_API_KEY:
        client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    else:
        logger.warning("GOOGLE_API_KEY not found in settings.")
except Exception as e:
    logger.error(f"Failed to configure Gemini Client: {e}")

def extract_text_from_pdf(pdf_file):
    """Extracts raw text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return None

def parse_text_transcript_with_gemini(text):
    """
    Uses Gemini 1.5 Flash to parse raw transcript text and return a list of grades.
    """
    if not text.strip():
        return []

    if client is None:
        logger.warning("Gemini client not available.")
        return []

    prompt = f"""
    Act as a transcript parser for a Kenyan University or TVET system. 
    Below is the raw text extracted from a student transcript. 
    Extract all course units and their respective grades into a structured JSON list.
    Course units should have unit_name, grade, credit_hours (as int), semester, and year (as int).
    
    Format required:
    [
        {{"unit_name": "Introduction to Programming", "grade": "A", "credit_hours": 3, "semester": "Semester 1", "year": 2023}},
        ...
    ]
    
    Transcription Text:
    {text}
    
    Return ONLY JSON.
    """

    try:
        response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
        content = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(content)
        return data
    except Exception as e:
        error_str = str(e)
        logger.error(f"Gemini text parsing error: {e}")
        return {"error": f"AI Parsing failed: {error_str}"}

def parse_transcript_with_gemini(pdf_file):
    """
    Uses Gemini 1.5 Flash to parse a student transcript and return a list of grades.
    """
    text = extract_text_from_pdf(pdf_file)
    if not text:
        return {"error": "Could not extract text from PDF"}
    return parse_text_transcript_with_gemini(text)

def generate_simulation_scenario(topic):
    """
    Generates a learning simulation scenario based on a specific topic.
    """
    if client is None:
        logger.warning("Gemini client not available.")
        return None

    prompt = f"""
    Create a professional learning simulation scenario for a university or TVET student.
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
        response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
        content = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except Exception as e:
        logger.error(f"Gemini simulation generation error: {e}")
        return None

def generate_search_queries(traits, category="events"):
    """
    Generates specific search queries based on student traits and a category.
    Used for scraping industry events, internships, or certifications.
    """
    if client is None:
        logger.warning("Gemini client not available.")
        return []

    prompt = f"""
    Based on these student traits: {traits}, generate 3 specific search queries 
    for {category} in Kenya (including TVET-specific opportunities if applicable). 
    Queries should be targeted and professionally relevant.
    Return ONLY the queries separated by newlines. No numbers, no bullets.
    """
    
    try:
        response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
        queries = response.text.strip().split('\n')
        return [q.strip() for q in queries if q.strip()]
    except Exception as e:
        logger.error(f"Gemini query generation error: {e}")
        return []
