try:
    from google import genai
except ImportError:
    genai = None

from django.conf import settings
import PyPDF2
import json
import logging

logger = logging.getLogger(__name__)

_client = None

def get_client():
    global _client
    if _client is not None:
        return _client
    if genai is None:
        return None
    api_key = getattr(settings, 'GOOGLE_API_KEY', None)
    if not api_key:
        logger.warning("GOOGLE_API_KEY not found in settings.")
        return None
    try:
        _client = genai.Client(api_key=api_key)
        return _client
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
        return None


def extract_text_from_pdf(pdf_file):
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
    if not text.strip():
        return []
    client = get_client()
    if client is None:
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
        if "429" in error_str or "quota" in error_str.lower():
            logger.error(f"Gemini API Quota Exceeded: {e}")
        elif "403" in error_str or "permission" in error_str.lower():
            logger.error(f"Gemini API Permission Denied: {e}")
        else:
            logger.error(f"Gemini text parsing error: {e}")
        return {"error": f"AI Parsing failed: {error_str}"}


def parse_transcript_with_gemini(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    if not text:
        return {"error": "Could not extract text from PDF"}
    return parse_text_transcript_with_gemini(text)


def generate_simulation_scenario(topic):
    client = get_client()
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
            {{"id": "B", "text": "...", "feedback": "..."}},
            {{"id": "C", "text": "...", "feedback": "..."}}
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
    client = get_client()
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
        error_str = str(e)
        if "429" in error_str or "quota" in error_str.lower():
            logger.error(f"Gemini API Quota Exceeded: {e}")
        else:
            logger.error(f"Gemini query generation error: {e}")
        return []


def unismart_career_chat(query, user_context=""):
    client = get_client()
    if client is None:
        return "I'm sorry, my AI career guidance system is temporarily unavailable. Please try again later."
    
    system_prompt = f"""
    You are 'UniSmart Assistant', a specialized Kenyan academic and career advisor for high school students.
    Your goal is to guide students on course selection, KUCCPS clusters, and career pathways in Kenya.
    
    Context about the student: {user_context}
    
    Guidelines:
    1. Be encouraging and provide specific advice relevant to the Kenyan education system (e.g., talk about KCSE, University groups, TVET).
    2. If asked about a specific course, explain what it entails and mention typical cluster requirements.
    3. Keep responses concise and formatted with markdown for readability.
    
    User Query: {query}
    """
    try:
        response = client.models.generate_content(model='gemini-1.5-flash', contents=system_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini UniSmart chat error: {e}")
        return "I encountered an error while processing your request. Please try again."


def get_mentor_recommendation(course_interest=None):
    """
    Finds a university student studying the interested course who is marked as a mentor.
    """
    from .models import CustomUser
    from django.db.models import Q
    
    # Base query for mentors
    mentors = CustomUser.objects.filter(
        portal_type=CustomUser.PORTAL_STUDENT,
        is_mentor=True
    ).exclude(course="")
    
    if course_interest:
        # Search for similar course names in student portal
        mentors = mentors.filter(
            Q(course__icontains=course_interest) | 
            Q(institution__icontains=course_interest)
        )
    
    return mentors.order_by('?')[:1].first() # Randomly pick one