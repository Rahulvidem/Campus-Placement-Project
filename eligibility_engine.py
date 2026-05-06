"""
eligibility_engine.py
Campus Placement Eligibility Engine
AIML-F | Samhita Iyengar · Sharvani Karnam · Videm Rahul
"""

import pandas as pd

# ─── COMPANY ELIGIBILITY RULES ──────────────────────────────────────────────
COMPANIES = {
    "TCS": {
        "min_cgpa": 6.0, "max_backlogs": 0,
        "branches": ["CSE","AIML","ECE","IT","EEE"],
        "skills": [], "package": "3.5 LPA"
    },
    "Infosys": {
        "min_cgpa": 6.5, "max_backlogs": 0,
        "branches": ["CSE","AIML","IT"],
        "skills": ["Python"], "package": "4.0 LPA"
    },
    "Wipro": {
        "min_cgpa": 6.0, "max_backlogs": 1,
        "branches": ["CSE","AIML","ECE","IT","EEE","MECH"],
        "skills": [], "package": "3.5 LPA"
    },
    "Accenture": {
        "min_cgpa": 6.5, "max_backlogs": 0,
        "branches": ["CSE","AIML","IT","ECE"],
        "skills": [], "package": "4.5 LPA"
    },
    "Cognizant": {
        "min_cgpa": 6.0, "max_backlogs": 0,
        "branches": ["CSE","AIML","IT","ECE","EEE"],
        "skills": [], "package": "4.0 LPA"
    },
    "HCL": {
        "min_cgpa": 5.5, "max_backlogs": 1,
        "branches": ["CSE","AIML","ECE","IT","EEE","MECH"],
        "skills": [], "package": "3.0 LPA"
    },
    "Google": {
        "min_cgpa": 8.5, "max_backlogs": 0,
        "branches": ["CSE","AIML"],
        "skills": ["Python","DSA"], "package": "25+ LPA"
    },
    "Amazon": {
        "min_cgpa": 7.5, "max_backlogs": 0,
        "branches": ["CSE","AIML","IT"],
        "skills": ["Python","DSA"], "package": "18 LPA"
    },
    "Microsoft": {
        "min_cgpa": 8.0, "max_backlogs": 0,
        "branches": ["CSE","AIML"],
        "skills": ["Python"], "package": "20 LPA"
    },
    "Deloitte": {
        "min_cgpa": 7.0, "max_backlogs": 0,
        "branches": ["CSE","AIML","IT","ECE","MECH","CIVIL"],
        "skills": [], "package": "7 LPA"
    },
}


def is_eligible(student_row: dict, company_rules: dict) -> tuple[bool, list]:
    """
    Check if a student is eligible for a company.
    Returns: (is_eligible: bool, rejection_reasons: list)
    """
    reasons = []

    if student_row.get('CGPA', 0) < company_rules['min_cgpa']:
        reasons.append(f"CGPA {student_row['CGPA']} < required {company_rules['min_cgpa']}")

    if student_row.get('Active_Backlogs', 0) > company_rules['max_backlogs']:
        reasons.append(f"Active backlogs {student_row['Active_Backlogs']} > allowed {company_rules['max_backlogs']}")

    if student_row.get('Branch', '') not in company_rules['branches']:
        reasons.append(f"Branch {student_row['Branch']} not in {company_rules['branches']}")

    student_skills = [s.strip() for s in str(student_row.get('Skills', '')).split(',')]
    for skill in company_rules['skills']:
        if skill not in student_skills:
            reasons.append(f"Missing required skill: {skill}")

    return len(reasons) == 0, reasons


def run_eligibility_engine(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run eligibility filtering on full student dataframe.
    Adds 'Eligible_Companies' and 'Eligible_Count' columns.
    """
    df = df.copy()

    def get_eligible_companies(row):
        eligible = []
        for company, rules in COMPANIES.items():
            passed, _ = is_eligible(row.to_dict(), rules)
            if passed:
                eligible.append(company)
        return ', '.join(eligible) if eligible else 'None'

    print("Running eligibility engine on", len(df), "students...")
    df['Eligible_Companies'] = df.apply(get_eligible_companies, axis=1)
    df['Eligible_Count'] = df['Eligible_Companies'].apply(
        lambda x: 0 if x == 'None' else len(x.split(', '))
    )
    print("Done! Eligible students:", int((df['Eligible_Count'] > 0).sum()))
    return df


def get_company_eligible_students(df: pd.DataFrame, company: str) -> pd.DataFrame:
    """Return dataframe of students eligible for a specific company."""
    if company not in COMPANIES:
        raise ValueError(f"Company '{company}' not found.")
    rules = COMPANIES[company]
    mask = df.apply(lambda row: is_eligible(row.to_dict(), rules)[0], axis=1)
    return df[mask].copy()


def generate_eligibility_report(df: pd.DataFrame) -> dict:
    """Generate a summary report of eligibility statistics."""
    df = run_eligibility_engine(df)
    report = {
        'total_students': len(df),
        'eligible_any': int((df['Eligible_Count'] > 0).sum()),
        'not_eligible': int((df['Eligible_Count'] == 0).sum()),
        'multi_eligible_3plus': int((df['Eligible_Count'] >= 3).sum()),
        'avg_cgpa': round(df['CGPA'].mean(), 2),
        'zero_backlogs': int((df['Active_Backlogs'] == 0).sum()),
        'placed': int((df['Placed_Status'] == 'Yes').sum()),
        'per_company': {}
    }
    for company, rules in COMPANIES.items():
        eligible_df = get_company_eligible_students(df, company)
        report['per_company'][company] = {
            'eligible_count': len(eligible_df),
            'avg_cgpa': round(eligible_df['CGPA'].mean(), 2) if len(eligible_df) > 0 else 0,
            'package': rules['package']
        }
    return report


if __name__ == "__main__":
    df = pd.read_csv("students_dataset.csv")
    report = generate_eligibility_report(df)
    print("\n=== CAMPUS PLACEMENT ELIGIBILITY REPORT ===")
    print(f"Total Students     : {report['total_students']:,}")
    print(f"Eligible (any co.) : {report['eligible_any']:,}")
    print(f"Not Eligible       : {report['not_eligible']:,}")
    print(f"Multi-eligible 3+  : {report['multi_eligible_3plus']:,}")
    print(f"Average CGPA       : {report['avg_cgpa']}")
    print(f"Zero Backlogs      : {report['zero_backlogs']:,}")
    print(f"Already Placed     : {report['placed']:,}")
    print("\n--- Company-wise ---")
    for company, stats in report['per_company'].items():
        print(f"{company:12s}: {stats['eligible_count']:5,} eligible | Avg CGPA: {stats['avg_cgpa']} | Package: {stats['package']}")
