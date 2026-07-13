import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs



st.set_page_config(page_title="JOb Recommender", page_icon=":briefcase:", layout= "wide")
st.title("📄AI JOb Recommender")
st.markdown("Upload Your Resume and get job recommendations based on your skills and experinece from linkdin and naukri.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extract text from your resume...."):
        resume_text =  extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume......"):
        summary = ask_openai(f"Summarize this resume highlighting the most important skills, education, and Experience : \n{resume_text}", max_tokens=500)

    with st.spinner("Finding a skills gaps......"):
        gaps = ask_openai(f"Analyzse this reume and highlight missing skills, certifications, and experiences need for better job opportunities : \n{resume_text}", max_tokens=500)
   
    with st.spinner("Creating future Roadmap......"):
        roadmap = ask_openai(f"Based on this resume, suggest future roadmap to imporve this person career prospects (skill to learn, certification nedded, industry exposure) : \n{resume_text}", max_tokens=500) 

    # display nicley formated results
    st.markdown("---")
    st.header("📝 Resume Summary")
    st.markdown(f"<div style= 'background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠 skill Gaps & Missing Areas")
    st.markdown(f"<div style= 'background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style= 'background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Comleted Successfully!")

    if st.button("🔎Get Job Recommendation"):
        with st.spinner("Fetching the job recommendation..."):
            keywords = ask_openai(
                f"Based on this resume summary, suggest the best job title and keywords for searching job. Give a comma- separted list only, no explaination.\n\nSummary: {summary}", 
                max_tokens=100
            )

            search_keywords_clean= keywords.replace("\n", "").strip()

        st.success(f"Extracted job Keywords: {search_keywords_clean }")

        with st.spinner(f"Fetching the job from Linkdin and Naukri....."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=60)

        st.markdown("---")
        st.header("💼 Top LinkedIn Jobs")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found.")

        st.markdown("---")
        st.header("💼 Top Naukri Jobs (India)")

        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('url')})")
                st.markdown("---")
        else:
            st.warning("No Naukri jobs found.")








    


