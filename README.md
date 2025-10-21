# HNG STAGE ONE TASK

This project is a FastAPI-based API for advanced string analysis and management. It allows users to analyze, store, retrieve, filter, and delete string data with rich metadata. Key features include:

- Analyzing strings for properties such as length, palindrome status, unique characters, word count, and character frequency.
- Storing analyzed string information in a PostgreSQL database.
- Retrieving all strings or filtering them using query parameters (e.g., palindrome, length, word count, specific characters).
- Natural language filtering: users can query strings using plain English (e.g., "all single word palindromic strings").
- Deleting strings and their associated metadata from the database.

The API is designed for extensibility and demonstrates best practices in Python, FastAPI, SQLAlchemy, and modern backend development.

## Setup

Follow these steps to set up the project on your local machine.

### 1. Create a Virtual Environment

Create a virtual environment to isolate the project dependencies.

```sh
python3 -m venv .venv
```
or

```sh
virtualenv venv
```

### 2. Activate Virtual Environment

Activate the virtual environment. The command differs based on your operating system:

On macOS and Linux:
```sh
source .venv/bin/activate
```

On Windows:
```sh
.venv\Scripts\activate
```

### 3. Install Project Dependencies

Install the required dependencies from requirements.txt.

```sh
pip install -r requirements.txt
```

### 4. Create a .env File 

Create a .env file by copying the provided .env.sample file. This file will hold your environment variables.

```sh
cp .env.sample .env
```

```sh
cp .env.config.sample .env
```
### 5. Run Database Migrations

Use Alembic to run database migrations. You can create a new migration and apply it or just apply existing migrations.

To create a new migration:
```sh
alembic revision --autogenerate -m 'initial migration'
```

To apply existing migrations:
```sh
alembic upgrade head
```

### 6. Start the Server

Start the FastAPI server with Uvicorn. The --reload flag will auto-reload the server on code changes.

```sh
uvicorn main:app --reload
```


## Project Structure

```graphql
.
├── alembic/                   # Alembic migrations
├── api/                       # API routes and endpoints
│   ├── v1/                    # Version 1 of the API
│   └── ...
├── core/                      # Core configurations and utilities
├── models/                    # Database models
├── schemas/                   # Pydantic schemas (data validation and serialization)
├── main.py                    # Application entry point
├── .env.sample                # Sample environment variables file
├── requirements.txt           # Project dependencies
└── ...
```
