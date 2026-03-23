const clusters_part2 = [
  {
    id: 'c11', num: '11', name: 'Fashion, Design & Sports', icon: '👗', color: '#ec4899', group: 'arts',
    requirements: 'CHE – C (PLAIN) | Various combinations',
    subclusters: [
      { id: '11A', name: 'Cluster 11A — Fashion & Design', courses: ['Bachelor of Arts (Interior Design With IT)','Bachelor of Arts (Textiles Apparel Design and Fashion Merchandising With IT)','Bachelor of Science (Apparel & Fashion Technology)','Bachelor of Science (Clothing Textile & Interior Design)','Bachelor of Science (Fashion Design & Marketing)','Bachelor of Science (Fashion Design and Textile Technology)','Bachelor of Science in Fashion Design and Marketing'] },
      { id: '12A', name: 'Cluster 12A — Sports Science', courses: ['Bachelor of Science (Health Promotion and Sports Science)','Bachelor of Science (Exercise & Sport Science)','Bachelor of Science (Recreation and Sports Management)','Bachelor of Sports Science & Management','Bachelor of Sports Management'] }
    ]
  },
  {
    id: 'c13', num: '13', name: 'Medicine, Health & Nursing', icon: '🏥', color: '#10b981', group: 'health',
    requirements: 'BIO – B (PLAIN) | CHE – B (PLAIN) | MAT ALT A/PHY – B (PLAIN)',
    subclusters: [
      { id: '13A', name: 'Cluster 13A — Medicine & Dentistry', courses: ['Bachelor of Dental Surgery','Bachelor of Medicine & Bachelor of Surgery','Bachelor of Medicine & Bachelor of Surgery (M.B.Ch.B)','Bachelor of Medicine and Bachelor of Surgery','Bachelor of Medicine and Bachelor of Surgery (M.B.Ch.B)','Bachelor of Medicine and Bachelor of Surgery (With IT)'] },
      { id: '13B', name: 'Cluster 13B — Pharmacy & Nursing', courses: ['Bachelor of Pharmacy','Bachelor of Science (Pharmaceutical Sciences With IT)','Bachelor of Science (Nursing With IT)','Bachelor of Science (Nursing)','Bachelor of Science in Nursing','Bachelor of Science (Nursing Science)','Bachelor of Science (Medical Laboratory Science & Technology)','Bachelor of Science (Medical Laboratory Sciences)','Bachelor of Science (Medical Laboratory)'] },
      { id: '13C', name: 'Cluster 13C — Clinical Medicine & Public Health', courses: ['Bachelor of Technology (Community and Public Health)','Bachelor of Science (Occupational Health & Safety)','Bachelor of Science in Medical Laboratory Sciences','Bachelor of Technology (Medical Laboratory Science)','Bachelor of Science in Clinical Medicine and Community Health','Bachelor of Science Clinical Medicine','Bachelor of Science in Clinical Medicine Surgery and Community Health','Bachelor of Science in Public Health','Bachelor of Science in Midwifery with Reproductive Health','Bachelor of Science (Environmental Health)','Bachelor of Science in Environmental Health','Bachelor of Science in Environmental Health Sciences (Public Health)','Bachelor of Science (Optometry and Vision Sciences)','Bachelor of Science (Physical Therapy)','Bachelor of Physiotherapy','Bachelor of Science in Physiotherapy','Bachelor of Science (Public Health With IT)','Bachelor of Science in Public Health','Bachelor of Science (Public Health)'] },
      { id: '13D', name: 'Cluster 13D — Veterinary Medicine', courses: ['Bachelor of Veterinary Medicine'] },
      { id: '13E', name: 'Cluster 13E — Community & Population Health', courses: ['Bachelor of Science (Biostatistics)','Bachelor of Science in Biostatistics','Bachelor of Science in Epidemiology and Biostatistics','Bachelor of Science in Community Health','Bachelor of Science in Global Health and Emporiatrics','Bachelor of Science in Health Systems Management','Bachelor of Health Services Management','Bachelor of Science in Occupational Therapy','Bachelor of Population Health','Bachelor of Science (Community Health and Development)','Bachelor of Science in Community Health and Development','Bachelor of Science in Community Health Education','Bachelor of Science (Population Health)','Bachelor of Science (Community Health & Development)','Bachelor of Science (Health Records and Informatics)','Bachelor of Science in Health Records and Information Management','Bachelor of Science (Health Records & Information Management)','Bachelor of Science (Health Records and Information Management with IT)','Bachelor of Science in Health Records Management & Informatics','Bachelor of Science (Medical Psychology)'] },
      { id: '13F', name: 'Cluster 13F — Biomedical Sciences', courses: ['Bachelor of Science (Biomedical Science and Technology)','Bachelor of Science in Biomedical Science and Technology','Bachelor of Science (Biomedical Science & Technology)','Bachelor of Science (Laboratory Sciences)','Bachelor of Technology (Science Laboratory Technology)'] },
      { id: '13G', name: 'Cluster 13G — Nutrition & Dietetics', courses: ['Bachelor of Science (Food Nutrition and Dietetics)','Bachelor of Science in Food Nutrition and Dietetics','Bachelor of Science (Food Science and Nutrition)','Bachelor of Science in Food Science and Nutrition','Bachelor of Science (Nutrition and Dietetics With IT)','Bachelor of Science in Human Nutrition and Dietetics','Bachelor of Science (Food Nutrition & Dietetics)','Bachelor of Technology (Nutrition and Dietetics)','Bachelor of Science (Food Science & Nutrition)','Bachelor of Science (Human Nutrition and Dietetics)','Bachelor of Science (Food, Nutrition & Dietetics)'] }
    ]
  },
  {
    id: 'c14', num: '14', name: 'History & Social Development', icon: '📜', color: '#64748b', group: 'arts',
    requirements: 'HAG – C+ | ENG/KIS',
    subclusters: [
      { id: '14A', name: 'Cluster 14A — History & Social Sciences', courses: ['Bachelor of Arts History and Archaeology)','Bachelor of Arts (History)','Bachelor of Arts (History and Archaeology With IT)','Bachelor of Arts in History & International Studies','Bachelor of Arts (Social Work)','Bachelor of Social Work and Administration','Bachelor of Arts (Sociology and Anthropology With IT)','Bachelor of Conflict Resolution and Humanitarian Assistance','Bachelor of Arts (Sociology)','Bachelor of Science in Sociology','Bachelor of Science in Public Administration and Leadership','Bachelor of Science (Disaster Mitigation and Sustainable Development)','Bachelor of Science in Medical Social Work','Bachelor of Science (Disaster Risk Management and Sustainable Development)','Bachelor of Arts (Disaster Management With IT)','Bachelor of Disaster Management & International Diplomacy','Bachelor of Arts in Community Development','Bachelor of Science (Disaster Preparedness and Environment Technology)','Bachelor of Arts (Peace and Conflict Studies)','Bachelor of Arts Community Development','Bachelor of Community Development','Bachelor of Development Studies','Bachelor of Arts in Development Studies','Bachelor of Arts (Gender)','Bachelor of Science (Community Development)','Bachelor of Science in Community Development','Bachelor of Science (Public Management and Development)','Bachelor of Public Management and Development','Bachelor of Science in Development Studies','Bachelor of Arts (Developmental and Policy Studies)','Bachelor of Arts in Management','Bachelor of Arts in Leadership and Philosophy','Bachelor of Science (Community Development and Environment)','Bachelor of Community Development and Environment','Bachelor of Science (Community Resource Management)'] }
    ]
  },
  {
    id: 'c15', num: '15', name: 'Agriculture, Environment & Natural Resources', icon: '🌿', color: '#10b981', group: 'science',
    requirements: 'BIO – C+ | Various combinations',
    subclusters: [
      { id: '15A', name: 'Cluster 15A — Animal Health & Production', courses: ['Bachelor of Science (Animal Health & Production)','Bachelor of Science (Animal Health and Production)','Bachelor of Science (Animal Health Production & Processing)','Bachelor of Science (Animal Production & Health Management)','Bachelor of Science in Animal Health Management','Bachelor of Science in Animal Production','Bachelor of Science in Applied Animal Laboratory Science'] },
      { id: '15B', name: 'Cluster 15B — Animal Science', courses: ['Bachelor of Science (Animal Science & Management)','Bachelor of Science (Animal Science With IT)','Bachelor of Science in Animal Science','Bachelor of Science in Animal Science & Technology','Bachelor of Science in Animal Products Technology'] },
      { id: '15E', name: 'Cluster 15E — Food Science & Technology', courses: ['Bachelor of Science (Food Processing Technology)','Bachelor of Science in Food Science & Technology','Bachelor of Science (Food Science & Technology)','Bachelor of Science (Food Science and Management)','Bachelor of Science (Food Science and Technology)','Bachelor of Science (Food Security)','Bachelor of Science in Food Technology & Quality Assurance','Bachelor of Science in Maritime Management (Commercial)','Bachelor of Science (Applied Aquatic Science)','Bachelor of Science (Fisheries & Aquatic Sciences)','Bachelor of Science in Aquaculture and Fisheries Technology','Bachelor of Science in Fisheries and Oceanography','Bachelor of Science in Marine Resource Management','Bachelor of Science (Coastal & Marine Resource Management)','Bachelor of Science (Marine Biology & Fisheries)','Bachelor of Science (Fisheries and Aquaculture Management)','Bachelor of Science (Fisheries and Aquaculture With IT)','Bachelor of Science Fisheries Management and Aquaculture Technology','Bachelor of Science in Fisheries and Aquaculture'] },
      { id: '15F', name: 'Cluster 15F — Environmental Science', courses: ['Bachelor of Technology (Environmental Resource Management)','Bachelor of Science (Environmental Management)','Bachelor of Science (Environmental Science With IT)','Bachelor of Science (Environmental Science)','Bachelor of Science in Environmental Science and Technology','Bachelor of Science (Environmental Sciences)','Bachelor of Environmental Studies (Community Development)','Bachelor of Science (Agriculture and Biotechnology)','Bachelor of Science (Bio-resources Management and Conservation)','Bachelor of Environmental Planning & Development Management','Bachelor of Environmental Studies and Community Development','Bachelor of Science in Environment Lands and Sustainable Development','Bachelor of Science in Natural Resources','Bachelor of Science (Natural Resource Management)','Bachelor of Science in Natural Resources Management','Bachelor of Environmental (Environmental Resource Conservation)','Bachelor of Environmental Science','Bachelor of Environmental Studies','Bachelor of Science in Environmental Studies','Bachelor of Environmental Studies (Arts)','Bachelor of Environmental Studies (Science)','Bachelor of Science in Environmental Science','Bachelor of Environmental Education'] },
      { id: '15G', name: 'Cluster 15G — Agriculture & Forestry', courses: ['Bachelor of Science (Natural Resources Management)','Bachelor of Science (Environmental Horticulture & Landscaping Technology)','Bachelor of Science (Forestry)','Bachelor of Science (Horticulture)','Bachelor of Science in Horticulture','Bachelor of Science in Horticultural Science & Management','Bachelor of Science Horticulture','Bachelor of Science (Wildlife Enterprises & Management)','Bachelor of Science in Wildlife Enterprise & Management','Bachelor of Science (Dryland Agriculture & Enterprise Development)','Bachelor of Science in Natural Resource Management','Bachelor of Science (Dryland Animal Science)','Bachelor of Science in Soil Environment & Land Use Management)','Bachelor of Science (Seed Science & Technology)','Bachelor of Science (Nutraceutical Science and Technology)','Bachelor of Science (Agroforestry & Rural Development)','Bachelor of Science in Nutraceutical Science and Technology','Bachelor of Science (Aquatic Resources Conservation and Development With IT)','Bachelor of Science (Utilization & Sustainability of Arid Lands (Usal))','Bachelor of Science in Agriculture','Bachelor of Science (Wildlife Management)','Bachelor of Science (Agricultural Biotechnology)','Bachelor of Science (Horticultural Science & Management)','Bachelor of Science (Horticulture With IT)','Bachelor of Science (Range Management)','Bachelor of Science (Bio-resources Management and Conservation)','Bachelor of Science (Integrated Forest Resources Management)','Bachelor of Science (Natural Products)','Bachelor of Science (Climate Change and Development With IT)','Bachelor of Science (Crop Improvement & Protection)','Bachelor of Science (Waste Management)','Bachelor of Science (Water Resource Management)','Bachelor of Science in Ethno botany','Bachelor of Science (Agriculture & Human Ecology Extension)','Bachelor of Science (Agriculture and Enterprise Development)','Bachelor of Science (Dairy Technology & Management)','Bachelor of Science (Leather Technology)','Bachelor of Science (Soil Science)','Bachelor of Science (Soils & Land Use Management)','Bachelor of Science (Water and Environment Management)','Bachelor of Science (Wood Science and Industrial Processes)','Bachelor of Science in Water and Environment Management','Bachelor of Science (Land Resource Management)','Bachelor of Science (Dryland Agriculture)','Bachelor of Science (Wildlife Management)'] }
    ]
  },
  {
    id: 'c16', num: '16', name: 'Geography & Natural Resources', icon: '🗺️', color: '#06b6d4', group: 'science',
    requirements: 'GEO – C+ | MAT ALT A/B',
    subclusters: [
      { id: '16A', name: 'Cluster 16A — Geography', courses: ['Bachelor of Arts (Geography)','Bachelor of Science (Geography)','Bachelor of Arts (Geography and Economics)','Bachelor of Arts (Kiswahili and Geography)','Bachelor of Science (Geography and Natural Resource Management With IT)','Bachelor of Science (Environmental Conservation and Natural Resources Management)','Bachelor of Science (Land Resource Planning & Management)','Bachelor of Science (Agronomy With IT)','Bachelor of Science in Land Resource Planning & Management','Bachelor of Arts (Planning)'] }
    ]
  },
  {
    id: 'c17', num: '17', name: 'French & German', icon: '🌐', color: '#8b5cf6', group: 'arts',
    requirements: 'FRE/GER – C+ | ENG/KIS',
    subclusters: [
      { id: '17A', name: 'Cluster 17A — Foreign Languages', courses: ['Bachelor of Arts (French)','Bachelor of Arts (French With IT)','Bachelor of Arts (German)'] }
    ]
  },
  {
    id: 'c18', num: '18', name: 'Music', icon: '🎵', color: '#f59e0b', group: 'arts',
    requirements: 'MUS – C+ | ENG/KIS',
    subclusters: [
      { id: '18A', name: 'Cluster 18A — Music', courses: ['Bachelor of Arts (Music)','Bachelor of Arts (Music With IT)','Bachelor of Music','Bachelor of Music (Technology)'] }
    ]
  },
  {
    id: 'c19', num: '19', name: 'Education', icon: '🎓', color: '#3b82f6', group: 'education',
    requirements: 'Various combinations – C+',
    subclusters: [
      { id: '19A', name: 'Cluster 19A — Science Education', courses: ['Bachelor of Science with Education','Bachelor of Education (Science)','Bachelor of Education (Science With IT)','Bachelor of Education (Science with IT)'] },
      { id: '19B', name: 'Cluster 19B — Arts Education', courses: ['Bachelor of Education (Arts)','Bachelor of Education (Early Childhood Development Education)','Bachelor of Education (Early Childhood Development)','Bachelor of Education (Early Childhood Education)','Bachelor of Education (Early Childhood Education With IT)','Bachelor of Education (Early Childhood)','Bachelor of Education in Early Childhood Education','Bachelor of Education (Library Science)','Bachelor of Education Arts','Bachelor of Education (Early Childhood and Primary Education)','Bachelor of Arts (With Education)','Bachelor of Education (Arts) With Guidance and Counselling','Bachelor of Education (Arts With IT)','Bachelor of Education (Home Science and Technology)','Bachelor of Education (Guidance and Counselling)','Bachelor of Education Arts (Home Economics)'] },
      { id: '19D', name: 'Cluster 19D — Physical Education', courses: ['Bachelor of Education (Physical Education and Sports)','Bachelor of Education (Physical Education)'] },
      { id: '19E', name: 'Cluster 19E — Special Needs & Visual Arts', courses: ['Bachelor of Education (Special Needs Education - Secondary Option)','Bachelor of Education (Special Needs Education)','Bachelor of Education (Visual and Performing Arts)'] },
      { id: '19F', name: 'Cluster 19F — French Education', courses: ['Bachelor of Education (French)','Bachelor of Education (French With IT)'] },
      { id: '19G', name: 'Cluster 19G — Business Studies Education', courses: ['Bachelor of Education Arts(Business Studies)'] },
      { id: '19H', name: 'Cluster 19H — Fine Arts Education', courses: ['Bachelor of Education (Arts) Fine Art'] },
      { id: '19I', name: 'Cluster 19I — Music Education', courses: ['Bachelor of Education (Music)','Bachelor of Education (Music With IT)','Bachelor of Education (German)','Bachelor of Education (Arts) German'] },
      { id: '19J', name: 'Cluster 19J — Agricultural Education', courses: ['Bachelor of Agricultural Education & Extension','Bachelor of Agricultural Education and Extension','Bachelor of Science in Agricultural Extension','Bachelor of Science (Agriculture Education and Extension)','Bachelor of Science Agricultural Extension and Education','Bachelor of Science (Agricultural Extension Education)','Bachelor of Science (Agricultural Education & Extension)','Bachelor of Science (Agricultural Extension and Education)','Bachelor of Science (Agriculture Education & Extension)','Bachelor of Science (Agriculture Education and Extension With IT)'] },
      { id: '19K', name: 'Cluster 19K — Computer Studies Education', courses: ['Bachelor of Education (Computer Studies)','Bachelor of Education (ICT)','Bachelor of Education (Agriculture)'] }
    ]
  },
  {
    id: 'c20', num: '20', name: 'Religious Studies & Theology', icon: '✝️', color: '#64748b', group: 'arts',
    requirements: 'CRE/IRE/HRE – C+ | ENG/KIS – C (PLAIN)',
    subclusters: [
      { id: '20A', name: 'Cluster 20A — Religion & Theology', courses: ['Bachelor of Arts (Religion With IT)','Bachelor of Arts in Sociology and Religious Studies','Bachelor of Arts (Religious Studies)','Bachelor of Arts (Theology With IT)','Bachelor of Arts (Sociology & Religion)','Bachelor of Theology','Bachelor of Arts in Intercultural Studies','Bachelor of Arts in Biblical Studies','Bachelor of Arts in Islamic Studies','Bachelor of Arts in Church Education Ministries','Bachelor of Arts in Islamic Sharia','Bachelor of Arts in Christian Ministries'] }
    ]
  }
];

