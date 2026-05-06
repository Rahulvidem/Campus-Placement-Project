# 🎓 Campus Placement Eligibility Dashboard

**BATCH: AIML-F**
- 24EG107F05 : SAMHITA IYENGAR
- 24EG107F47 : SHARVANI KARNAM
- 24EG107F58 : VIDEM RAHUL

---

## 📦 Project Structure

```
placement_project/
├── app.py                        # Main Streamlit application
├── students_dataset.csv          # Raw 10,000 student dataset
├── students_enriched.csv         # Dataset with eligibility results
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the app
```bash
streamlit run app.py
```

### Step 3 — Open browser
The app will open at: `http://localhost:8501`

---

## 📊 Dashboard Modules

| Module | Description |
|--------|-------------|
| 🏠 Overview | 8 KPI cards + 5 interactive charts |
| 🔍 Student Search | Filter, search, view individual profiles |
| 🏢 Company Analysis | Company-wise eligibility stats & charts |
| 📊 Analytics Deep Dive | CGPA, skills, internship analysis + heatmap |
| ✅ Eligibility Checker | Real-time eligibility check for any student |
| 📥 Export Reports | Download eligible lists as CSV or Excel |

---

## 🏢 Companies & Eligibility Criteria

| Company | Min CGPA | Max Backlogs | Branches | Skills Required |
|---------|----------|--------------|----------|-----------------|
| TCS | 6.0 | 0 | CSE, AIML, ECE, IT, EEE | None |
| Infosys | 6.5 | 0 | CSE, AIML, IT | Python |
| Wipro | 6.0 | 1 | CSE, AIML, ECE, IT, EEE, MECH | None |
| Accenture | 6.5 | 0 | CSE, AIML, IT, ECE | None |
| Cognizant | 6.0 | 0 | CSE, AIML, IT, ECE, EEE | None |
| HCL | 5.5 | 1 | CSE, AIML, ECE, IT, EEE, MECH | None |
| Google | 8.5 | 0 | CSE, AIML | Python, DSA |
| Amazon | 7.5 | 0 | CSE, AIML, IT | Python, DSA |
| Microsoft | 8.0 | 0 | CSE, AIML | Python |
| Deloitte | 7.0 | 0 | CSE, AIML, IT, ECE, MECH, CIVIL | None |

---

## 🗃️ Dataset Fields

| Field | Type | Description |
|-------|------|-------------|
| Student_ID | String | Unique ID (EG00001–EG10000) |
| Student_Name | String | Full name |
| Gender | String | Male/Female |
| Branch | String | CSE/AIML/ECE/IT/EEE/MECH/CIVIL/CHEM |
| Year_of_Study | String | 1st–4th Year |
| CGPA | Float | 4.0–10.0 |
| 10th_Percentage | Float | SSC marks |
| 12th_Percentage | Float | HSC marks |
| Active_Backlogs | Integer | Current backlogs |
| History_of_Backlogs | Integer | Total ever |
| Skills | String | Comma-separated |
| Certifications | String | Comma-separated |
| Internships_Completed | Integer | 0–3 |
| Placed_Status | String | Yes/No |
| Eligible_Companies | String | Auto-computed |
| Eligible_Count | Integer | Auto-computed |

---

## 🛠️ Tech Stack

- **Python** — Core language
- **Pandas** — Data processing & filtering
- **Streamlit** — Web application framework
- **Plotly** — Interactive charts & visualizations
- **OpenPyXL** — Excel export
