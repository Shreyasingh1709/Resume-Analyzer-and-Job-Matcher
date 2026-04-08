# Resume Analyzer & Job Matcher Backend

This backend is part of the Resume Analyzer & Job Matcher project. It provides REST API endpoints for analyzing resumes and matching them with job descriptions using LLM-based understanding and keyword extraction.

## Features
- Upload resumes and job descriptions (PDF or TXT)
- Extract key skills, programming languages, and technical terms
- Match resumes with job descriptions and compute a match score
- Suggest improvements for resumes based on missing skills

## Endpoints

### `POST /analyze_match`
Analyze a resume and job description for skill matching.

**Request:**
- `resume`: Resume file (PDF or TXT, required)
- `job_description_file`: Job description file (PDF or TXT, optional)
- `job_description`: Job description text (optional, used if file not provided)

**Response:**
- `match_score`: Percentage match between resume and job description
- `extracted_skills`: List of extracted skills, programming languages, and technical terms
- `suggestions`: Suggestions for improving the resume

### `GET /`
Health check endpoint.

## Setup & Run
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Start the backend server:
   ```
   uvicorn main:app --reload
   ```
3. The API will be available at [http://localhost:8000](http://localhost:8000)

## How it works
- Uses a transformer-based NER model to extract entities from resumes and job descriptions
- Adds custom keyword extraction for programming languages and common technical terms
- Computes match score and generates suggestions

## Example Usage
See the [frontend](../frontend/) for an interactive Streamlit UI that connects to this backend.

---
**Author:** Shreya Kumari
# Resume Analyzer & Job Matcher Backend

## Endpoints
- `/upload_resume/` (POST): Upload a resume (PDF or text). Returns extracted text.
- `/analyze/` (POST): Analyze resume text and job description. Returns match score and suggestions.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Notes
- PDF parsing uses `pdfplumber`.
- LLM/NLP logic is placeholder; integrate OpenAI/transformers for real extraction and matching.
