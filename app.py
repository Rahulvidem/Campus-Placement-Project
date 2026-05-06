import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Campus Placement Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── COMPANY RULES ──────────────────────────────────────────────────────────
COMPANIES = {
    "TCS":        {"min_cgpa": 6.0, "max_backlogs": 0, "branches": ["CSE","AIML","ECE","IT","EEE"], "skills": [], "color": "#0052CC"},
    "Infosys":    {"min_cgpa": 6.5, "max_backlogs": 0, "branches": ["CSE","AIML","IT"], "skills": ["Python"], "color": "#007CC2"},
    "Wipro":      {"min_cgpa": 6.0, "max_backlogs": 1, "branches": ["CSE","AIML","ECE","IT","EEE","MECH"], "skills": [], "color": "#341C5C"},
    "Accenture":  {"min_cgpa": 6.5, "max_backlogs": 0, "branches": ["CSE","AIML","IT","ECE"], "skills": [], "color": "#A100FF"},
    "Cognizant":  {"min_cgpa": 6.0, "max_backlogs": 0, "branches": ["CSE","AIML","IT","ECE","EEE"], "skills": [], "color": "#0033A0"},
    "HCL":        {"min_cgpa": 5.5, "max_backlogs": 1, "branches": ["CSE","AIML","ECE","IT","EEE","MECH"], "skills": [], "color": "#0076CE"},
    "Google":     {"min_cgpa": 8.5, "max_backlogs": 0, "branches": ["CSE","AIML"], "skills": ["Python","DSA"], "color": "#4285F4"},
    "Amazon":     {"min_cgpa": 7.5, "max_backlogs": 0, "branches": ["CSE","AIML","IT"], "skills": ["Python","DSA"], "color": "#FF9900"},
    "Microsoft":  {"min_cgpa": 8.0, "max_backlogs": 0, "branches": ["CSE","AIML"], "skills": ["Python"], "color": "#00A4EF"},
    "Deloitte":   {"min_cgpa": 7.0, "max_backlogs": 0, "branches": ["CSE","AIML","IT","ECE","MECH","CIVIL"], "skills": [], "color": "#86BC25"},
}

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

