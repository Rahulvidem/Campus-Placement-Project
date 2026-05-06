# 🎓 Campus Placement Eligibility Dashboard
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

## 🛠️ Tech Stack

- **Python** — Core language
- **Pandas** — Data processing & filtering
- **Streamlit** — Web application framework
- **Plotly** — Interactive charts & visualizations
- **OpenPyXL** — Excel export
