import os
import json
import logging
import time
import PyPDF2
import bleach
import markdown
from django.conf import settings

try:
    from google import genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)

_client = None

def render_ai_markdown(text):
    html = markdown.markdown(
        str(text or ''),
        extensions=['extra', 'nl2br', 'sane_lists']
    )
    return bleach.clean(
        html,
        tags={
            'p', 'br', 'strong', 'em', 'del', 'ul', 'ol', 'li', 'h3', 'h4',
            'blockquote', 'code', 'pre', 'a'
        },
        attributes={'a': ['href', 'title', 'target', 'rel']},
        protocols={'http', 'https', 'mailto'},
        strip=True
    )

def get_model_name():
    return getattr(settings, 'GEMINI_MODEL', 'gemini-3.6-flash')

def get_client():
    global _client
    if _client is not None:
        return _client
    if genai is None:
        logger.error("google-genai library is not installed or could not be imported.")
        return None
    api_key = (
        getattr(settings, 'GOOGLE_API_KEY', '')
        or os.environ.get('GOOGLE_API_KEY', '')
        or os.environ.get('GEMINI_API_KEY', '')
    )
    if not api_key:
        logger.warning("GOOGLE_API_KEY / GEMINI_API_KEY not found in settings or environment.")
        return None
    api_key = str(api_key).strip().strip('"').strip("'")
    if not api_key:
        return None
    try:
        _client = genai.Client(api_key=api_key)
        return _client
    except Exception as e:
        logger.error(f"Failed to configure Gemini client: {e}")
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


