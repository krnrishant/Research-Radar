ResearchRadar 🔬
================

**ResearchRadar** is a research discovery project designed to help users search for academic papers and explore research connections.

**The project is currently in its early backend development stage. This initial version integrates the OpenAlex API with a Flask REST API and PostgreSQL database to retrieve, process, and store academic paper metadata. Current Features**



* **Academic paper search:** Fetches research papers from the OpenAlex API using a search query.

* **REST API:** Provides a Flask-RESTful endpoint for searching papers.

* **Metadata extraction:** Retrieves paper titles, OpenAlex IDs, publication years, citation counts, and author names.

* **PostgreSQL integration:** Stores paper metadata in a relational database.

* **JSON responses:** Returns structured search results to API clients.

* **Basic error handling:** Handles external API connection failures, unsuccessful HTTP responses, and JSON parsing errors.

Tech Stack
----------

* **Python** — Core programming language

* **Flask** — Web application framework

* **Flask-RESTful** — REST API resources and routing

* **Requests** — External API communication

* **Flask-SQLAlchemy** — ORM and database integration

* **SQLAlchemy** — Database models and queries

* **PostgreSQL** — Persistent data storage

* **OpenAlex API** — Academic research metadata

API Endpoint
------------

### Search for research papers

`GET /api/v1/papers`

**Query parameter**

| Parameter | Description                     | Default    |
| --------- | ------------------------------- | ---------- |
| `search`  | Search term for academic papers | `research` |

**Example request**
    GET /api/v1/papers?search=machine%20learning

**Example response**
    {  "results": [    {      "title": "Example Research Paper",      "openalex_id": "https://openalex.org/W123456789",      "cited_by_count": 42,      "year": 2024,      "authors": [        "Author One",        "Author Two"      ]    }  ]}

_The response above is illustrative; actual results depend on the OpenAlex API._
Database Structure
------------------

The current SQLAlchemy model is `PaperModel`, mapped to the `paper_model` table.

| Column           | Type    | Description                |
| ---------------- | ------- | -------------------------- |
| `id`             | Integer | Primary key                |
| `openalex_id`    | String  | Unique OpenAlex identifier |
| `title`          | Text    | Paper title                |
| `authors`        | JSON    | List of author names       |
| `year`           | Integer | Publication year           |
| `cited_by_count` | Integer | Number of citations        |

Paper metadata is added to the SQLAlchemy session and committed to PostgreSQL after processing the search results.
Setup and Installation
----------------------

### 1. Clone the repository

    git clone <your-repository-url>cd ResearchRadar

### 2. Create a virtual environment

    python -m venv venv

Activate it on Windows:
    .\venv\Scripts\Activate.ps1

### 3. Install dependencies

    pip install Flask Flask-RESTful requests Flask-SQLAlchemy "psycopg[binary]"

### 4. Configure PostgreSQL

Install PostgreSQL and create a database named `ResearchRadar`.

Set the database connection URI using an environment variable rather than hardcoding credentials in the source code.

Example PowerShell command:
    $env:DATABASE_URL = "postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/ResearchRadar"

Update the Flask configuration to read the variable:
    import osapp.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

Replace `USERNAME` and `PASSWORD` with your local PostgreSQL credentials. Do not commit passwords or other secrets to GitHub.

### 5. Run the application

    python app.py

The application currently calls `db.create_all()` within the Flask application context to create missing tables.

### 6. Test the endpoint

Open the following URL in your browser or an API client:
    http://127.0.0.1:5000/api/v1/papers?search=artificial%20intelligence
Current Development Status
--------------------------

**Implemented**

* Flask application and REST endpoint

* OpenAlex API integration

* Paper metadata extraction

* SQLAlchemy model

* PostgreSQL connection and table creation

* Basic external API error handling

* Database insertion workflow

**In progress / planned**

* Duplicate-paper detection before insertion

* Database transaction error handling and rollback

* Automated API tests

* Improved validation and defensive parsing

* Deployment to a production server

Project Roadmap
---------------

ResearchRadar is intended to grow beyond a basic paper-search API. Planned directions include:

* A user-facing research search interface

* Related-paper recommendations

* Citation relationship visualization

* Research topic and publication trend analysis

* Deployment so others can access the application

These are future goals, not features of the current implementation.
Learning Objectives
-------------------

This project is also a practical exercise in:

* Building REST APIs with Flask

* Consuming third-party APIs

* Processing nested JSON data

* Designing database models

* Persisting external data with SQLAlchemy

* Handling API and database errors

* Developing a larger application incrementally

Acknowledgements
----------------

* [OpenAlex](https://openalex.org/) for providing scholarly me
