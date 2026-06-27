import json
import logging
from accounts.ai_utils import get_client
from django.db import transaction
from .models import CourseObjective, MarketChallenge, StudentSimulation

logger = logging.getLogger(__name__)

def generate_matched_scenarios(student):
    """
    Finds matches between the student's course objectives and active market challenges.
    Creates StudentSimulation records for the best matches.
    """
    # 1. Fetch student's grades to identify active courses
    student_grades = student.grades.all()
    if not student_grades.exists():
        logger.info(f"Student {student.username} has no transcript grades.")
        return []

    # Auto-populate CourseObjectives from student grades if they don't exist
    for grade in student_grades:
        exists = CourseObjective.objects.filter(course_title__iexact=grade.unit_name).exists()
        if not exists:
            # Create a simple unique course code based on unit name prefix
            clean_name = ''.join(c for c in grade.unit_name if c.isalnum() or c.isspace())
            words = clean_name.split()
            if len(words) >= 2:
                code = "".join(w[0] for w in words[:4]).upper() + str(len(grade.unit_name))
            else:
                code = grade.unit_name[:4].upper() + str(len(grade.unit_name))
            
            # Ensure unique code
            base_code = code
            counter = 1
            while CourseObjective.objects.filter(course_code=code).exists():
                code = f"{base_code}_{counter}"
                counter += 1

            CourseObjective.objects.create(
                course_code=code,
                course_title=grade.unit_name,
                objectives_keywords=f"{grade.unit_name.lower()}, learning, application",
                institution=student.institution or "General"
            )

    client = get_client()
    if not client:
        logger.warning("Gemini client not available for AI matching.")
        return []

    objectives = CourseObjective.objects.all()
    if not objectives.exists():
        logger.info("No CourseObjective records available in database.")
        return []

    challenges = MarketChallenge.objects.filter(is_active=True)
    if not challenges.exists():
        logger.info("No active MarketChallenge records available.")
        return []

    # Build prompt inputs
    objectives_data = [
        {
            "id": obj.id,
            "code": obj.course_code,
            "title": obj.course_title,
            "keywords": obj.objectives_keywords
        } for obj in objectives
    ]

    challenges_data = [
        {
            "id": chal.id,
            "title": chal.title,
            "description": chal.description,
            "skills": chal.required_skills
        } for chal in challenges
    ]

    prompt = f"""
You are an AI matching engine that connects academic course syllabus objectives to real-world business challenges.
Match the student's Course Objectives with the available Market Challenges based on required skills and academic topics.

Course Objectives:
{json.dumps(objectives_data, indent=2)}

Market Challenges:
{json.dumps(challenges_data, indent=2)}

Return a JSON list of matches. Each match must have:
- "course_objective_id": integer ID of the course objective
- "market_challenge_id": integer ID of the market challenge
- "confidence_score": float between 0.0 and 1.0
- "reasoning": 1-2 sentence explanation of why this match makes sense

Return ONLY a valid JSON list. No explanation, no HTML tags, no ```json markdown codeblock wrappers.
"""

    try:
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        text = response.text.strip()
        
        # Clean markdown code block wraps if present
        if "```json" in text:
            text = text.split("```json")[-1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[-1].split("```")[0].strip()
            
        start = text.find('[')
        end = text.rfind(']') + 1
        if start != -1 and end != 0:
            text = text[start:end]

        matches = json.loads(text)
        created_sims = []

        with transaction.atomic():
            for match in matches:
                obj_id = match.get("course_objective_id")
                chal_id = match.get("market_challenge_id")
                score = match.get("confidence_score", 0.0)
                reasoning = match.get("reasoning", "")

                if not obj_id or not chal_id:
                    continue

                try:
                    obj = CourseObjective.objects.get(id=obj_id)
                    chal = MarketChallenge.objects.get(id=chal_id)
                except (CourseObjective.DoesNotExist, MarketChallenge.DoesNotExist):
                    continue

                if score >= 0.5:
                    sim, created = StudentSimulation.objects.get_or_create(
                        student=student,
                        challenge=chal,
                        defaults={
                            'course_objective': obj,
                            'status': 'assigned',
                            'adapt_config_json': {
                                'confidence_score': float(score),
                                'match_reasoning': reasoning
                            }
                        }
                    )
                    created_sims.append(sim)
                    
        return created_sims
    except Exception as e:
        logger.error(f"Error in AI matching: {e}")
        return []
