import PyPDF2
from accounts.ai_utils import parse_text_transcript_with_gemini as parse_transcript_with_ai
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

# Removed legacy OpenAI parse_transcript_with_ai (now imported from accounts.ai_utils)
