import streamlit as st
import sys
import os
import math

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from src.parser import extract_text_from_pdf
from src.skills import extract_skills
from src.matcher import calculate_similarity
from src.scorer import calculate_skill_score, calculate_ats_score
from src.report_generator import generate_report
from src.ranking import rank_resumes

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeIQ",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme injection ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Canvas */
.stApp { background: #0D1117; }
section[data-testid="stSidebar"] {
    background: #161B27 !important;
    border-right: 1px solid #21293B;
}
section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

/* Headings */
h1 { font-size: 1.6rem !important; font-weight: 800 !important;
     letter-spacing: -0.03em !important; color: #F1F5F9 !important; }
h2 { font-size: 1.1rem !important; font-weight: 700 !important;
     color: #E2E8F0 !important; }
h3 { font-size: 0.9rem !important; font-weight: 600 !important;
     color: #CBD5E1 !important; }

/* Metrics */
div[data-testid="metric-container"] {
    background: #161B27;
    border: 1px solid #21293B;
    border-radius: 12px;
    padding: 1rem 1.25rem !important;
}
div[data-testid="metric-container"] label {
    color: #64748B !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-size: 1.4rem !important;
    font-weight: 800 !important;
}

/* Progress bar */
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #2563EB, #60A5FA) !important;
    border-radius: 4px !important;
}
div[data-testid="stProgressBar"] > div {
    background: #21293B !important;
    border-radius: 4px !important;
    height: 6px !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 3px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1D4ED8, #3B82F6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.6rem 1.25rem !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Download button */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #2563EB !important;
    color: #60A5FA !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    padding: 0.4rem 1rem !important;
    width: auto !important;
}

/* Textarea */
.stTextArea textarea {
    background: #0D1117 !important;
    border: 1px solid #21293B !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}
.stTextArea textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}

/* File uploader */
section[data-testid="stFileUploaderDropzone"] {
    background: #0D1117 !important;
    border: 1px dashed #21293B !important;
    border-radius: 10px !important;
}

/* Divider */
hr { border-color: #21293B !important; }

/* Chip helper */
.chip-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
.chip {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
}
.chip-green { background: #052E16; color: #4ADE80; border: 1px solid #14532D; }
.chip-red   { background: #1C0A0A; color: #F87171; border: 1px solid #7F1D1D; }

/* Score ring */
.ring-wrap { text-align: center; }
.ring-label {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #64748B; margin-top: 4px;
    font-family: 'Inter', sans-serif;
}

/* Rank table */
.rank-row {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid #21293B;
    font-family: 'Inter', sans-serif;
}
.rank-row:last-child { border-bottom: none; }
.rank-num {
    width: 26px; height: 26px; border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 800; flex-shrink: 0;
}
.rank-g { background: #3D2500; color: #F59E0B; border: 1px solid #B45309; }
.rank-s { background: #1C2030; color: #94A3B8; border: 1px solid #475569; }
.rank-b { background: #2D1810; color: #CD7C54; border: 1px solid #92400E; }
.rank-n { background: #161B27; color: #64748B; border: 1px solid #21293B; }
.rank-name { flex: 1; font-size: 0.85rem; font-weight: 500; color: #E2E8F0;
             white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.rank-bar { width: 90px; height: 5px; background: #21293B;
            border-radius: 3px; overflow: hidden; }
.rank-fill { height: 100%; background: linear-gradient(90deg,#1D4ED8,#60A5FA);
             border-radius: 3px; }
.rank-score { font-size: 0.85rem; font-weight: 700; color: #F1F5F9;
              font-variant-numeric: tabular-nums; }

/* Sidebar caption text */
.sidebar-caption {
    font-size: 0.68rem; color: #334155; line-height: 1.6;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def score_ring(score: float, size: int = 90) -> str:
    r = (size - 12) / 2
    circ = 2 * math.pi * r
    dash = circ * score
    gap  = circ - dash
    cx   = cy = size / 2
    if score >= 0.85:   col = "#4ADE80"
    elif score >= 0.70: col = "#60A5FA"
    elif score >= 0.50: col = "#FBBF24"
    else:               col = "#F87171"
    return (
        f'<div class="ring-wrap">'
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#21293B" stroke-width="6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="6" '
        f'stroke-linecap="round" '
        f'stroke-dasharray="{dash:.2f} {gap:.2f}" transform="rotate(-90 {cx} {cy})"/>'
        f'<text x="{cx}" y="{cy+1}" text-anchor="middle" dominant-baseline="middle" '
        f'font-family="Inter,sans-serif" font-size="{int(size*0.19)}" '
        f'font-weight="800" fill="{col}">{score*100:.0f}%</text>'
        f'</svg>'
        f'<div class="ring-label">ATS Score</div></div>'
    )


def chips(skills: list, kind: str) -> str:
    css = "chip-green" if kind == "match" else "chip-red"
    icon = "✓" if kind == "match" else "✗"
    if not skills:
        return ""
    return (
        '<div class="chip-wrap">'
        + "".join(f'<span class="chip {css}">{icon} {s}</span>' for s in skills)
        + "</div>"
    )


def rank_medal(pos: int) -> str:
    return {1: "rank-g", 2: "rank-s", 3: "rank-b"}.get(pos, "rank-n")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎯 ResumeIQ")
    st.caption("AI-powered resume screening")
    st.divider()

    st.markdown("**Upload Resumes**")
    uploaded_files = st.file_uploader(
        "Drop PDF files here",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    st.markdown("**Job Description**")
    job_description = st.text_area(
        "Paste the full JD",
        placeholder="Paste the full job description here…",
        height=210,
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("Analyze Resumes →")

    st.divider()
    st.markdown(
        '<div class="sidebar-caption">'
        "Parses PDFs · Extracts skills · Semantic similarity · "
        "ATS scoring · PDF report · Candidate ranking"
        "</div>",
        unsafe_allow_html=True,
    )


# ── Main ──────────────────────────────────────────────────────────────────────
st.title("Resume Screening")
st.caption("Upload candidate PDFs and a job description — get instant ATS scores, skill gaps, and ranked results.")
st.divider()

if not run:
    st.markdown(
        "<br><br>"
        "<div style='text-align:center;color:#334155;font-family:Inter,sans-serif'>"
        "<div style='font-size:2.5rem'>🎯</div>"
        "<p style='font-size:1rem;font-weight:600;color:#475569;margin:0.5rem 0'>Ready to screen candidates</p>"
        "<p style='font-size:0.82rem;color:#334155'>Upload PDFs and paste a JD in the sidebar,<br>then hit <b style=color:#3B82F6>Analyze Resumes →</b></p>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

# ── Validation ────────────────────────────────────────────────────────────────
if not uploaded_files:
    st.error("Upload at least one resume PDF in the sidebar.")
    st.stop()

if not job_description.strip():
    st.error("Paste a job description in the sidebar.")
    st.stop()

# ── Analysis loop ─────────────────────────────────────────────────────────────
os.makedirs("temp", exist_ok=True)
ranking_data = []
jd_skills = extract_skills(job_description)

for i, uploaded_file in enumerate(uploaded_files):

    pdf_path = os.path.join("temp", uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    resume_text    = extract_text_from_pdf(pdf_path)
    resume_skills  = extract_skills(resume_text)
    semantic_score = calculate_similarity(resume_text, job_description)
    skill_score    = calculate_skill_score(jd_skills, resume_skills)
    ats_score      = calculate_ats_score(skill_score, semantic_score)
    ranking_data.append((uploaded_file.name, ats_score))

    matched = sorted(set(jd_skills) & set(resume_skills))
    missing = sorted(set(jd_skills) - set(resume_skills))

    # ── Card header ──
    st.markdown(f"#### 📄 {uploaded_file.name}")

    # ── Score ring + metrics ──
    col_ring, col_m1, col_m2, col_m3 = st.columns([1, 1, 1, 1])
    with col_ring:
        st.markdown(score_ring(ats_score), unsafe_allow_html=True)
    with col_m1:
        st.metric("Skill Match",    f"{skill_score*100:.1f}%")
    with col_m2:
        st.metric("Semantic Match", f"{semantic_score*100:.1f}%")
    with col_m3:
        st.metric("Skills Found",   len(resume_skills))

    # ── Progress + verdict ──
    st.progress(int(ats_score * 100))
    if ats_score >= 0.85:
        st.success("✦ Excellent Match — highly suitable for this role")
    elif ats_score >= 0.70:
        st.info("✦ Good Match — strong candidate with minor gaps")
    elif ats_score >= 0.50:
        st.warning("✦ Average Match — consider after addressing skill gaps")
    else:
        st.error("✦ Poor Match — significant gaps vs. job requirements")

    # ── Skills ──
    c_match, c_miss = st.columns(2)
    with c_match:
        st.markdown("**Matched Skills**")
        if matched:
            st.markdown(chips(matched, "match"), unsafe_allow_html=True)
        else:
            st.caption("No matched skills detected.")
    with c_miss:
        st.markdown("**Missing Skills**")
        if missing:
            st.markdown(chips(missing, "miss"), unsafe_allow_html=True)
        else:
            st.caption("✓ All required skills present.")

    # ── Download ──
    st.markdown("<br>", unsafe_allow_html=True)
    report_file = generate_report(
        ats_score, skill_score, semantic_score, matched, missing
    )
    with open(report_file, "rb") as pdf_file:
        st.download_button(
            label="↓ Download ATS Report",
            data=pdf_file,
            file_name=report_file,
            mime="application/pdf",
            key=f"dl_{i}",
        )

    st.divider()


# ── Ranking ───────────────────────────────────────────────────────────────────
st.markdown("### 🏆 Candidate Ranking")
ranked = rank_resumes(ranking_data)

rows = ""
for pos, (name, score) in enumerate(ranked, 1):
    medal = rank_medal(pos)
    bar_w = int(score * 100)
    rows += (
        f'<div class="rank-row">'
        f'<div class="rank-num {medal}">{pos}</div>'
        f'<div class="rank-name">{name}</div>'
        f'<div class="rank-bar"><div class="rank-fill" style="width:{bar_w}%"></div></div>'
        f'<div class="rank-score">{score*100:.1f}%</div>'
        f'</div>'
    )

st.markdown(
    f'<div style="background:#161B27;border:1px solid #21293B;border-radius:14px;padding:1.25rem 1.5rem">{rows}</div>',
    unsafe_allow_html=True,
)