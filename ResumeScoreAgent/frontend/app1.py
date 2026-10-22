import streamlit as st
import re
from collections import Counter

# Set page config
st.set_page_config(
    page_title="AI Resume Screener & Career Agent",
    page_icon="📄",
    layout="wide"
)

# Optional dependencies for file parsing
try:
    import pypdf
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    import docx
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False


# ==========================================
# HELPER FUNCTIONS & SCREENING ENGINE
# ==========================================

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded PDF or DOCX file."""
    text = ""
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type == 'pdf':
        if not PDF_SUPPORT:
            st.error("Please install `pypdf` to read PDF files (`pip install pypdf`).")
            return ""
        reader = pypdf.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""
            
    elif file_type == 'docx':
        if not DOCX_SUPPORT:
            st.error("Please install `python-docx` to read DOCX files (`pip install python-docx`).")
            return ""
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
            
    elif file_type == 'txt':
        text = str(uploaded_file.read(), "utf-8")
        
    return text


def clean_and_tokenize(text):
    """Clean text and break down into lowercase words/keywords."""
    text = text.lower()
    # Remove punctuation & special characters
    words = re.findall(r'\b[a-zA-Z0-9+#.]+\b', text)
    # Filter common stop words
    stop_words = set(["and", "the", "to", "a", "of", "for", "in", "with", "on", "at", "by", "from", "is", "an", "or", "as", "be", "are"])
    return [w for w in words if w not in stop_words and len(w) > 1]


def evaluate_resume(resume_text, jd_text):
    """Core screening logic that computes score and extracts insights."""
    resume_words = clean_and_tokenize(resume_text)
    jd_words = clean_and_tokenize(jd_text)

    resume_counter = Counter(resume_words)
    jd_counter = Counter(jd_words)

    # Unique keywords from JD
    unique_jd_keywords = set(jd_counter.keys())
    matched_keywords = [word for word in unique_jd_keywords if word in resume_counter]
    missing_keywords = [word for word in unique_jd_keywords if word not in resume_counter]

    # Calculate match percentage
    if unique_jd_keywords:
        match_score = round((len(matched_keywords) / len(unique_jd_keywords)) * 100, 1)
    else:
        match_score = 0.0

    # Sort missing words by JD frequency (most important missing skills first)
    top_missing = sorted(missing_keywords, key=lambda x: jd_counter[x], reverse=True)[:10]
    top_matched = sorted(matched_keywords, key=lambda x: jd_counter[x], reverse=True)[:10]

    return {
        "score": match_score,
        "matched_keywords": top_matched,
        "missing_keywords": top_missing,
        "total_jd_terms": len(unique_jd_keywords),
        "total_matched_terms": len(matched_keywords)
    }


# ==========================================
# UI & APP STRUCTURE
# ==========================================

st.title("📄 AI Resume Screener & Career Agent")
st.write("Analyze how well a candidate's resume aligns with a Job Description (JD) and get instant feedback.")

st.divider()

# Two-column layout for input fields
col_left, col_right = st.columns(2)

with col_left:
    st.header("1. Job Description")
    jd_input = st.text_area(
        "Paste the Job Description here:",
        height=280,
        placeholder="Paste requirements, responsibilities, and required skills..."
    )

with col_right:
    st.header("2. Resume Input")
    
    input_method = st.radio("Choose input method:", ["File Upload (PDF/DOCX/TXT)", "Direct Text Paste"], horizontal=True)
    
    resume_text_input = ""
    
    if input_method == "File Upload (PDF/DOCX/TXT)":
        uploaded_file = st.file_uploader("Upload Resume File", type=["pdf", "docx", "txt"])
        if uploaded_file is not None:
            resume_text_input = extract_text_from_file(uploaded_file)
            st.success(f"Successfully loaded `{uploaded_file.name}` ({len(resume_text_input)} characters extracted)")
    else:
        resume_text_input = st.text_area(
            "Paste Resume Text here:",
            height=200,
            placeholder="Paste raw resume content..."
        )

# Analyze Button
st.write("")
analyze_btn = st.button("🚀 Analyze Resume & Calculate Score", type="primary", use_container_width=True)

# ==========================================
# RESULTS & FEEDBACK DASHBOARD
# ==========================================

if analyze_btn:
    if not jd_input.strip() or not resume_text_input.strip():
        st.error("⚠️ Please provide both a **Job Description** and a **Resume** before running the evaluation.")
    else:
        results = evaluate_resume(resume_text_input, jd_input)
        score = results["score"]

        st.divider()
        st.header("📊 Screening Evaluation & Score")

        # Score Banner & Visual Gauge
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        metric_col1.metric("Overall Match Score", f"{score}%")
        metric_col2.metric("Matched Keywords", f"{results['total_matched_terms']} / {results['total_jd_terms']}")
        
        if score >= 75:
            match_status = "🟢 Strong Candidate Match"
            status_color = "success"
        elif score >= 50:
            match_status = "🟡 Moderate Candidate Match"
            status_color = "warning"
        else:
            match_status = "🔴 Low Match / Needs Work"
            status_color = "error"

        metric_col3.subheader("Assessment")
        if status_color == "success":
            metric_col3.success(match_status)
        elif status_color == "warning":
            metric_col3.warning(match_status)
        else:
            metric_col3.error(match_status)

        st.progress(int(score))

        # Actionable Feedback Tabs
        st.write("---")
        st.subheader("💡 Analysis & Actionable Recommendations")

        tab_analysis, tab_action, tab_interview = st.tabs([
            "🔍 Detailed Analysis", 
            "📝 Recommendations & Improvements", 
            "❓ Tailored Interview Questions"
        ])

        with tab_analysis:
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("### ✅ Matched Key Skills/Terms")
                if results["matched_keywords"]:
                    for kw in results["matched_keywords"]:
                        st.markdown(f"- **`{kw}`**")
                else:
                    st.write("No major key terms matched.")

            with col_b:
                st.write("### ❌ Missing Important Skills/Terms")
                if results["missing_keywords"]:
                    for kw in results["missing_keywords"]:
                        st.markdown(f"- **`{kw}`**")
                else:
                    st.write("No critical gaps identified!")

        with tab_action:
            st.write("### 🎯 Custom Advice to Improve Resume")
            if score >= 75:
                st.info("""
                **Great fit!** Your resume strongly aligns with this job description.
                * **Tip 1:** Quantify your achievements (e.g., *'Increased revenue by 20%'* instead of *'Responsible for sales'*).
                * **Tip 2:** Highlight specific tools and frameworks in bullet points.
                """)
            elif score >= 50:
                st.warning(f"""
                **Moderate Match ({score}%).** Your resume covers the basics, but lacks several key terms from the job post.
                * **Tip 1:** Add experience or skills mentioning: **{', '.join(results['missing_keywords'][:5])}**.
                * **Tip 2:** Tailor bullet points under your work history to mirror the language used in the Job Description.
                """)
            else:
                st.error(f"""
                **Low Match ({score}%).** The resume appears significantly different from the job requirements.
                * **Action Item:** Make sure to feature missing core technical/domain terms such as: **{', '.join(results['missing_keywords'][:5])}**.
                * **Action Item:** Restructure summary and project descriptions to directly address the JD core requirements.
                """)

        with tab_interview:
            st.write("### 💡 Likely Interview Questions (Based on Skills Gaps)")
            st.write("Be prepared to answer these questions during an interview to address potential experience gaps:")
            
            missing_sample = results["missing_keywords"][:3]
            if missing_sample:
                for idx, skill in enumerate(missing_sample, 1):
                    st.markdown(f"**Q{idx}:** The job description highlights **'{skill}'**. Do you have hands-on experience or transferable skills in this area?")
            else:
                st.write("1. Describe a project where you applied the key requirements of this role.")
                st.write("2. What are your core strengths relevant to this position?")

        # Download Report Feature
        st.write("---")
        report_text = f"""RESUME SCREENING REPORT
========================
Overall Match Score: {score}%
Assessment: {match_status}

TOP MATCHED SKILLS:
{', '.join(results['matched_keywords'])}

TOP MISSING SKILLS:
{', '.join(results['missing_keywords'])}
"""
        st.download_button(
            label="📥 Download Screening Report (.txt)",
            data=report_text,
            file_name="resume_screener_report.txt",
            mime="text/plain"
        )