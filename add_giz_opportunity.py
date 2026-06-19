import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradpulse.settings')
django.setup()

from opportunities.models import Opportunity

def run():
    op, created = Opportunity.objects.get_or_create(
        title="Empowering Entrepreneurs Call for Applications",
        defaults={
            'type': 'freelance', 
            'sector': 'Manufacturing',
            'location': 'Kiambu, Machakos, Kajiado, Nairobi',
            'description': 'We invite you to the accelerator programme implemented by GIZ in collaboration with Kenya Institute of Business Training (KIBT) and Youth Enterprise Development Fund (YEDF). Aimed at strengthening your business management skills, enhancing financial access, networking and linkages and supporting you to grow and scale your enterprise to the next level.',
            'requirements': 'Eligibility Criteria:\n- Entrepreneur below 35 years operating in Agro-processing and Food value addition, Leather processing, or Textile processing.\n- Enterprise located in Kiambu, Machakos, Kajiado, or Nairobi Counties.\n- Operated enterprise for not more than 7 years.\n- Business has at least 2 employees.\n- Annual turnover of KES 1 Million and above.\n\nApply Link: https://ee-eu.kobotoolbox.org/x/C9J1fKLO',
            'skills_required': 'Business Management, Entrepreneurship, Scaling',
            'deadline': date(2026, 3, 27),
            'status': 'active',
        }
    )

    if created:
        print(f"Created Opportunity: {op.title}. Please upload the poster image via the Admin Panel.")
    else:
        print(f"Opportunity {op.title} already exists.")

if __name__ == '__main__':
    run()
