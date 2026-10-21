# ResearchRadar 🔍

> A full-stack research intelligence platform designed to bridge the gap in academic discovery through unified search and structured metadata extraction.

---

## 🛠️ Current Tech Stack (Week 1)

* **Backend Framework:** Python, Flask, Flask-RESTful
* **External Integration:** OpenAlex REST API (`requests`, connection timeouts, error handling)
* **Data Processing:** JSON normalization & schema transformation

---

## 🚀 Current Implementation (Week 1 Complete)

* **Research Paper Search API:** Implemented a RESTful endpoint (`GET /api/v1/papers?q={query}`) that queries the OpenAlex database.
* **Upstream Error Handling:** Integrated exception handling for connection timeouts, failed API requests, and malformed upstream responses.
* **Metadata Normalization:** Automatically extracts and structures raw payload attributes—including paper titles, citation counts (`cited_by_count`), publication years, and author arrays—into a clean, standardized JSON format.

---

## 🗺️ Execution Roadmap

- [x] **Week 1: Research Ingestion API** — OpenAlex integration, parameter handling, data normalization.
- [ ] **Week 2: Persistence & Local Library** — PostgreSQL integration, SQLAlchemy ORM models, and upsert caching logic.
- [ ] **Week 3: ML Recommendation Engine** — TF-IDF vectorization and cosine similarity algorithm for related paper discovery.
- [ ] **Week 4: React Web Client** — Interactive UI featuring real-time search, filters, and paper detail views.
- [ ] **Week 5: Production & VPS Deployment** — Automated unit tests, Gunicorn WSGI, Nginx reverse proxy, and SSL setup.

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ResearchRadar.git
cd ResearchRadar
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install Flask flask-restful requests
```

### 4. Run the Development Server
```bash
python app.py
```

### 5. Test the Endpoint
Open your browser or API client (Postman/Curl) and request:
```text
http://127.0.0.1:5000/api/v1/papers?q=quantum+computing
```

---
*This repository is actively updated week-by-week following a strict layered engineering roadmap.*