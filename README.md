# Library Management System

A lightweight REST API for managing a library catalog, built with FastAPI, SQLAlchemy, SQLite, and Pydantic.

## Overview

The Library Management System provides a simple way to manage a collection of books through a clean REST API. It supports creating records, retrieving one or many books, updating book information, and deleting books.

The project is intentionally minimal and uses a layered structure, which makes it a good starting point for a larger library application or for learning FastAPI and SQLAlchemy.

## Features

- Full CRUD support for books
- Request validation with Pydantic v2
- Duplicate record detection
- Cursor-based pagination for listing books
- SQLite persistence via the SQLAlchemy ORM
- Auto-generated Swagger UI and ReDoc documentation
- Layered architecture: routers, services, CRUD, models, and schemas

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy 2.x
- SQLite
- Pydantic v2
- Uvicorn

## Project Structure

```text
Library-Management-System/
├── app/
│   ├── crud/
│   │   └── book_crud.py        # Database queries
│   ├── database/
│   │   └── database.py         # Engine, session factory, Base, get_db
│   ├── models/
│   │   └── book_model.py       # SQLAlchemy Book model
│   ├── routers/
│   │   └── book_router.py      # Route definitions
│   ├── schemas/
│   │   └── book_schemas.py     # Pydantic request/response schemas
│   └── services/
│       └── book_service.py     # Business logic and HTTP errors
├── main.py                     # Application entry point
├── requirements.txt
├── LICENSE
├── README.md
└── .gitignore
```

### How a request flows

```text
Router  →  Service  →  CRUD  →  Database
(HTTP)     (rules)     (queries)  (SQLite)
```

- **Routers** define the endpoints and validate path and query parameters.
- **Services** hold business rules (for example, rejecting duplicates) and raise HTTP errors.
- **CRUD** contains the SQLAlchemy queries.
- **Models** map Python classes to database tables.
- **Schemas** define the shape of request and response data.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mhkn-2007/Library-Management-System.git
cd Library-Management-System
```

### 2. Create and activate a virtual environment

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

Run it from the project root, using either option:

```bash
# Option A: entry point
python main.py

# Option B: Uvicorn directly
python -m uvicorn main:app --reload
```

Once the server is running, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

The SQLite database file `app.db` and the `books` table are created automatically on first run.

## API Endpoints

| Method | Endpoint | Description | Success status |
| --- | --- | --- | --- |
| GET | `/books` | List books with pagination | 200 |
| GET | `/books/{book_id}` | Retrieve a specific book | 200 |
| POST | `/books` | Create a new book | 201 |
| PATCH | `/books/{book_id}` | Partially update a book | 200 |
| DELETE | `/books/{book_id}` | Delete a book | 204 |

## Book Schema

| Field | Type | Rules |
| --- | --- | --- |
| `id` | integer | Primary key, generated automatically |
| `title` | string | 1 to 50 characters |
| `author_name` | string | 1 to 50 characters |
| `publish_year` | integer | Between 1450 and the current year |

## Validation Rules

The API validates incoming data before saving it:

- `title` and `author_name` cannot be empty and must not exceed 50 characters
- `publish_year` must be between `1450` and the current year
- A book is rejected if another book has the same `title`, `author_name`, and `publish_year`
- `book_id` in the URL must be greater than 0

## Error Responses

| Status | When |
| --- | --- |
| 400 | A book with the same title, author, and year already exists |
| 404 | The requested book does not exist |
| 422 | The request body or parameters failed validation |

Error bodies follow FastAPI's standard format, for example:

```json
{ "detail": "Book not found" }
```

## Pagination

`GET /books` uses cursor-based pagination with two optional query parameters:

| Parameter | Default | Description |
| --- | --- | --- |
| `limit` | `10` | Maximum number of books to return |
| `last_id` | none | Return only books with an ID greater than this value |

The response contains the books and a cursor for the next page. To fetch the next page, pass `next_last_id` as `last_id`. When there are no more results, `items` is empty and `next_last_id` is `null`.

```bash
curl "http://127.0.0.1:8000/books?limit=5&last_id=10"
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

Example response:

```json
{
  "items": [
    {
      "id": 1,
      "title": "Dune",
      "author_name": "Frank Herbert",
      "publish_year": 1965
    }
  ],
  "next_last_id": 1
}
```

### Update a book

Send only the fields you want to change:

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

- `app.db` is created in the directory you start the server from. It is a local data file, so keep it in `.gitignore`.
- The project does not use database migrations. If you change the model's columns after `app.db` exists, delete the file so the table is recreated.

## Possible Next Steps

- Member management
- Borrowing and returning books
- Categories and genres
- Search and filtering
- Authentication and authorization
- Automated tests and CI workflows

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.