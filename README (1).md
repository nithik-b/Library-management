# Library / Book Inventory API

A simple CRUD REST API built with Flask + Flask-SQLAlchemy, backed by PostgreSQL.

## Project structure
```
library_api/
├── app.py            # Flask app + all routes
├── models.py          # Book model (SQLAlchemy ORM)
├── extensions.py       # shared db instance
├── config.py          # DB connection config
├── requirements.txt
├── .env.example        # copy to .env and fill in your DB URL
└── README.md
```

---

## Step 1 — Install PostgreSQL (if not already installed)

**Windows/Mac:** download from https://www.postgresql.org/download/
**Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Or skip local install entirely and use a free hosted Postgres like
[Neon](https://neon.tech) or [Supabase](https://supabase.com) — they give you
a ready `DATABASE_URL` in under a minute. Good option if you're short on time.

## Step 2 — Create the database

If using local Postgres:
```bash
psql -U postgres
CREATE DATABASE library_db;
\q
```

You don't need to manually create the `books` table — `app.py` does that for
you automatically on first run (`db.create_all()`).

## Step 3 — Set up the Python project

```bash
cd library_api
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Step 4 — Configure your DB connection

```bash
cp .env.example .env
```

Edit `.env` and set your real credentials:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/library_db
```

## Step 5 — Run the app

```bash
python app.py
```

You should see Flask running on `http://127.0.0.1:5000`, and the `books`
table will be created automatically.

---

## Step 6 — Test the API

### Create a book
```bash
curl -X POST http://127.0.0.1:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert Martin", "genre": "Programming", "isbn": "9780132350884", "total_copies": 3}'
```

### List all books
```bash
curl http://127.0.0.1:5000/books
```

### Filter by author or genre
```bash
curl "http://127.0.0.1:5000/books?author=Martin"
curl "http://127.0.0.1:5000/books?genre=Programming"
```

### Get one book
```bash
curl http://127.0.0.1:5000/books/1
```

### Update a book
```bash
curl -X PUT http://127.0.0.1:5000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"genre": "Software Engineering"}'
```

### Borrow a book (decreases available_copies)
```bash
curl -X PATCH http://127.0.0.1:5000/books/1/borrow
```

### Return a book (increases available_copies)
```bash
curl -X PATCH http://127.0.0.1:5000/books/1/return
```

### Delete a book
```bash
curl -X DELETE http://127.0.0.1:5000/books/1
```

---

## Key concepts you're practicing

- **ORM mapping**: `models.py` maps a Python class to a Postgres table —
  no raw SQL needed for basic operations.
- **Environment config**: DB credentials live in `.env`, not hardcoded —
  standard practice for any real project.
- **REST conventions**: POST=create, GET=read, PUT=update, DELETE=remove,
  PATCH=partial update (used here for borrow/return).
- **Validation & error handling**: 400 for bad input, 404 for missing
  resources, business-rule checks (can't borrow with 0 copies left).
- **Query filtering**: `?author=` and `?genre=` show how to build dynamic
  queries with SQLAlchemy.

## Stretch ideas (optional, once the base works)
- Add pagination: `?page=1&limit=10`
- Add a `members` table + a `borrowed_by` relationship (real foreign key)
- Add simple API key auth via a request header
- Write a Postman collection to save all these requests
