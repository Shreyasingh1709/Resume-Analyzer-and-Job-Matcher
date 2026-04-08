# Resume Analyzer & Job Matcher

A full-stack project to analyze resumes and match them with job descriptions using LLM-based understanding, keyword extraction, and a modern interactive UI.

---

## Features
- Upload resumes and job descriptions (PDF or TXT)
- Extract key skills, programming languages, and technical terms
- Match resumes with job descriptions and compute a match score
- Suggest improvements for resumes based on missing skills
- Interactive Streamlit frontend

---

## Project Structure

```
Resume Analyzer and Job Matcher/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── app.py
│   └── requirements.txt
└── README.md  # (this file)
```

---

## Backend
- **Framework:** FastAPI
- **Location:** `backend/`
- **Key file:** `main.py`
- **Endpoints:**
  - `POST /analyze_match` — Analyze and match resume with job description
  - `GET /` — Health check
- **Skills Extraction:**
  - Uses a transformer-based NER model
  - Adds custom keyword extraction for programming languages and technical terms
- **How to run:**
  1. `cd backend`
  2. `pip install -r requirements.txt`
  3. `uvicorn main:app --reload`
  4. Visit [http://localhost:8000/docs](http://localhost:8000/docs) for API docs

---

## Frontend
- **Framework:** Streamlit
- **Location:** `frontend/`
- **Key file:** `app.py`
- **Features:**
  - Upload resume and job description (file or text)
  - Displays extracted skills, match score, and suggestions
  - Connects to backend at `http://localhost:8000/analyze_match`
- **How to run:**
  1. `cd frontend`
  2. `pip install -r requirements.txt`
  3. `streamlit run app.py`

---

## Example Workflow
1. Start the backend server (see above)
2. Start the frontend Streamlit app (see above)
3. Open the Streamlit UI in your browser
4. Upload a resume and job description (PDF/TXT or paste text)
5. View extracted skills, match score, and suggestions for improvement

---

## Author
Shreya Kumari
