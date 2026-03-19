import json
import os
from django.conf import settings

def get_institution_choices():
    """Reads kenya_institutions.json and returns Django-compatible grouped choices."""
    json_path = os.path.join(settings.BASE_DIR, 'data', 'kenya_institutions.json')
    choices = [('', '— Select Institution —')]
    
    if not os.path.exists(json_path):
        return choices
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for category, institutions in data.items():
            category_name = category.replace('_', ' ').title()
            category_choices = []
            
            for inst in institutions:
                name = inst.get('name', 'Unknown')
                category_choices.append((name, name))
            
            # Sort choices alphabetically within category
            category_choices.sort(key=lambda x: x[1])
            choices.append((category_name, tuple(category_choices)))
            
    except Exception as e:
        print(f"Error loading institutions JSON: {e}")
        
    return choices
