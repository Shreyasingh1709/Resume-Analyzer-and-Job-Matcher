from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
import pdfplumber
from transformers import pipeline

app = FastAPI()

# NER pipeline
ner = pipeline("ner", grouped_entities=True, model="dslim/bert-base-NER")

def extract_text_from_upload(file: UploadFile) -> str:
    if file.content_type == "application/pdf":
        file.file.seek(0)
        with pdfplumber.open(file.file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text
    else:
        return file.file.read().decode("utf-8")

def extract_entities(text: str) -> List[str]:
    results = ner(text)
    whitelist = {
        "ai", "ml", "ui", "ux", "it", "qa", "hr", "pm", "bi", "ba", "ds", "cv", "nlp", "devops", "db",
        "go", "js", "ts", "c#", "c++", "sql", "aws", "gcp", "api", "etl"
    }
    # Programming languages to search for (case-insensitive)
    prog_langs = [
        "python", "java", "c", "c++", "c#", "javascript", "typescript", "go", "ruby", "php", "swift", "kotlin", "scala", "r", "perl", "matlab", "sql", "html", "css", "bash", "shell", "powershell", "dart", "objective-c", "assembly", "fortran", "lua", "groovy", "rust"
    ]
    # Common technical terms to search for (case-insensitive)
    tech_terms = [
        "data structures", "algorithms", "machine learning", "deep learning", "cloud computing", "docker", "kubernetes", "git", "linux", "rest api", "graphql", "microservices", "tensorflow", "pytorch", "scikit-learn", "numpy", "pandas", "react", "angular", "vue", "node.js", "express", "flask", "django", "spark", "hadoop", "aws", "azure", "gcp", "firebase", "mongodb", "postgresql", "mysql", "sqlite", "redis", "elasticsearch", "jira", "agile", "scrum", "ci/cd", "unit testing", "integration testing", "oop", "object oriented programming", "functional programming", "data analysis", "data visualization", "nlp", "computer vision", "devops", "blockchain", "cybersecurity", "networking", "virtualization", "cloud", "api", "etl", "sas", "spacy", "matplotlib", "seaborn", "tableau", "power bi", "excel"
    ]
    entities = set()
    # NER-based extraction and filtering
    for ent in results:
        word = ent["word"].lower()
        if word.startswith("##"):
            continue
        if (len(word) == 1 and word not in whitelist) or (len(word) == 2 and not word.isalpha() and word not in whitelist):
            continue
        if (len(word) < 3 and word not in whitelist):
            continue
        entities.add(word)
    # Keyword-based extraction for programming languages
    text_lower = text.lower()
    import re
    for lang in prog_langs:
        # For single-letter languages like 'c', match only if surrounded by non-word chars
        if len(lang) == 1:
            if re.search(rf'\b{lang}\b', text_lower):
                entities.add(lang)
        else:
            if lang in text_lower:
                entities.add(lang)
    # Keyword-based extraction for technical terms (exact phrase match)
    for term in tech_terms:
        if term in text_lower:
            entities.add(term)
    return list(entities)

@app.post("/analyze_match")
async def analyze_match(
    resume: UploadFile = File(...),
    job_description_file: Optional[UploadFile] = File(None),
    job_description: Optional[str] = Form(None)
):
    resume_text = extract_text_from_upload(resume)
    if job_description_file:
        job_desc_text = extract_text_from_upload(job_description_file)
    elif job_description:
        job_desc_text = job_description
    else:
        return JSONResponse(status_code=400, content={"error": "No job description provided."})
    resume_skills = set(extract_entities(resume_text))
    job_skills = set(extract_entities(job_desc_text))
    matched = resume_skills & job_skills
    missing = job_skills - resume_skills
    match_score = int(len(matched) / max(len(job_skills), 1) * 100)
    suggestions = []
    if missing:
        for skill in missing:
            suggestions.append(f"Add or highlight skill: {skill}")
    if match_score < 100:
        suggestions.append("Tailor your resume to better match the job description.")
    return {
        "match_score": match_score,
        "extracted_skills": list(resume_skills),
        "suggestions": suggestions
    }

@app.get("/")
def root():
    return {"message": "Resume Analyzer & Job Matcher API"}