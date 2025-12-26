import pdfplumber
import spacy
import re
from spacy.matcher import Matcher

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def extract_entities(text):
    doc = nlp(text)
    
    # Extract Email & Phone using Regex
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    
    # Extract Name (using spaCy PERSON label or Pattern Matcher)
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "Not Found")
    
    # Basic Skill Extraction (can be expanded with a CSV list)
    common_skills = ["Python", "Flask", "PostgreSQL", "Machine Learning", "SQL", "Java", "AWS"]
    skills = [skill for skill in common_skills if skill.lower() in text.lower()]

    return {
        "name": name,
        "email": email.group() if email else "N/A",
        "phone": phone.group() if phone else "N/A",
        "skills": list(set(skills)),
        "raw_text": text[:500]  # Store snippet
    }