const clusters = [...clusters_part1, ...clusters_part2];

let activeGroup = 'all';
let searchQuery = '';

function highlight(text, query) {
  if (!query) return text;
  const re = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`, 'gi');
  return text.replace(re, '<mark>$1</mark>');
}

function countAllCourses() {
  let total = 0;
  clusters.forEach(c => c.subclusters.forEach(s => total += s.courses.length));
  return total;
}

function buildSidebar() {
  const nav = document.getElementById('clusterNav');
  nav.innerHTML = clusters.map(c => `
    <div class="cluster-item" id="nav-${c.id}" onclick="scrollToCluster('${c.id}')">
      <span class="cluster-dot" style="background:${c.color}"></span>
      <span class="cluster-name">${c.num}. ${c.name}</span>
      <span class="cluster-count">${c.subclusters.reduce((a,s)=>a+s.courses.length,0)}</span>
    </div>
  `).join('');
}

function scrollToCluster(id) {
  const el = document.getElementById(`section-${id}`);
  if (el) { el.scrollIntoView({behavior:'smooth', block:'start'}); }
  document.querySelectorAll('.cluster-item').forEach(i => i.classList.remove('active'));
  document.getElementById(`nav-${id}`)?.classList.add('active');
}

function render() {
  const content = document.getElementById('content');
  const csrfToken = document.querySelector('#csrf-form input[name="csrfmiddlewaretoken"]').value;
  let totalVisible = 0;

  const html = clusters.map(c => {
    if (activeGroup !== 'all' && c.group !== activeGroup) return '';

    const subclustersHtml = c.subclusters.map((s, sIndex) => {
      const filtered = s.courses.filter(course =>
        !searchQuery || course.toLowerCase().includes(searchQuery.toLowerCase())
      );
      if (filtered.length === 0) return '';
      totalVisible += filtered.length;

      return `
        <div class="subcluster">
          <div class="subcluster-header">
            <span class="subcluster-title">${s.id} — ${s.name.replace(/^Cluster \\w+ — /,'')}</span>
            <div class="subcluster-line"></div>
            <span style="font-size:11px;color:var(--muted)">${filtered.length} programmes</span>
          </div>
          <div class="course-grid">
            ${filtered.map((course, cIndex) => {
              const safeCourseName = course.replace(/'/g, "&apos;").replace(/"/g, "&quot;");
              const safeInstName = c.name.replace(/'/g, "&apos;").replace(/"/g, "&quot;");
              return `
                <div class="course-card">
                  <div class="course-name">${highlight(course, searchQuery)}</div>
                  <div id="add-btn-${c.id}-${sIndex}-${cIndex}">
                    <button class="add-btn" 
                            hx-post="/unismart/add-to-cart/"
                            hx-headers='{"X-CSRFToken": "${csrfToken}"}'
                            hx-vals='{"course_name": "${safeCourseName}", "course_code": "", "institution": "${safeInstName}"}'
                            hx-target="#add-btn-${c.id}-${sIndex}-${cIndex}"
                            hx-swap="innerHTML"
                            onclick="event.stopPropagation();">
                        <i class="fas fa-plus me-1"></i> Add to Selection
                    </button>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }).join('');

    if (!subclustersHtml.trim()) return '';

    return `
      <div class="cluster-section" id="section-${c.id}">
        <div class="cluster-header">
          <div class="cluster-icon" style="background:${c.color}22;border:1px solid ${c.color}33">${c.icon}</div>
          <div class="cluster-header-text">
            <h2>Cluster ${c.num}: ${c.name}</h2>
            <p>${c.subclusters.reduce((a,s)=>a+s.courses.length,0)} programmes in this cluster</p>
          </div>
        </div>
        <div class="req-badge">
          📋 ${c.requirements}
        </div>
        ${subclustersHtml}
      </div>
    `;
  }).join('');

  content.innerHTML = html || `
    <div class="empty">
      <h3>No programmes found</h3>
      <p>Try a different search term or filter</p>
    </div>
  `;

  document.getElementById('resultsCount').textContent = `${totalVisible} programmes`;
  
  if (window.htmx) {
      window.htmx.process(content);
  }
}

function filterAll(btn) {
  activeGroup = 'all';
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  render();
}

function filterGroup(group, btn) {
  activeGroup = group;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  render();
}

document.getElementById('searchInput').addEventListener('input', function() {
  searchQuery = this.value.trim();
  render();
});

// Init
document.getElementById('totalCourses').textContent = countAllCourses();
buildSidebar();
render();
