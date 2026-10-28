# Library Management System

A lightweight asynchronous REST API for managing a library catalog, built with **FastAPI**, **SQLAlchemy 2.x**, **PostgreSQL**, and **Pydantic v2**.

## Overview

The Library Management System provides a REST API for creating, retrieving, updating, and deleting book records. It uses SQLAlchemy's asynchronous API to communicate with PostgreSQL and keeps the application organized into separate layers for routing, business logic, database queries, models, and schemas.

## Features

- Full CRUD operations for books
- Asynchronous database access with SQLAlchemy `AsyncSession`
- PostgreSQL persistence through `asyncpg`
- Environment-based database configuration using `.env`
- Request and response validation with Pydantic v2
- Duplicate book detection using title, author, and publication year
- Cursor-based pagination when listing books
- Automatic API documentation through Swagger UI and ReDoc
- Layered architecture: routers, services, CRUD, models, and schemas

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x (async)
- PostgreSQL
- `asyncpg`
- Pydantic v2
- `python-dotenv`

## Project Structure

```text
Library-Management-System/
├── app/
│   ├── crud/
│   │   └── book_crud.py        # Asynchronous database queries
│   ├── database/
│   │   └── database.py         # Async engine, session factory, Base, get_db
│   ├── models/
│   │   └── book_model.py       # SQLAlchemy Book model
│   ├── routers/
│   │   └── book_router.py      # API route definitions
│   ├── schemas/
│   │   └── book_schemas.py     # Pydantic request/response schemas
│   └── services/
│       └── book_service.py     # Business logic and HTTP errors
├── main.py                     # Application entry point
├── .env                        # Local environment variables (not committed)
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

### Request flow

```text
Router  →  Service  →  CRUD  →  PostgreSQL
(HTTP)     (rules)     (queries)  (database)
```

- **Routers** define endpoints and handle HTTP parameters and dependencies.
- **Services** contain business rules and raise HTTP errors.
- **CRUD** functions execute database queries.
- **Models** map Python classes to database tables.
- **Schemas** validate incoming data and shape outgoing responses.
- **Database** configures the asynchronous SQLAlchemy engine and session factory.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mhkn-2007/Library-Management-System.git
cd Library-Management-System
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If `requirements.txt` is up to date:

```bash
python -m pip install -r requirements.txt
```

The main packages used by the project are:

```bash
python -m pip install fastapi "uvicorn[standard]" "sqlalchemy[asyncio]" asyncpg pydantic python-dotenv
```

### 4. Create the PostgreSQL database

Make sure PostgreSQL is installed and running. Create a database for the project, for example:

```sql
CREATE DATABASE library_management_system;
```

Use a PostgreSQL role that has permission to connect to and work with this database.

### 5. Configure environment variables

Create a `.env` file in the project root, alongside `main.py`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/library_management_system
```

Replace `YOUR_PASSWORD` with your PostgreSQL password. Do not add `DATABASE_URL=` twice. The URL format is:

```text
postgresql+asyncpg://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

Keep `.env` out of version control. Add this entry to `.gitignore`:

```gitignore
.env
```

If your password contains URL-reserved characters such as `@`, `/`, or `#`, URL-encode those characters in the connection URL.

### 6. Run the application

Run the command from the project root:

```bash
python -m uvicorn main:app --reload
```

If the entry point is configured to run Uvicorn directly, you can also use:

```bash
python main.py
```

Once the server is running, open:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

The application is configured to create registered model tables on startup if its lifespan handler calls `Base.metadata.create_all`. This project does not currently use Alembic migrations.

## API Endpoints

| Method | Endpoint | Description | Success status |
| --- | --- | --- | --- |
| `GET` | `/books` | List books with pagination | `200 OK` |
| `GET` | `/books/{book_id}` | Retrieve one book | `200 OK` |
| `POST` | `/books` | Create a book | `201 Created` |
| `PATCH` | `/books/{book_id}` | Partially update a book | `200 OK` |
| `DELETE` | `/books/{book_id}` | Delete a book | `204 No Content` |

## Book Schema

| Field | Type | Rules |
| --- | --- | --- |
| `id` | integer | Generated primary key |
| `title` | string | 1–50 characters |
| `author_name` | string | 1–50 characters |
| `publish_year` | integer | Between 1450 and the current year |

## Validation and Error Responses

- `title` and `author_name` must contain between 1 and 50 characters.
- `publish_year` must be between `1450` and the current year.
- A book with the same title, author, and publication year is rejected as a duplicate.
- `book_id` must be greater than `0`.
- `PATCH` requests can include only the fields to update; omitted fields remain unchanged.

| Status | Meaning |
| --- | --- |
| `400 Bad Request` | A book with the same title, author, and publication year already exists |
| `404 Not Found` | The requested book does not exist |
| `422 Unprocessable Entity` | Request data or parameters failed validation |

Example error response:

```json
{
  "detail": "Book not found"
}
```

## Pagination

`GET /books` supports cursor-based pagination using these query parameters:

| Parameter | Default | Description |
| --- | --- | --- |
| `limit` | `10` | Maximum number of books to return |
| `last_id` | omitted | Return books whose ID is greater than this value |

Example:

```text
GET /books?limit=5&last_id=10
```

The response includes an `items` array and `next_last_id`. Use the returned `next_last_id` as the `last_id` value in the next request. If `items` is empty, there are no more results for that query.

Example response:

```json
{
  "items": [
    {
      "id": 11,
      "title": "Dune",
      "author_name": "Frank Herbert",
      "publish_year": 1965
    }
  ],
  "next_last_id": 11
}
```

## Example Requests

### Create a book

```bash
curl -X POST "http://127.0.0.1:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Dune",
    "author_name": "Frank Herbert",
    "publish_year": 1965
  }'
```

Example response:

```json
{
  "id": 1,
  "title": "Dune",
  "author_name": "Frank Herbert",
  "publish_year": 1965
}
```

### List books

```bash
curl "http://127.0.0.1:8000/books?limit=10"
```

### Retrieve a book

```bash
curl "http://127.0.0.1:8000/books/1"
```

### Partially update a book

Send only the fields that should change:

```bash
curl -X PATCH "http://127.0.0.1:8000/books/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Dune Messiah"}'
```

### Delete a book

```bash
curl -X DELETE "http://127.0.0.1:8000/books/1"
```

## Notes

- PostgreSQL must be running and the database specified by `DATABASE_URL` must already exist.
- Keep `.env` and other secrets out of source control.
- The project does not currently use Alembic. `Base.metadata.create_all` creates missing tables but does not update existing tables when model columns change. Use migrations for schema changes in a long-lived project.
- The project focuses on the book catalog; member management and borrowing workflows are not implemented.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
