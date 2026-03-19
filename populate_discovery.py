import os
import django
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gradpulse.settings")
django.setup()

from opportunities.models import YouthProgram, Opportunity
from credentials.models import ProfessionalQualification, Simulation, Credential
from events.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

def populate():
    print("Simulating Webscraping for Discovery Sections...")
    
    # 1. Youth Programs
    youth_data = [
        {
            "title": "Presidential Digital Talent Programme (PDTP)",
            "organization": "ICT Authority Kenya",
            "description": "An internship program that develops ICT high-end skills in recent graduates through private and public sector placements.",
            "location": "Nairobi, Kenya",
            "category": "Technology",
            "link": "https://icta.go.ke/digital-entrenching-ict-skills/"
        },
        {
            "title": "Ajira Digital Program",
            "organization": "Ministry of ICT",
            "description": "Empowering youth with digital skills to enable them to access online work and earn a decent income.",
            "location": "Remote / Nationwide",
            "category": "Digital Skills",
            "link": "https://ajiradigital.go.ke/"
        },
        {
            "title": "Equity Leaders Program (ELP)",
            "organization": "Equity Group Foundation",
            "description": "Leadership development and internship for top-performing scholars in the KCSE examinations.",
            "location": "Nationwide",
            "category": "Leadership",
            "link": "https://equitygroupfoundation.com/elp/"
        },
        {
            "title": "Young African Leaders Initiative (YALI)",
            "organization": "USAID",
            "description": "Leadership training and networking for young leaders across Africa.",
            "location": "Regional Centres",
            "category": "Leadership",
            "link": "https://yali.state.gov/"
        }
    ]

    for item in youth_data:
        YouthProgram.objects.get_or_create(title=item['title'], defaults=item)

    # 2. Professional Qualifications
    qual_data = [
        {
            "title": "Certified Public Accountant (CPA) - Part 1",
            "provider": "KASNEB",
            "description": "The professional qualification for accountants in Kenya, covering Financial Accounting and Law.",
            "category": "Finance",
            "duration": "6 Months",
            "link": "https://kasneb.or.ke/"
        },
        {
            "title": "Certified Human Resource Professional (CHRP)",
            "provider": "HRMPEB",
            "description": "The premier HR qualification in Kenya for aspiring HR Directors and Managers.",
            "category": "HR",
            "duration": "1 Year",
            "link": "https://hrmpeb.or.ke/"
        },
        {
            "title": "AWS Certified Cloud Practitioner",
            "provider": "Amazon Web Services",
            "description": "A global certification for foundational cloud knowledge.",
            "category": "Cloud Computing",
            "duration": "2 Months",
            "link": "https://aws.amazon.com/certification/certified-cloud-practitioner/"
        }
    ]

    for item in qual_data:
        ProfessionalQualification.objects.get_or_create(**item)

    # 3. Simulations (Scenario-Based Learning)
    sim_data = [
        {
            "title": "Audit Junior: First Field Visit",
            "description": "Simulate a site visit to a client office. Learn to verify inventory and check internal controls.",
            "category": "Finance",
            "difficulty": "Beginner",
            "duration_minutes": 45,
            "is_premium": True,
            "created_by": admin_user
        },
        {
            "title": "Software Engineer: Incident Management",
            "description": "A server goes down at 2 AM. Walk through the dashboard, find the logs, and restore service.",
            "category": "Tech",
            "difficulty": "Advanced",
            "duration_minutes": 60,
            "is_premium": True,
            "created_by": admin_user
        }
    ]

    for item in sim_data:
        if not Simulation.objects.filter(title=item['title']).exists():
            Simulation.objects.create(**item)

    # 4. Events
    event_data = [
        {
            "title": "Kenya Tech Summit 2026",
            "organizer": "Safaricom & Partners",
            "description": "The largest gathering of tech talent and innovators in East Africa.",
            "location": "Sarit Expo Centre, Nairobi",
            "date": date.today() + timedelta(days=30),
            "category": "Networking",
            "created_by": admin_user
        }
    ]

    for item in event_data:
        if not Event.objects.filter(title=item['title']).exists():
            Event.objects.create(**item)

    print("Successfully populated discovery data!")

if __name__ == "__main__":
    populate()
