"""
data_cleaning.py
Data Cleaning & Validation for Campus Placement Dataset
AIML-F | Samhita Iyengar · Sharvani Karnam · Videm Rahul
"""

import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    'Student_ID', 'Student_Name', 'Gender', 'Branch', 'Year_of_Study',
    'CGPA', '10th_Percentage', '12th_Percentage',
    'Active_Backlogs', 'History_of_Backlogs',
    'Skills', 'Certifications', 'Internships_Completed', 'Placed_Status'
]

VALID_BRANCHES = ['CSE', 'AIML', 'ECE', 'IT', 'EEE', 'MECH', 'CIVIL', 'CHEM']
VALID_GENDER = ['Male', 'Female', 'Other']
VALID_PLACED = ['Yes', 'No']
VALID_YEARS = ['1st Year', '2nd Year', '3rd Year', '4th Year']


def validate_and_clean(df: pd.DataFrame, verbose=True) -> tuple[pd.DataFrame, dict]:
    """
    Full data cleaning and validation pipeline.
    Returns cleaned DataFrame and a report dict.
    """
    report = {
        'original_rows': len(df),
        'issues_found': [],
        'rows_dropped': 0,
        'columns_fixed': []
    }

    def log(msg):
        report['issues_found'].append(msg)
        if verbose:
            print(f"[CLEAN] {msg}")

    # ── Step 1: Check required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        log(f"Missing columns: {missing_cols}")
        for col in missing_cols:
            df[col] = np.nan

    # ── Step 2: Remove complete duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    if len(df) < before:
        log(f"Removed {before - len(df)} duplicate rows")

    # ── Step 3: Remove duplicate Student_IDs
    before = len(df)
    df.drop_duplicates(subset='Student_ID', keep='first', inplace=True)
    if len(df) < before:
        log(f"Removed {before - len(df)} duplicate Student IDs")

    # ── Step 4: CGPA cleaning
    df['CGPA'] = pd.to_numeric(df['CGPA'], errors='coerce')
    invalid_cgpa = df['CGPA'].isna() | (df['CGPA'] < 0) | (df['CGPA'] > 10)
    if invalid_cgpa.sum() > 0:
        log(f"Fixing {invalid_cgpa.sum()} invalid CGPA values → median")
        median_cgpa = df.loc[~invalid_cgpa, 'CGPA'].median()
        df.loc[invalid_cgpa, 'CGPA'] = round(median_cgpa, 2)
        report['columns_fixed'].append('CGPA')
    df['CGPA'] = df['CGPA'].round(2)

    # ── Step 5: Percentage cleaning
    for col in ['10th_Percentage', '12th_Percentage']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        invalid = df[col].isna() | (df[col] < 0) | (df[col] > 100)
        if invalid.sum() > 0:
            log(f"Fixing {invalid.sum()} invalid {col} values → median")
            df.loc[invalid, col] = df.loc[~invalid, col].median()
            report['columns_fixed'].append(col)
        df[col] = df[col].round(1)

    # ── Step 6: Backlogs cleaning
    for col in ['Active_Backlogs', 'History_of_Backlogs']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        df[col] = df[col].clip(lower=0)
    # History >= Active
    df['History_of_Backlogs'] = df[['Active_Backlogs','History_of_Backlogs']].max(axis=1)

    # ── Step 7: Branch standardization
    df['Branch'] = df['Branch'].astype(str).str.upper().str.strip()
    invalid_branch = ~df['Branch'].isin(VALID_BRANCHES)
    if invalid_branch.sum() > 0:
        log(f"{invalid_branch.sum()} invalid branch values → 'CSE'")
        df.loc[invalid_branch, 'Branch'] = 'CSE'
        report['columns_fixed'].append('Branch')

    # ── Step 8: Gender standardization
    df['Gender'] = df['Gender'].astype(str).str.capitalize().str.strip()
    invalid_gender = ~df['Gender'].isin(VALID_GENDER)
    if invalid_gender.sum() > 0:
        df.loc[invalid_gender, 'Gender'] = 'Other'

    # ── Step 9: Placed_Status standardization
    df['Placed_Status'] = df['Placed_Status'].astype(str).str.capitalize().str.strip()
    invalid_placed = ~df['Placed_Status'].isin(VALID_PLACED)
    if invalid_placed.sum() > 0:
        df.loc[invalid_placed, 'Placed_Status'] = 'No'

    # ── Step 10: Year_of_Study standardization
    df['Year_of_Study'] = df['Year_of_Study'].astype(str).str.strip()
    invalid_year = ~df['Year_of_Study'].isin(VALID_YEARS)
    if invalid_year.sum() > 0:
        df.loc[invalid_year, 'Year_of_Study'] = '1st Year'

    # ── Step 11: Internships
    df['Internships_Completed'] = pd.to_numeric(
        df['Internships_Completed'], errors='coerce').fillna(0).astype(int).clip(0, 10)

    # ── Step 12: Skills / Certifications — clean whitespace
    df['Skills'] = df['Skills'].astype(str).str.strip()
    df['Certifications'] = df['Certifications'].astype(str).str.strip()

    # ── Step 13: Student_Name — clean
    df['Student_Name'] = df['Student_Name'].astype(str).str.strip().str.title()

    report['final_rows'] = len(df)
    report['rows_dropped'] = report['original_rows'] - len(df)

    if verbose:
        print(f"\n✅ Cleaning complete.")
        print(f"   Original rows : {report['original_rows']:,}")
        print(f"   Final rows    : {report['final_rows']:,}")
        print(f"   Rows dropped  : {report['rows_dropped']:,}")
        print(f"   Issues found  : {len(report['issues_found'])}")

    return df.reset_index(drop=True), report


if __name__ == "__main__":
    df = pd.read_csv("students_dataset.csv")
    clean_df, report = validate_and_clean(df, verbose=True)
    clean_df.to_csv("students_clean.csv", index=False)
    print("\nCleaned dataset saved to students_clean.csv")
