# ResearchRadar 🔎

A research paper discovery and management API built with Flask, PostgreSQL, and OpenAlex.

ResearchRadar is an ongoing backend development project designed to make academic research easier to discover and organize. It integrates with the OpenAlex API to retrieve academic papers and stores paper metadata in a PostgreSQL database for persistent access.

The project is being developed incrementally, with a focus on learning backend development, REST APIs, database integration, and reliable external API communication.

---

## Current Features

- **Academic paper search:** Retrieve papers from OpenAlex using a search query.
- **Paper metadata extraction:** Extract paper titles, OpenAlex IDs, authors, publication years, and citation counts.
- **PostgreSQL persistence:** Store retrieved paper metadata for later access.
- **Duplicate prevention:** Use PostgreSQL conflict handling to avoid inserting duplicate papers with the same OpenAlex ID.
- **Saved-paper retrieval:** Retrieve papers stored in the local database.
- **Title filtering:** Search saved papers by matching text in their titles.
- **Pagination:** Retrieve saved papers in pages with a configurable page size.
- **Error handling:** Handle external API connection failures, unsuccessful HTTP responses, and JSON parsing errors.

---

## Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming language |
| **Flask** | Web application framework |
| **Flask-RESTful** | REST API resource and endpoint management |
| **Flask-SQLAlchemy** | Database integration and ORM |
| **SQLAlchemy** | Database models and queries |
| **PostgreSQL** | Persistent relational database |
| **Requests** | HTTP communication with OpenAlex |
| **OpenAlex API** | Academic paper discovery and metadata source |

---

## API Endpoints

### 1. Search Academic Papers

```http
GET /api/v1/papers
```

Queries OpenAlex and returns matching papers. Retrieved paper metadata is automatically persisted to PostgreSQL.

#### Query Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `search` | String | `research` | Search term for academic papers |

#### Example Request
```http
GET /api/v1/papers?search=machine%20learning
```

The response contains a `results` array with paper titles, OpenAlex IDs, authors, publication years, and citation counts.

---

### 2. Retrieve Saved Papers

```http
GET /api/v1/saved
```

Retrieves papers previously saved in PostgreSQL.

#### Query Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `search` | String | *None* | Filter saved papers by matching text in title |
| `page` | Integer | `1` | Page number to retrieve |
| `per_page` | Integer | `20` | Number of papers per page (Max: `100`) |

#### Example Requests

* **Retrieve saved papers (Default page 1, 20 items):**
  ```http
  GET /api/v1/saved
  ```

* **Search saved papers by title:**
  ```http
  GET /api/v1/saved?search=neural%20networks
  ```

* **Retrieve page 2 with 10 papers per page:**
  ```http
  GET /api/v1/saved?page=2&per_page=10
  ```

* **Combine search and pagination:**
  ```http
  GET /api/v1/saved?search=machine&page=1&per_page=5
  ```

The response includes the requested page number, page size, and a results array containing the matching papers.

---

## Database Design

The `PaperModel` schema stores:

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Internal database primary key |
| `openalex_id` | String | Unique identifier for the paper in OpenAlex (Unique constraint) |
| `title` | String | Paper title |
| `authors` | JSON | Author names stored as JSON |
| `year` | Integer | Publication year (nullable) |
| `cited_by_count` | Integer | Citation count reported by OpenAlex |

*Duplicate Prevention:* PostgreSQL `ON CONFLICT (openalex_id) DO NOTHING` logic prevents duplicate records when the same paper is retrieved multiple times.

---

## Setup & Installation

### Prerequisites

- **Python 3.10+**
- **PostgreSQL** installed and running
- **Git**

### Step-by-Step Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd ResearchRadar
   ```

2. **Create and activate a virtual environment:**
   * Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   * Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root directory (or export the variable in your terminal) and configure your database URI:
   ```env
  # .env.example
      DATABASE_URL=postgresql://<username>:<password>@localhost:5432/research_radar
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will run locally on `http://127.0.0.1:5000`. Database tables will automatically initialize on startup.

---

## Current Limitations

- Search filtering on saved papers matches titles only.
- Pagination returns the current page and page size but does not yet report total count or total pages.
- Database migrations are handled on startup via `db.create_all()` rather than Flask-Migrate / Alembic workflows.
- Application currently runs on Flask's built-in development server.

---

## Roadmap

- [x] Integrate OpenAlex API
- [x] Extract and store paper metadata in PostgreSQL
- [x] Implement duplicate prevention (`ON CONFLICT`)
- [x] Title search and pagination for saved papers
- [ ] Add total records and total pages metadata to paginated responses
- [ ] Set up database migration workflow (Flask-Migrate)
- [ ] Implement citation-graph analysis endpoint
- [ ] Build a frontend web client

---

## License

This project is currently unlicensed.