import streamlit as st

from llm_client import (
    LLMError,
    MissingAPIKeyError,
    generate_match_report,
    get_api_key,
)
from parser import PDFExtractionError, extract_text_from_pdf

st.set_page_config(page_title="AI Resume-Job Matcher", layout="wide")

st.title("AI Resume-Job Matcher")
st.caption("Upload your resume and paste a job description to get a tailored matching report.")

with st.sidebar:
    st.header("Setup")
    st.markdown(
        "Set `DEEPSEEK_API_KEY` in one of the following:\n\n"
        "- **Local:** `.env` file (copy from `.env.example`)\n"
        "- **Streamlit Cloud:** [Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) → `DEEPSEEK_API_KEY`"
    )
    if not get_api_key():
        st.warning("API key missing. See the instructions above to configure it.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the job description", height=200)
analyze_clicked = st.button("Analyze", type="primary")

if analyze_clicked:
    if uploaded_file is None:
        st.error("Please upload a PDF resume before analyzing.")
        st.stop()
    
    jd = job_description.strip()
    if not jd:
        st.error("Please paste a job description before analyzing.")
        st.stop()
    
    if not get_api_key():
        st.error("DEEPSEEK_API_KEY is not set. Set it in .env (local) or Streamlit Cloud Secrets.")
        st.stop()
    
    try:
        resume_text = extract_text_from_pdf(uploaded_file.read())
    except PDFExtractionError as e:
        st.error(str(e))
        st.stop()
    
    with st.spinner("Analyzing resume against job description..."):
        try:
            report = generate_match_report(resume_text, jd)
        except MissingAPIKeyError as e:
            st.error(str(e))
            st.stop()
        except LLMError as e:
            st.error(f"Analysis failed: {e}. Check your API key and try again.")
            st.stop()
    
    st.markdown("## Report")
    st.markdown(report, unsafe_allow_html=False)
    st.download_button(
        label="Download report (.md)",
        data=report,
        file_name="resume_match_report.md",
        mime="text/markdown"
    )