.main { background: #0A0E1A; }
[data-testid="stAppViewContainer"] { background: #0A0E1A; }
[data-testid="stSidebar"] { background: #0D1220 !important; border-right: 1px solid #1E2A45; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.kpi-card {
    background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
    border: 1px solid #1E2A45;
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.kpi-card:hover { transform: translateY(-2px); border-color: #3B82F6; }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
}
.kpi-label { font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #6B7280; margin-bottom: 8px; }
.kpi-value { font-size: 32px; font-weight: 800; color: #F9FAFB; line-height: 1; font-family: 'JetBrains Mono', monospace; }
.kpi-sub { font-size: 12px; color: #9CA3AF; margin-top: 6px; }
.kpi-icon { position: absolute; right: 20px; top: 20px; font-size: 28px; opacity: 0.2; }

.section-title {
    font-size: 18px; font-weight: 700; color: #F9FAFB;
    border-left: 4px solid #3B82F6;
    padding-left: 12px; margin: 24px 0 16px 0;
    letter-spacing: 0.3px;
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.badge-green { background: #064E3B; color: #34D399; }
.badge-red   { background: #450A0A; color: #F87171; }
.badge-blue  { background: #1E3A5F; color: #60A5FA; }

stDataFrame { border-radius: 12px !important; }

[data-testid="metric-container"] { background: #111827; border-radius: 12px; padding: 12px 16px; border: 1px solid #1E2A45; }

div[data-testid="stSelectbox"] > div, div[data-testid="stMultiSelect"] > div {
    background: #111827 !important; border-color: #1E2A45 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #3B82F6, #2563EB);
    color: white; border: none; border-radius: 8px;
    font-family: 'Sora', sans-serif; font-weight: 600;
    padding: 8px 20px;
    transition: all 0.2s ease;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 20px rgba(59,130,246,0.4); }

.company-chip {
    display: inline-block; margin: 3px;
    padding: 4px 12px; border-radius: 20px;
    font-size: 12px; font-weight: 600;
    background: #1E2A45; color: #93C5FD;
    border: 1px solid #2D3F5E;
}

.eligibility-rule {
    background: #111827; border: 1px solid #1E2A45;
    border-radius: 10px; padding: 14px 18px;
    margin: 8px 0;
}

.header-band {
    background: linear-gradient(135deg, #0F172A 0%, #1E2A45 50%, #0F172A 100%);
    border: 1px solid #1E2A45;
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.header-band::after {
    content: '🎓';
    position: absolute; right: 40px; top: 50%;
    transform: translateY(-50%);
    font-size: 80px; opacity: 0.08;
}
.header-title { font-size: 30px; font-weight: 800; color: #F9FAFB; margin: 0; }
.header-sub { font-size: 14px; color: #6B7280; margin-top: 6px; }
.header-team { font-size: 12px; color: #3B82F6; margin-top: 10px; font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ───────────────────────────────────────────────────────────
@st.cache_data
def load_data(file=None):
    if file is not None:
        df = pd.read_csv(file)
    else:
        try:
            df = pd.read_csv("students_enriched.csv")
        except:
            df = pd.read_csv("students_dataset.csv")
    return df

@st.cache_data
def enrich_data(df):
    def is_eligible(row, rules):
        if row['CGPA'] < rules['min_cgpa']: return False
        if row['Active_Backlogs'] > rules['max_backlogs']: return False
        if row['Branch'] not in rules['branches']: return False
        student_skills = [s.strip() for s in str(row['Skills']).split(',')]
        for sk in rules['skills']:
            if sk not in student_skills: return False
        return True

    if 'Eligible_Companies' not in df.columns:
        def get_eligible(row):
            ec = [c for c, rules in COMPANIES.items() if is_eligible(row, rules)]
            return ', '.join(ec) if ec else 'None'
        df = df.copy()
        df['Eligible_Companies'] = df.apply(get_eligible, axis=1)
        df['Eligible_Count'] = df['Eligible_Companies'].apply(lambda x: 0 if x == 'None' else len(x.split(', ')))
    return df

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎓 Placement Dashboard")
    st.markdown("---")

    uploaded = st.file_uploader("📂 Upload CSV Dataset", type=['csv'])
    df_raw = load_data(uploaded)
    df = enrich_data(df_raw)

    st.markdown("---")
    page = st.radio("📍 Navigate", [
        "🏠 Overview",
        "🔍 Student Search",
        "🏢 Company Analysis",
        "📊 Analytics Deep Dive",
        "✅ Eligibility Checker",
        "📥 Export Reports"
    ])

    st.markdown("---")
    st.markdown("**Filters**")
    sel_branch = st.multiselect("Branch", sorted(df['Branch'].unique()), default=[])
    sel_year = st.multiselect("Year of Study", sorted(df['Year_of_Study'].unique()), default=[])
    cgpa_range = st.slider("CGPA Range", 0.0, 10.0, (0.0, 10.0), 0.1)
    backlog_filter = st.selectbox("Backlogs", ["All", "Zero Backlogs", "Has Backlogs"])

    # Apply filters
    dff = df.copy()
    if sel_branch: dff = dff[dff['Branch'].isin(sel_branch)]
    if sel_year:   dff = dff[dff['Year_of_Study'].isin(sel_year)]
    dff = dff[(dff['CGPA'] >= cgpa_range[0]) & (dff['CGPA'] <= cgpa_range[1])]
    if backlog_filter == "Zero Backlogs": dff = dff[dff['Active_Backlogs'] == 0]
    elif backlog_filter == "Has Backlogs": dff = dff[dff['Active_Backlogs'] > 0]

    st.markdown("---")
    st.markdown(f"<small style='color:#6B7280'>Showing **{len(dff):,}** of **{len(df):,}** students</small>", unsafe_allow_html=True)
    st.markdown("<small style='color:#374151'>AIML-F | Campus Placement System</small>", unsafe_allow_html=True)

CHART_COLORS = ['#3B82F6','#10B981','#F59E0B','#EF4444','#8B5CF6','#06B6D4','#F97316','#84CC16']
PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Sora, sans-serif', color='#9CA3AF', size=12),
    xaxis=dict(gridcolor='#1E2A45', linecolor='#1E2A45', tickcolor='#6B7280'),
    yaxis=dict(gridcolor='#1E2A45', linecolor='#1E2A45', tickcolor='#6B7280'),
    margin=dict(t=40, b=40, l=40, r=20),
)

# ─── PAGE: OVERVIEW ─────────────────────────────────────────────────────────
if page == "🏠 Overview":
    st.markdown("""
    <div class="header-band">
        <p class="header-title">Campus Placement Eligibility Dashboard</p>
        <p class="header-sub">Automated eligibility filtering & placement analytics for 10,000 students</p>
    </div>
    """, unsafe_allow_html=True)

    total = len(dff)
    eligible_any = int((dff['Eligible_Count'] > 0).sum())
    placed = int((dff['Placed_Status'] == 'Yes').sum())
    avg_cgpa = round(dff['CGPA'].mean(), 2)
    zero_backlogs = int((dff['Active_Backlogs'] == 0).sum())
    multi_eligible = int((dff['Eligible_Count'] >= 3).sum())
    placement_rate = round(placed / total * 100, 1) if total > 0 else 0
    eligibility_rate = round(eligible_any / total * 100, 1) if total > 0 else 0

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent: #3B82F6">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Total Students</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">In filtered dataset</div>
        </div>
        <div class="kpi-card" style="--accent: #10B981">
            <div class="kpi-icon">✅</div>
            <div class="kpi-label">Eligible Students</div>
            <div class="kpi-value">{eligible_any:,}</div>
            <div class="kpi-sub">{eligibility_rate}% eligibility rate</div>
        </div>
        <div class="kpi-card" style="--accent: #F59E0B">
            <div class="kpi-icon">🏆</div>
            <div class="kpi-label">Already Placed</div>
            <div class="kpi-value">{placed:,}</div>
            <div class="kpi-sub">{placement_rate}% placement rate</div>
        </div>
        <div class="kpi-card" style="--accent: #8B5CF6">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Average CGPA</div>
            <div class="kpi-value">{avg_cgpa}</div>
            <div class="kpi-sub">Across all students</div>
        </div>
        <div class="kpi-card" style="--accent: #06B6D4">
            <div class="kpi-icon">🎯</div>
            <div class="kpi-label">Zero Backlogs</div>
            <div class="kpi-value">{zero_backlogs:,}</div>
            <div class="kpi-sub">{round(zero_backlogs/total*100,1)}% clean record</div>
        </div>
        <div class="kpi-card" style="--accent: #EF4444">
            <div class="kpi-icon">🚀</div>
            <div class="kpi-label">Multi-Company</div>
            <div class="kpi-value">{multi_eligible:,}</div>
            <div class="kpi-sub">Eligible for 3+ companies</div>
        </div>
        <div class="kpi-card" style="--accent: #F97316">
            <div class="kpi-icon">💼</div>
            <div class="kpi-label">Not Yet Placed</div>
            <div class="kpi-value">{total - placed:,}</div>
            <div class="kpi-sub">Still seeking placement</div>
        </div>
        <div class="kpi-card" style="--accent: #84CC16">
            <div class="kpi-icon">🏢</div>
            <div class="kpi-label">Companies</div>
            <div class="kpi-value">{len(COMPANIES)}</div>
            <div class="kpi-sub">Participating recruiters</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Branch-wise Student Distribution</div>', unsafe_allow_html=True)
        branch_counts = dff['Branch'].value_counts().reset_index()
        branch_counts.columns = ['Branch', 'Count']
        fig = px.bar(branch_counts, x='Branch', y='Count', color='Branch',
                     color_discrete_sequence=CHART_COLORS)
        fig.update_layout(**PLOTLY_THEME, showlegend=False, height=280)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">CGPA Distribution</div>', unsafe_allow_html=True)
        fig2 = px.histogram(dff, x='CGPA', nbins=30, color_discrete_sequence=['#3B82F6'])
        fig2.update_layout(**PLOTLY_THEME, height=280, bargap=0.05)
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">Placement Status</div>', unsafe_allow_html=True)
        placed_counts = dff['Placed_Status'].value_counts()
        fig3 = px.pie(values=placed_counts.values, names=placed_counts.index,
                      color_discrete_sequence=['#10B981','#EF4444'], hole=0.55)
        fig3.update_layout(**PLOTLY_THEME, height=280, showlegend=True)
        fig3.update_traces(textfont_size=13)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">Company Eligibility Count</div>', unsafe_allow_html=True)
        comp_eligible = {}
        for company, rules in COMPANIES.items():
            def is_elig(row, r=rules):
                if row['CGPA'] < r['min_cgpa']: return False
                if row['Active_Backlogs'] > r['max_backlogs']: return False
                if row['Branch'] not in r['branches']: return False
                ss = [s.strip() for s in str(row['Skills']).split(',')]
                for sk in r['skills']:
                    if sk not in ss: return False
                return True
            comp_eligible[company] = int(dff.apply(is_elig, axis=1).sum())

        comp_df = pd.DataFrame(list(comp_eligible.items()), columns=['Company','Eligible'])
        comp_df = comp_df.sort_values('Eligible', ascending=True)
        fig4 = px.bar(comp_df, x='Eligible', y='Company', orientation='h',
                      color='Eligible', color_continuous_scale='Blues')
        fig4.update_layout(**PLOTLY_THEME, height=280, coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-title">Year-wise Placement Overview</div>', unsafe_allow_html=True)
    year_placed = dff.groupby(['Year_of_Study','Placed_Status']).size().reset_index(name='Count')
    fig5 = px.bar(year_placed, x='Year_of_Study', y='Count', color='Placed_Status',
                  barmode='group', color_discrete_map={'Yes':'#10B981','No':'#EF4444'})
    fig5.update_layout(**PLOTLY_THEME, height=250)
    st.plotly_chart(fig5, use_container_width=True)


# ─── PAGE: STUDENT SEARCH ───────────────────────────────────────────────────
elif page == "🔍 Student Search":
    st.markdown('<div class="section-title">🔍 Student Search & Profile Viewer</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3,1])
    with col1:
        search = st.text_input("Search by Student Name or ID", placeholder="e.g. Samhita or EG00001")
    with col2:
        sort_col = st.selectbox("Sort by", ['CGPA', 'Eligible_Count', 'Internships_Completed', 'Active_Backlogs'])

    results = dff.copy()
    if search:
        results = results[
            results['Student_Name'].str.contains(search, case=False, na=False) |
            results['Student_ID'].str.contains(search, case=False, na=False)
        ]

    results = results.sort_values(sort_col, ascending=(sort_col == 'Active_Backlogs'))

    st.markdown(f"<small style='color:#6B7280'>Found **{len(results):,}** students</small>", unsafe_allow_html=True)

    display_cols = ['Student_ID','Student_Name','Gender','Branch','Year_of_Study',
                    'CGPA','Active_Backlogs','Internships_Completed','Placed_Status','Eligible_Count','Eligible_Companies']

    def highlight_rows(row):
        if row['Eligible_Count'] >= 5:
            return ['background-color: #064E3B22'] * len(row)
        elif row['Eligible_Count'] == 0:
            return ['background-color: #450A0A22'] * len(row)
        return [''] * len(row)

    st.dataframe(
        results[display_cols].head(500).style.apply(highlight_rows, axis=1),
        use_container_width=True,
        height=450
    )

    if len(results) == 1:
        st.markdown('<div class="section-title">📋 Student Profile</div>', unsafe_allow_html=True)
        student = results.iloc[0]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("CGPA", student['CGPA'])
            st.metric("10th %", f"{student['10th_Percentage']}%")
            st.metric("12th %", f"{student['12th_Percentage']}%")
        with c2:
            st.metric("Active Backlogs", student['Active_Backlogs'])
            st.metric("History Backlogs", student['History_of_Backlogs'])
            st.metric("Internships", student['Internships_Completed'])
        with c3:
            st.metric("Eligible For", f"{student['Eligible_Count']} companies")
            st.metric("Placed", student['Placed_Status'])
            st.metric("Year", student['Year_of_Study'])

        st.markdown("**Skills:**")
        skills_html = ' '.join([f'<span class="company-chip">{s.strip()}</span>' for s in str(student['Skills']).split(',')])
        st.markdown(skills_html, unsafe_allow_html=True)

        st.markdown("**Eligible Companies:**")
        if student['Eligible_Companies'] != 'None':
            comp_html = ' '.join([f'<span class="company-chip" style="color:#34D399;border-color:#064E3B">✓ {c.strip()}</span>' for c in str(student['Eligible_Companies']).split(',')])
        else:
            comp_html = '<span class="badge badge-red">Not eligible for any company</span>'
        st.markdown(comp_html, unsafe_allow_html=True)


# ─── PAGE: COMPANY ANALYSIS ─────────────────────────────────────────────────
elif page == "🏢 Company Analysis":
    st.markdown('<div class="section-title">🏢 Company-wise Eligibility Analysis</div>', unsafe_allow_html=True)

    selected_company = st.selectbox("Select Company", list(COMPANIES.keys()))
    rules = COMPANIES[selected_company]

    def is_eligible_company(row, r):
        if row['CGPA'] < r['min_cgpa']: return False
        if row['Active_Backlogs'] > r['max_backlogs']: return False
        if row['Branch'] not in r['branches']: return False
        ss = [s.strip() for s in str(row['Skills']).split(',')]
        for sk in r['skills']:
            if sk not in ss: return False
        return True

    eligible_mask = dff.apply(lambda r: is_eligible_company(r, rules), axis=1)
    eligible_students = dff[eligible_mask]
    not_eligible = dff[~eligible_mask]

    st.markdown(f"""
    <div class="eligibility-rule">
        <strong style="color:#F9FAFB;font-size:16px">{selected_company} Eligibility Criteria</strong><br><br>
        <span class="badge badge-blue">Min CGPA: {rules['min_cgpa']}</span>&nbsp;
        <span class="badge badge-blue">Max Backlogs: {rules['max_backlogs']}</span>&nbsp;
        <span class="badge badge-blue">Branches: {', '.join(rules['branches'])}</span>&nbsp;
        {'<span class="badge badge-blue">Required Skills: ' + ', '.join(rules['skills']) + '</span>' if rules['skills'] else '<span class="badge badge-green">No Skill Restriction</span>'}
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Eligible Students", f"{len(eligible_students):,}")
    k2.metric("Not Eligible", f"{len(not_eligible):,}")
    k3.metric("Eligibility Rate", f"{round(len(eligible_students)/len(dff)*100,1)}%")
    k4.metric("Avg CGPA (Eligible)", f"{round(eligible_students['CGPA'].mean(),2)}" if len(eligible_students) > 0 else "N/A")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="section-title">Branch-wise Eligible for {selected_company}</div>', unsafe_allow_html=True)
        branch_elig = eligible_students['Branch'].value_counts().reset_index()
        branch_elig.columns = ['Branch','Count']
        fig = px.bar(branch_elig, x='Branch', y='Count', color='Count',
                     color_continuous_scale='Blues')
        fig.update_layout(**PLOTLY_THEME, height=280, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f'<div class="section-title">CGPA Distribution — Eligible vs Not</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(x=eligible_students['CGPA'], name='Eligible', marker_color='#10B981', opacity=0.7, nbinsx=20))
        fig2.add_trace(go.Histogram(x=not_eligible['CGPA'], name='Not Eligible', marker_color='#EF4444', opacity=0.7, nbinsx=20))
        fig2.update_layout(**PLOTLY_THEME, barmode='overlay', height=280)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f'<div class="section-title">Eligible Students for {selected_company}</div>', unsafe_allow_html=True)
    show_cols = ['Student_ID','Student_Name','Branch','CGPA','Active_Backlogs','Internships_Completed','Placed_Status','Skills']
    st.dataframe(eligible_students[show_cols].sort_values('CGPA', ascending=False), use_container_width=True, height=350)


# ─── PAGE: ANALYTICS DEEP DIVE ──────────────────────────────────────────────
elif page == "📊 Analytics Deep Dive":
    st.markdown('<div class="section-title">📊 Analytics Deep Dive</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🎓 Academic Analysis", "💼 Skills & Internships", "🌐 Branch Heatmap"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">CGPA vs Backlogs</div>', unsafe_allow_html=True)
            fig = px.scatter(dff.sample(min(2000, len(dff))), x='CGPA', y='Active_Backlogs',
                             color='Branch', size_max=6, opacity=0.6,
                             color_discrete_sequence=CHART_COLORS)
            fig.update_layout(**PLOTLY_THEME, height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">10th vs 12th vs CGPA</div>', unsafe_allow_html=True)
            fig2 = px.scatter(dff.sample(min(1500, len(dff))), x='10th_Percentage', y='12th_Percentage',
                              color='CGPA', size_max=5, color_continuous_scale='Blues',
                              hover_data=['Student_Name','Branch'])
            fig2.update_layout(**PLOTLY_THEME, height=300)
            st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="section-title">Branch-wise Avg CGPA</div>', unsafe_allow_html=True)
            avg_cgpa_branch = dff.groupby('Branch')['CGPA'].mean().reset_index()
            fig3 = px.bar(avg_cgpa_branch.sort_values('CGPA', ascending=False),
                          x='Branch', y='CGPA', color='CGPA',
                          color_continuous_scale='Blues', range_y=[5.5, 8.5])
            fig3.update_layout(**PLOTLY_THEME, height=250, coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.markdown('<div class="section-title">Backlog Distribution</div>', unsafe_allow_html=True)
            bl = dff['Active_Backlogs'].value_counts().sort_index().reset_index()
            bl.columns = ['Backlogs', 'Students']
            fig4 = px.bar(bl, x='Backlogs', y='Students', color='Students',
                          color_continuous_scale='Reds')
            fig4.update_layout(**PLOTLY_THEME, height=250, coloraxis_showscale=False)
            st.plotly_chart(fig4, use_container_width=True)

    with tab2:
        from collections import Counter
        all_skills = []
        for s in dff['Skills']:
            all_skills.extend([x.strip() for x in str(s).split(',')])
        skill_counter = Counter(all_skills)
        top_skills_df = pd.DataFrame(skill_counter.most_common(15), columns=['Skill','Count'])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">Top 15 Skills</div>', unsafe_allow_html=True)
            fig = px.bar(top_skills_df.sort_values('Count'), x='Count', y='Skill',
                         orientation='h', color='Count', color_continuous_scale='Blues')
            fig.update_layout(**PLOTLY_THEME, height=380, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">Internship vs CGPA</div>', unsafe_allow_html=True)
            fig2 = px.box(dff, x='Internships_Completed', y='CGPA',
                          color='Internships_Completed',
                          color_discrete_sequence=CHART_COLORS)
            fig2.update_layout(**PLOTLY_THEME, height=380, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="section-title">Internship Distribution</div>', unsafe_allow_html=True)
            intern_counts = dff['Internships_Completed'].value_counts().sort_index().reset_index()
            intern_counts.columns = ['Internships','Count']
            intern_counts['Label'] = intern_counts['Internships'].apply(lambda x: f"{x} Internship{'s' if x!=1 else ''}")
            fig3 = px.pie(intern_counts, values='Count', names='Label',
                          color_discrete_sequence=CHART_COLORS, hole=0.4)
            fig3.update_layout(**PLOTLY_THEME, height=280)
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.markdown('<div class="section-title">Gender Distribution by Branch</div>', unsafe_allow_html=True)
            gd = dff.groupby(['Branch','Gender']).size().reset_index(name='Count')
            fig4 = px.bar(gd, x='Branch', y='Count', color='Gender', barmode='group',
                          color_discrete_map={'Male':'#3B82F6','Female':'#EC4899'})
            fig4.update_layout(**PLOTLY_THEME, height=280)
            st.plotly_chart(fig4, use_container_width=True)

    with tab3:
        st.markdown('<div class="section-title">Branch × Company Eligibility Heatmap</div>', unsafe_allow_html=True)
        heatmap_data = {}
        for company, rules in COMPANIES.items():
            heatmap_data[company] = {}
            for branch in ['CSE','AIML','ECE','IT','EEE','MECH','CIVIL','CHEM']:
                bdf = dff[dff['Branch'] == branch]
                def is_e(row, r=rules):
                    if row['CGPA'] < r['min_cgpa']: return False
                    if row['Active_Backlogs'] > r['max_backlogs']: return False
                    if row['Branch'] not in r['branches']: return False
                    ss = [s.strip() for s in str(row['Skills']).split(',')]
                    for sk in r['skills']:
                        if sk not in ss: return False
                    return True
                heatmap_data[company][branch] = int(bdf.apply(is_e, axis=1).sum())

        hm_df = pd.DataFrame(heatmap_data).T
        fig = px.imshow(hm_df, color_continuous_scale='Blues', aspect='auto',
                        text_auto=True)
        fig.update_layout(**PLOTLY_THEME, height=400)
        fig.update_traces(textfont_size=12)
        st.plotly_chart(fig, use_container_width=True)


# ─── PAGE: ELIGIBILITY CHECKER ──────────────────────────────────────────────
elif page == "✅ Eligibility Checker":
    st.markdown('<div class="section-title">✅ Individual Student Eligibility Checker</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("#### Enter Student Details")
        s_name = st.text_input("Student Name", "Samhita Iyengar")
        s_branch = st.selectbox("Branch", ['CSE','AIML','ECE','IT','EEE','MECH','CIVIL','CHEM'])
        s_cgpa = st.number_input("CGPA", 0.0, 10.0, 7.5, 0.1)
        s_backlogs = st.number_input("Active Backlogs", 0, 10, 0)
        s_skills = st.multiselect("Skills", ['Python','Java','C++','SQL','Machine Learning',
                                              'Deep Learning','JavaScript','React','Node.js',
                                              'DSA','R','Tableau','Power BI','TensorFlow',
                                              'Keras','HTML/CSS','Django','Flask','AWS','Git'])

    with col2:
        st.markdown("#### Eligibility Results")
        if st.button("🔍 Check Eligibility", use_container_width=True):
            eligible_for = []
            not_eligible_for = []

            for company, rules in COMPANIES.items():
                reasons = []
                passed = True
                if s_cgpa < rules['min_cgpa']:
                    reasons.append(f"CGPA {s_cgpa} < {rules['min_cgpa']}")
                    passed = False
                if s_backlogs > rules['max_backlogs']:
                    reasons.append(f"Backlogs {s_backlogs} > {rules['max_backlogs']}")
                    passed = False
                if s_branch not in rules['branches']:
                    reasons.append(f"{s_branch} not in allowed branches")
                    passed = False
                for sk in rules['skills']:
                    if sk not in s_skills:
                        reasons.append(f"Missing skill: {sk}")
                        passed = False
                if passed:
                    eligible_for.append(company)
                else:
                    not_eligible_for.append((company, reasons))

            if eligible_for:
                st.success(f"✅ **{s_name}** is eligible for **{len(eligible_for)}** companies!")
                for c in eligible_for:
                    color = COMPANIES[c]['color']
                    st.markdown(f"<span class='badge badge-green' style='font-size:14px;padding:6px 14px'>✓ {c}</span>", unsafe_allow_html=True)
            else:
                st.error(f"❌ **{s_name}** is not eligible for any company.")

            if not_eligible_for:
                with st.expander("See rejection reasons"):
                    for company, reasons in not_eligible_for:
                        st.markdown(f"**{company}:** {' | '.join(reasons)}")
        else:
            st.info("Fill in student details and click **Check Eligibility**")

    st.markdown("---")
    st.markdown('<div class="section-title">📋 All Company Eligibility Rules</div>', unsafe_allow_html=True)
    rules_data = []
    for company, rules in COMPANIES.items():
        rules_data.append({
            'Company': company,
            'Min CGPA': rules['min_cgpa'],
            'Max Backlogs': rules['max_backlogs'],
            'Allowed Branches': ', '.join(rules['branches']),
            'Required Skills': ', '.join(rules['skills']) if rules['skills'] else 'None'
        })
    rules_df = pd.DataFrame(rules_data)
    st.dataframe(rules_df, use_container_width=True, hide_index=True)


# ─── PAGE: EXPORT ───────────────────────────────────────────────────────────
elif page == "📥 Export Reports":
    st.markdown('<div class="section-title">📥 Export Reports</div>', unsafe_allow_html=True)

    st.markdown("#### Select Company to Export Eligible Students")
    export_company = st.selectbox("Company", ["All Companies"] + list(COMPANIES.keys()))

    if export_company == "All Companies":
        export_df = dff.copy()
        export_df = export_df[export_df['Eligible_Count'] > 0]
    else:
        rules = COMPANIES[export_company]
        def is_elig_export(row, r=rules):
            if row['CGPA'] < r['min_cgpa']: return False
            if row['Active_Backlogs'] > r['max_backlogs']: return False
            if row['Branch'] not in r['branches']: return False
            ss = [s.strip() for s in str(row['Skills']).split(',')]
            for sk in r['skills']:
                if sk not in ss: return False
            return True
        export_df = dff[dff.apply(is_elig_export, axis=1)].copy()

    st.markdown(f"**{len(export_df):,} students** will be included in the export.")
    st.dataframe(export_df.head(100), use_container_width=True, height=300)

    col1, col2 = st.columns(2)
    with col1:
        csv_data = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Download as CSV",
            data=csv_data,
            file_name=f"eligible_{export_company.replace(' ','_')}.csv",
            mime='text/csv',
            use_container_width=True
        )

    with col2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, index=False, sheet_name='Eligible Students')
            # Summary sheet
            summary = pd.DataFrame({
                'Metric': ['Total Eligible', 'Company', 'Export Date'],
                'Value': [len(export_df), export_company, pd.Timestamp.now().strftime('%Y-%m-%d')]
            })
            summary.to_excel(writer, index=False, sheet_name='Summary')
        buffer.seek(0)
        st.download_button(
            "⬇️ Download as Excel",
            data=buffer,
            file_name=f"eligible_{export_company.replace(' ','_')}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            use_container_width=True
        )

    st.markdown("---")
    st.markdown('<div class="section-title">📊 Full Eligibility Matrix</div>', unsafe_allow_html=True)
    matrix_rows = []
    for _, student in dff.iterrows():
        row = {
            'Student_ID': student['Student_ID'],
            'Student_Name': student['Student_Name'],
            'Branch': student['Branch'],
            'CGPA': student['CGPA'],
        }
        for company, rules in COMPANIES.items():
            def is_e(r, ru=rules):
                if r['CGPA'] < ru['min_cgpa']: return False
                if r['Active_Backlogs'] > ru['max_backlogs']: return False
                if r['Branch'] not in ru['branches']: return False
                ss = [s.strip() for s in str(r['Skills']).split(',')]
                for sk in ru['skills']:
                    if sk not in ss: return False
                return True
            row[company] = '✓' if is_e(student) else '✗'
        matrix_rows.append(row)

    matrix_df = pd.DataFrame(matrix_rows)
    st.dataframe(matrix_df.head(200), use_container_width=True, height=350)

    matrix_csv = matrix_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Full Matrix CSV", data=matrix_csv,
                       file_name="full_eligibility_matrix.csv", mime='text/csv')
