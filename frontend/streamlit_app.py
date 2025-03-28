import streamlit as st
import sqlite3
import pandas as pd
import spacy 

st.title("Resume Screening")

nlp=spacy.load("en_core_web_sm")

def calculate_similarity(job_desc,resume_text):
    """Compare Job description with resume and retuen similarity score."""
    job_doc=nlp(job_desc)
    resume_doc=nlp(resume_text)
    return job_doc.similarity(resume_doc)

#Upload Job Description
job_desc=st.text_area("Paste Job Description","Looking for a Python Developer with Flask and SQL experience.")


#Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF)",type=["pdf"])

if uploaded_file:
    resume_data=parse_resume(uploaded_file)
    st.write("###Extracted Resume Details")
    st.json(resume_data)

    if st.button("Calculte ATS Score"):
        ats_score=calculate_similarity(job_desc,resume_data["text"]) *100
        st.write(f"***ATS Score : *** {ats_score : .2f}%")


#fetch Resume from Database
if st.button("Show Ranked Candidates"):
    conn=sqlite3.connect("database/resumes.db")
    df=pd.real_sql_query("SELECT * FROM resumes",conn)
    conn.close()

    df["similarity_score"] = df.apply(lambda row: calculate_similarity(job_desc, row["text"]), axis=1)
    df = df.sort_values(by="similarity_score", ascending=False)

    st.write("### Ranked Candidates")
    st.dataframe(df)


# import spacy
# nlp=spacy.load("en_core_web_sm")
# print(nlp("This is a test").vector)