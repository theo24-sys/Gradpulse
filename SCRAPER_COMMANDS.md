# 🚀 GradPulse Scraper CLI Cheat Sheet

Run these commands from your project root (`c:\Users\USER\Desktop\GradPulse`) to populate your database via the Apify cloud.

### **🌟 Master Command**
| Action | Command |
| :--- | :--- |
| **Run EVERYTHING** | `python manage.py crawl all` |

---

### **🗂️ Commands by Category**

#### **🏛️ Government & Youth Programs**
*Includes: PSC Kenya, NYS, Ajira Digital, NYOTA Project, Youth Empowerment Centres.*
- `python manage.py crawl gov`

#### **🌍 NGOs & International Orgs**
*Includes: UN Kenya, ReliefWeb, World Vision, CAP YEI, Generation Kenya.*
- `python manage.py crawl ngos`

#### **🎓 Scholarships**
*Includes: Scholarship Positions, ScholarshipSet.*
- `python manage.py crawl scholarships`

#### **💼 Internships & Jobs**
*Includes: BrighterMonday, MyJobMag, LinkedIn, CFK Africa, MultiWork.*
- `python manage.py crawl jobs`

#### **📜 Certifications & Credentials**
*Includes: Microsoft, Google Grow, IBM, Coursera, ISACA, ITCILO, Leadership KE.*
- `python manage.py crawl learning`
- *Alias: `python manage.py crawl certs`*
- *Alias: `python manage.py crawl credentials`*

#### **📅 Career Fairs & Events**
*Includes: Post Training Fairs, Education Fairs Africa, AllConferenceAlert, NLBH Events, Conference Alerts Nairobi.*
- `python manage.py crawl events`
- *Alias: `python manage.py crawl fairs`*
- *Alias: `python manage.py crawl networking`*

---

### **⚠️ Remember: Build First**
After making changes to scrapers, always click **"Build"** in your [Apify Console](https://console.apify.com) to deploy the code to the cloud!
