# Library Management API

A containerized Library Management REST API built using Flask, PostgreSQL, SQLAlchemy, and Docker.

This project provides a RESTful backend for managing books in a library. It supports book creation, retrieval, updating, deletion, filtering, borrowing, and returning. The application uses PostgreSQL for persistent data storage and Docker Compose to run the API and database as separate services.

## Features

- Create new books
- Retrieve all books
- Retrieve a single book by ID
- Filter books by author
- Filter books by genre
- Update book information
- Delete books
- Borrow books
- Return books
- Track total and available copies
- Health check endpoint
- Simple web frontend
- PostgreSQL database
- SQLAlchemy ORM
- Docker containerization
- Docker Compose for multi-container deployment
- Environment-based database configuration
- REST API testing using Postman

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming language |
| Flask | REST API framework |
| Flask-SQLAlchemy | Database ORM integration |
| SQLAlchemy | Database interaction |
| PostgreSQL | Relational database |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| HTML | Frontend |
| Postman | API testing |
| Git | Version control |
| GitHub | Source code hosting |

## System Architecture

text
                    +----------------------+
                    |        Client        |
                    |  Browser / Postman   |
                    +----------+-----------+
                               |
                               | HTTP Requests
                               v
                    +----------------------+
                    |      Flask API       |
                    |                      |
                    |  REST Endpoints      |
                    |  CRUD Operations      |
                    |  Borrow / Return     |
                    |  Health Check        |
                    +----------+-----------+
                               |
                               | SQLAlchemy
                               v
                    +----------------------+
                    |     PostgreSQL       |
                    |       Database       |
                    +----------------------+

              Docker Compose manages the
              Flask API and PostgreSQL services.
Project Structure
Library/
│
├── templates/
│   └── index.html
│
├── app.py
├── config.py
├── extensions.py
├── models.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── .env
└── README.md

File	Description
app.py ===>	Main Flask application and API routes
config.py	===> Application and database configuration
extensions.py ===>	SQLAlchemy database initialization
models.py ===>	Database models
templates/index.html ===>	Simple frontend interface
Dockerfile ===>	Instructions for building the API container
docker-compose.yml ===>	Defines API and PostgreSQL services
requirements.txt ===>	Python dependencies
.dockerignore	===> Files excluded from Docker build context
.gitignore ===>	Files excluded from Git
.env ===>	Environment-specific configuration
Database Schema

The application uses PostgreSQL as the primary database.
The main table is:
books
Books Table
Column	Description
id	Unique identifier for the book
title	Title of the book
author	Author of the book
genre	Genre or category of the book
isbn	ISBN number
total_copies	Total number of copies owned by the library
available_copies	Number of copies currently available
added_on	Date and time when the book was added
Environment Configuration

The application uses an environment variable for the PostgreSQL database connection.

Create a .env file in the project root:

DATABASE_URL=postgresql://postgres:password@db:5432/library_db
Replace the database username, password, and other values according to your configuration.
The .env file contains sensitive configuration and should not be committed to GitHub.
Make sure .env is included in .gitignore:

.env
venv/
__pycache__/
Running the Project with Docker
Prerequisites

Make sure the following are installed:

Python
Docker Desktop
Git
Postman
Step 1: Clone the Repository
git clone https://github.com/nithik-b/Library-management.git
Step 2: Open the Project Directory
cd Library-management
Step 3: Create the Environment File

Create a file named:

.env

Add the database connection:

DATABASE_URL=postgresql://postgres:password@db:5432/library_db
Step 4: Build and Start the Application

Run:

docker compose up --build

Docker Compose will:

Build the Flask API image
Create the application container
Create the PostgreSQL container
Create the Docker network
Create the PostgreSQL volume
Start both services
Connect the Flask API to PostgreSQL
Accessing the Application

Once the containers are running, open:

http://localhost:5000

The application frontend should be available through the browser.

Health Check

The project includes a health check endpoint.

Open:

http://localhost:5000/health

Expected response:

{
    "status": "healthy",
    "service": "library-api"
}

This endpoint can be used to verify that the API is running correctly.

REST API Documentation
1. Create a Book
Endpoint
POST /books
Request Body
{
    "title": "Clean Code",
    "author": "Robert Martin",
    "genre": "Programming",
    "isbn": "9780132350884",
    "total_copies": 5
}
Response
{
    "id": 1,
    "title": "Clean Code",
    "author": "Robert Martin",
    "genre": "Programming",
    "isbn": "9780132350884",
    "total_copies": 5,
    "available_copies": 5
}
2. Get All Books
Endpoint
GET /books
Example
http://localhost:5000/books

This endpoint returns all books stored in the database.

3. Filter Books by Author
Endpoint
GET /books?author=<author>
Example
http://localhost:5000/books?author=Robert

The API performs a case-insensitive search for the specified author.

4. Filter Books by Genre
Endpoint
GET /books?genre=<genre>
Example
http://localhost:5000/books?genre=Programming

The API returns books matching the specified genre.

5. Get a Single Book
Endpoint
GET /books/<book_id>
Example
GET /books/1

If the book exists, its details are returned.

If the book does not exist, the API returns:

{
    "error": "Book not found"
}

with HTTP status code:

404
6. Update a Book
Endpoint
PUT /books/<book_id>
Example
PUT /books/1
Request Body
{
    "title": "Clean Code Updated",
    "author": "Robert Martin",
    "genre": "Programming",
    "total_copies": 10,
    "available_copies": 8
}

