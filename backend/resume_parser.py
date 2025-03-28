import re
import spacy
import pdfplumber

nlp=spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extract Text from a PDF file"""
    text= ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.page:
            text+=page.extract_text()+ "\n"
    return text.strip()

def extract_email(text):
    """Extract email from text"""
    match= re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+",text)
    return match.group() if match  else None

def extract_phone(text):
    """Extract phone number from text"""
    match = re.search(r"\b\d{10}\b", text)  # Matches 10-digit numbers
    return match.group() if match else None

def extract_skills(text):
    """Extract key skills using NLP"""
    doc = nlp(text)
    skills = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return ", ".join(set(skills))

def parse_resume(pdf_path):
    """Parse resume and extract details"""
    text = extract_text_from_pdf(pdf_path)
    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "text": text
    }