def calculate_kcse_clusters(results):
    """
    Uses Gemini to calculate cluster points and suggest courses.
    results: dict of grades {'ENG': 'A', ...}
    """
    client = get_client()
    if client is None:
        logger.warning("Gemini client not available for KCSE cluster calculation.")
        return {
            "clusters": {},
            "summary": "AI calculation offline. Please configure `GOOGLE_API_KEY` or `GEMINI_API_KEY` in your environment variables.",
            "recommendations": []
        }

    prompt = f"""
    You are a Kenyan career consultant and KUCCPS expert.
    The student has the following KCSE results: {results}
    
    1. Calculate the Cluster Points for the following 4 main clusters as defined by KUCCPS:
       - Law & Humanities
       - Business & Economics
       - Engineering & Technology
       - Medicine & Health Sciences
    
    2. Give a summary of whether the student qualifies for Degree, Diploma, or Certificate level.
    
    3. List 5 specific courses they qualify for based on these grades.
    
    Return the response as a JSON object with this structure:
    {{
        "clusters": {{
            "Law": 42.1,
            "Business": 38.5,
            "Engineering": 35.2,
            "Medicine": 32.8
        }},
        "summary": "Overall grade is X. You qualify for...",
        "recommendations": [
            {{"name": "Bachelor of Laws", "code": "1234567", "institution": "UoN"}},
            ...
        ]
    }}
    Only return valid JSON. No other text.
    """
    
    try:
        response = client.models.generate_content(model=get_model_name(), contents=prompt)
        
        if not response.text:
            # Check for safety blocks
            feedback = getattr(response, 'prompt_feedback', 'No feedback')
            logger.warning(f"Gemini returned empty text. Feedback: {feedback}")
            return {
                "clusters": {"Law": 0, "Business": 0, "Engineering": 0, "Medicine": 0},
                "summary": "AI response was blocked or empty. Please ensure your grades are standard.",
                "recommendations": []
            }

        text = response.text.strip()
        logger.info(f"KCSE Cluster AI Raw Response: {text}")
        
        # Robust JSON cleaning
        if "```json" in text:
            text = text.split("```json")[-1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[-1].split("```")[0].strip()
        
        # Remove any leading/trailing non-JSON characters
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != 0:
            text = text[start:end]
            
        return json.loads(text)
    except Exception as e:
        error_msg = str(e)
        raw_resp = "N/A"
        try:
            raw_resp = response.text if 'response' in locals() else 'N/A'
        except:
            raw_resp = "Response blocked or unavailable"
            
        logger.error(f"Error calculating clusters: {e}. Raw: {raw_resp}")
        
        summary = f"AI calculation failed. Error: {error_msg[:100]}."
        if "429" in error_msg or "quota" in error_msg.lower():
            summary = "AI Quota Exceeded for today. Please try again tomorrow or provide a different Google API Key."
            
        return {
            "clusters": {
                "Law": 0, "Business": 0, "Engineering": 0, "Medicine": 0
            },
            "summary": summary,
            "recommendations": []
        }


def extract_courses_from_text(text, level='degree'):
    """
    Parses raw text to extract courses using Gemini.
    """
    if not text.strip():
        return []
    
    client = get_client()
    if client is None:
        return []
        
    prompt = f"""
    Act as a KUCCPS data specialist. Extract all courses from the following raw text which appears to be from a KUCCPS {level} manual.
    For each course, extract:
    - course_name
    - course_code
    - institution (if unique to one)
    - cluster_group
    - min_points (as a float)
    
    Format as a JSON list. 
    Format example: [ {{"course_name": "Law", "course_code": "123", ...}}, ... ]
    
    Text:
    {text[:10000]}
    
    Return ONLY valid JSON. No other text.
    """
    
    try:
        response = client.models.generate_content(model=get_model_name(), contents=prompt)
        content = response.text.strip()
        
        if "```json" in content:
            content = content.split("```json")[-1].split("```")[0].strip()
        
        start = content.find('[')
        end = content.rfind(']') + 1
        if start != -1 and end != 0:
            content = content[start:end]
            
        return json.loads(content)
    except Exception as e:
        logger.error(f"Gemini text course extraction error: {e}")
        return []


def extract_courses_from_pdf(pdf_file, level='degree'):
    """
    Parses a KUCCPS manual PDF to extract courses.
    """
    text = extract_text_from_pdf(pdf_file)
    if not text:
        return []
    
    client = get_client()
    if client is None:
        return []
        
    prompt = f"""
    Act as a KUCCPS data specialist. Extract all courses from the following snippet of the KUCCPS {level} manual.
    For each course, extract:
    - course_name
    - course_code
    - institution (if unique to one)
    - cluster_group
    - min_points (as a float)
    
    Format as a JSON list.
    Snippet:
    {text[:8000]}  # Limit text to avoid token overflow
    
    Return ONLY valid JSON.
    """
    
    try:
        response = client.models.generate_content(model=get_model_name(), contents=prompt)
        content = response.text.strip()
        
        # Robust JSON cleaning
        if "```json" in content:
            content = content.split("```json")[-1].split("```")[0].strip()
        
        start = content.find('[')
        end = content.rfind(']') + 1
        if start != -1 and end != 0:
            content = content[start:end]
            
        return json.loads(content)
    except Exception as e:
        logger.error(f"Gemini course extraction error: {e}")
        return []


def get_academic_guidance(course):
    """
    Returns a quick academic success tip for a student's course.
    """
    client = get_client()
    if client is None:
        return "Stay focused and manage your time well!"
    
    prompt = f"Give one specific academic success tip for a university student studying {course}. Keep it under 150 characters. Be concise and practical."
    try:
        response = client.models.generate_content(model=get_model_name(), contents=prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Grade AI error: {e}")
        return "Consistency is the key to better grades."


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
        response = client.models.generate_content(model=get_model_name(), contents=prompt)
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
        response = client.models.generate_content(model=get_model_name(), contents=prompt)
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
        response = client.models.generate_content(model=get_model_name(), contents=prompt)
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
        api_key = (
            getattr(settings, 'GOOGLE_API_KEY', '')
            or os.environ.get('GOOGLE_API_KEY', '')
            or os.environ.get('GEMINI_API_KEY', '')
        )
        if not api_key:
            return (
                "⚠️ **AI Setup Required**: Google Gemini API key is missing. "
                "Please configure `GOOGLE_API_KEY` (or `GEMINI_API_KEY`) in your Railway / Render environment variables to activate live AI career guidance!\n\n"
                "💡 In the meantime, you can explore available courses under **Explore Courses** or enter your KCSE grades to compute your cluster points."
            )
        return "⚠️ I'm sorry, the AI career guidance service is temporarily reconnecting. Please try asking your question again in a moment."
    
    system_prompt = f"""
    You are 'UniSmart Assistant', a specialized Kenyan academic and career advisor for high school students.
    Your goal is to guide students on course selection, KUCCPS clusters, and career pathways in Kenya.
    
    Context about the student: {user_context}
    
    Guidelines:
    1. Be encouraging and provide specific advice relevant to the Kenyan education system (e.g., talk about KCSE, University groups, TVET, and KUCCPS).
    2. If you mention or recommend a specific course, explain what it entails and mention typical cluster requirements.
    3. Proactively suggest that the student can "add this course to their basket" if they seem interested, so they can track it later.
    4. Keep responses concise and formatted with markdown for readability.
    
    User Query: {query}
    """
    try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(model=get_model_name(), contents=system_prompt)
                break
            except Exception as e:
                error_text = str(e).lower()
                transient_error = '503' in error_text or 'unavailable' in error_text or '429' in error_text
                if not transient_error or attempt == 2:
                    raise
                time.sleep(1.5 * (attempt + 1))
        if response and response.text:
            return response.text.strip()
        return "I received an empty response. Please try rephrasing your question."
    except Exception as e:
        logger.error(f"Gemini UniSmart chat error: {e}")
        err_msg = str(e)
        if "API_KEY_INVALID" in err_msg or "400" in err_msg or "API key not valid" in err_msg:
            return "⚠️ **AI Authentication Error**: Your Google API key appears to be invalid or disabled. Please check your `GOOGLE_API_KEY` in Google AI Studio."
        elif "429" in err_msg or "quota" in err_msg.lower() or "RESOURCE_EXHAUSTED" in err_msg:
            return "⚠️ **AI Rate Limit**: Quota exceeded for today. Please wait a moment or supply a fresh Google API Key."
        elif "503" in err_msg or "unavailable" in err_msg.lower():
            return "⚠️ **AI Busy**: Gemini is experiencing high demand right now. Please try again in a few seconds."
        return f"⚠️ I encountered an error while processing your request: {err_msg[:120]}. Please try again."


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
        targeted_mentors = mentors.filter(
            Q(course__icontains=course_interest) | 
            Q(institution__icontains=course_interest)
        )
        if targeted_mentors.exists():
            return targeted_mentors.order_by('?')[:1].first()
    
    # Fallback to any random mentor if no match or no interest
    return mentors.order_by('?')[:1].first()