The book information is updated in the PostgreSQL database.

7. Delete a Book
Endpoint
DELETE /books/<book_id>
Example
DELETE /books/1

Successful response:

{
    "message": "Book 1 deleted"
}
8. Borrow a Book
Endpoint
PATCH /books/<book_id>/borrow
Example
PATCH /books/1/borrow

When a book is borrowed:

available_copies = available_copies - 1

If no copies are available, the API returns:

{
    "error": "No copies available to borrow"
}
9. Return a Book
Endpoint
PATCH /books/<book_id>/return
Example
PATCH /books/1/return

When a book is returned:

available_copies = available_copies + 1

The API prevents the number of available copies from exceeding the total number of copies.

10. Health Check
Endpoint
GET /health
Example
GET http://localhost:5000/health
Response
{
    "status": "healthy",
    "service": "library-api"
}
API Summary
Method	Endpoint	Description
POST	/books	Create a new book
GET	/books	Get all books
GET	/books?author=...	Filter books by author
GET	/books?genre=...	Filter books by genre
GET	/books/<id>	Get a specific book
PUT	/books/<id>	Update a book
DELETE	/books/<id>	Delete a book
PATCH	/books/<id>/borrow	Borrow a book
PATCH	/books/<id>/return	Return a book
GET	/health	Check API health
Testing with Postman

The API was tested using Postman.

The following operations were tested successfully:

POST     /books
GET      /books
GET      /books/<id>
PUT      /books/<id>
DELETE   /books/<id>
PATCH    /books/<id>/borrow
PATCH    /books/<id>/return
GET      /health

Postman was used to verify:

HTTP status codes
JSON responses
Book creation
Book retrieval
Book updates
Book deletion
Borrowing logic
Returning logic
Error handling
Health check functionality
Docker Configuration

The application is divided into two Docker services.

+---------------------------+
|       library-api         |
|                           |
| Flask + SQLAlchemy        |
| Port: 5000                |
+-------------+-------------+
              |
              |
              v
+---------------------------+
|        library-db         |
|                           |
| PostgreSQL 16             |
| Port: 5432                |
+---------------------------+

Docker Compose provides networking between the API and database containers.

The Flask application connects to PostgreSQL using the Docker Compose service name rather than localhost.

Useful Docker Commands
Start the application
docker compose up
Build and start
docker compose up --build
Run in detached mode
docker compose up -d
Check container status
docker compose ps
View API logs
docker compose logs api
View database logs
docker compose logs db
View the latest API logs
docker compose logs api --tail=50
Stop the application
docker compose down
Stop and remove containers
docker compose down
Rebuild the application
docker compose up --build
Access PostgreSQL

The PostgreSQL database can be accessed from the running database container.

Example:

docker exec -it library-db psql -U postgres -d library_db

Inside PostgreSQL:

\dt

To view the books table:
SELECT * FROM books;
To exit PostgreSQL:
\q
Error Handling

The API provides appropriate responses for common error conditions.

Missing Required Fields

If title or author is missing:

{
    "error": "title and author are required"
}

HTTP status:

400 Bad Request
Book Not Found
{
    "error": "Book not found"
}

HTTP status:

404 Not Found
No Copies Available
{
    "error": "No copies available to borrow"
}

HTTP status:

400 Bad Request
All Copies Already Returned
{
    "error": "All copies are already returned"
}

HTTP status:
400 Bad Request

Data Persistence
PostgreSQL data is stored using a Docker volume.
This allows database data to persist even when the PostgreSQL container is stopped or recreated.
The application and database are connected through the Docker Compose network.

Security Considerations
Sensitive configuration is stored using environment variables.
The .env file should not be committed to the repository.

Recommended .gitignore entries:
.env
venv/
__pycache__/
*.pyc

Before pushing the project to GitHub, verify that no passwords, database credentials, or other secrets are included in the repository.

Learning Outcomes

This project helped demonstrate practical implementation of:

Python backend development
Flask REST API development
RESTful API design
CRUD operations
PostgreSQL database management
SQLAlchemy ORM
Database connectivity
Docker containerization
Docker Compose
Multi-container application architecture
Environment variable configuration
API testing with Postman
Git version control
GitHub repository management
Project Workflow
Client
   |
   v
HTTP Request
   |
   v
Flask REST API
   |
   v
Request Validation
   |
   v
SQLAlchemy ORM
   |
   v
PostgreSQL Database
   |
   v
JSON Response
   |
   v
Client
Future Improvements

The following features can be added in future versions:
JWT authentication
User registration and login
Admin and user roles
Swagger/OpenAPI documentation
Automated testing using Pytest
Database migrations using Flask-Migrate
Pagination
Advanced book search
Book categories
Borrower management
Borrowing history
AWS deployment
CI/CD using GitHub Actions
Application monitoring
Production WSGI configuration
Reverse proxy using Nginx

These features are not part of the current implementation and are listed as possible future improvements.

Project Status
Project Status: Completed

The current version successfully implements the core Library Management REST API with Flask, PostgreSQL, SQLAlchemy, Docker, Docker Compose, and Postman testing.

Author
Nithikbalaji S
Computer Science and Engineering Student

GitHub:
https://github.com/nithik-b

License
This project is created for educational and portfolio purposes.
