import os
import django
import sys
import re

# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GradPulse.settings')
django.setup()

from accounts.models import UniSmartMasterCourse
from cluster_map import CLUSTER_NAMES

def import_all():
    if not os.path.exists('kuccps_manual_extra.txt'):
        print("Missing kuccps_manual_extra.txt")
        return

    with open('kuccps_manual_extra.txt', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split by Cluster
    # Pattern to find Cluster ID: Digit(s) optionally followed by a letter, at start of line
    # We use finditer to get positions
    cluster_starts = []
    # Match digit+optional letter at start of line, followed by space or newline
    for m in re.finditer(r'(?:\n|^)(\d+[A-Z]?)(?:\s+|$)', content):
        cluster_id = m.group(1)
        # Avoid page numbers (e.g. "© ... Page 1 of 11")
        # Check context: if followed by "of 11" it's a page number
        context = content[m.end():m.end()+10]
        if "of" in context.lower(): continue
        if len(cluster_id) > 3: continue # Likely not a cluster ID
        cluster_starts.append(m)
    
    total = 0
    for i in range(len(cluster_starts)):
        start_idx = cluster_starts[i].start()
        end_idx = cluster_starts[i+1].start() if i+1 < len(cluster_starts) else len(content)
        
        cluster_id = cluster_starts[i].group(1)
        cluster_body = content[start_idx:end_idx]
        
        cluster_display_name = CLUSTER_NAMES.get(cluster_id, f"Cluster {cluster_id}")
        
        # Extract requirements
        req_match = re.search(r'(Subject\s+1.*?\n.*?\n.*?\n.*?\n)', cluster_body, re.DOTALL | re.IGNORECASE)
        requirements = req_match.group(1).replace('\n', ' ').strip() if req_match else "See manual for requirements"
        # Cleanup requirements
        requirements = re.sub(r'\s+', ' ', requirements).strip()
        
        # Extract all "Bachelor" lines
        # Sometimes they are multiple on one line
        raw_courses = re.findall(r'(Bachelor\s+(?:of|in|to)\s+[\w\s\(\),&/]+)', cluster_body, re.IGNORECASE)
        
        for cname in raw_courses:
            cname = cname.strip()
            # Cleanup common PDF copy artifacts
            cname = re.sub(r'©.*Page \d+ of \d+', '', cname)
            cname = cname.split('©')[0].strip()
            if len(cname) < 15: continue # Skip short/invalid matches
            if "Copyright" in cname: continue
            
            # Generate unique code
            clean_name = re.sub(r'[^a-zA-Z\s]', '', cname)
            words = [w[:3].upper() for w in clean_name.split() if len(w) >= 3]
            # Use cluster + first 4 words
            code = f"{cluster_id}-{''.join(words[:4])}"
            
            # Shorten code if it's too long (>50 is the limit in model)
            if len(code) > 45: code = code[:45]

            try:
                course, created = UniSmartMasterCourse.objects.update_or_create(
                    code=code,
                    defaults={
                        "name": cname,
                        "cluster_group": cluster_display_name,
                        "requirements": requirements,
                        "institution": "Various Universities",
                        "level": 'degree'
                    }
                )
                if created:
                    total += 1
                # print(f"Imported: {cname} | {cluster_display_name}")
            except Exception as e:
                # print(f"Error for {cname}: {e}")
                pass

    print(f"\nFinal Import Result: {total} new courses added.")

if __name__ == "__main__":
    import_all()
