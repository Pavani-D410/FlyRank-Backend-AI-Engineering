# Containerized Task API

A RESTful CRUD API built with **FastAPI** and **PostgreSQL**, containerized using **Docker** and **Docker Compose**.

This project demonstrates how an application can switch from an in-memory storage approach to a real PostgreSQL repository without putting database SQL logic inside the API routes.

---

## Features

- Create tasks
- Get all tasks
- Get a task by ID
- Update tasks
- Delete tasks
- PostgreSQL database
- Docker containerization
- Docker Compose for running the complete stack
- Persistent PostgreSQL storage using a Docker volume
- Environment variables using `.env`
- Swagger API documentation

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- psycopg2
- Docker
- Docker Compose

---

## Project Structure

```text
Containerized-Stack/
│
├── app/
│   ├── main.py
│   ├── database.py
│   └── repository.py
│
├── sql/
│   └── init.sql
│
├── screenshots/
│   ├── swagger.png
│   └── persistence.png
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

> `.env` is not committed to GitHub because it contains local database configuration.

---

# Architecture

The application follows a layered structure:

```text
Client / Swagger
       ↓
FastAPI Routes
       ↓
PostgresTaskRepository
       ↓
Database Connection
       ↓
PostgreSQL
```

The API routes do not contain SQL queries.

All database operations are handled by the PostgreSQL repository.

This demonstrates that the storage implementation can be changed independently of the API routes.

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
POSTGRES_DB=taskdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:your_password@db:5432/taskdb
```

A `.env.example` file is included in the repository as a template.

The `.env` file is included in `.gitignore`.

---

# Database

The application uses PostgreSQL.

The database table is created using:

```text
sql/init.sql
```

The `tasks` table contains:

| Column | Description |
|---|---|
| `id` | Unique task ID |
| `title` | Task title |
| `done` | Task completion status |

---

# Run the Complete Stack

Make sure **Docker Desktop is running**.

Open a terminal inside the project directory and run:

```bash
docker compose up --build
```

This command starts:

- FastAPI application
- PostgreSQL database

The FastAPI application will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API home endpoint |
| GET | `/health` | Check API health |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

---

# Example Task

## Create a Task

**POST `/tasks`**

Request:

```json
{
  "title": "Learn Docker"
}
```

Example response:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "done": false
}
```

---

# Docker Compose

The project uses Docker Compose to run both services together:

```text
Docker Compose
     │
     ├── FastAPI Application
     │
     └── PostgreSQL Database
              │
              └── Docker Volume
```

The complete stack can be started with one command:

```bash
docker compose up
```

---

# PostgreSQL Persistence

PostgreSQL data is stored using a Docker named volume:

```text
postgres_data
```

The Docker volume ensures that database data persists even when containers are stopped and started again.

## Persistence Test

Persistence was tested using the following steps:

1. Started the application and PostgreSQL using:

   ```bash
   docker compose up --build
   ```

2. Created a task using the FastAPI API.

3. Confirmed the task using:

   ```text
   GET /tasks
   ```

4. Stopped the running containers.

5. Started the stack again using:

   ```bash
   docker compose up
   ```

6. Called:

   ```text
   GET /tasks
   ```

7. The previously created task was still present.

This confirms that PostgreSQL data persists across an application and container restart.

---

---

# Assignment Requirements Completed

- [x] PostgreSQL runs in Docker
- [x] PostgreSQL uses a persistent Docker volume
- [x] Database configuration is stored in `.env`
- [x] `.env` is gitignored
- [x] `.env.example` is included in the repository
- [x] PostgreSQL table is created using `init.sql`
- [x] PostgreSQL repository handles database operations
- [x] API routes do not contain SQL queries
- [x] FastAPI and PostgreSQL run together using Docker Compose
- [x] The complete stack starts with `docker compose up`
- [x] Database persistence was tested and confirmed

---

## Author

FlyRank Backend & AI Engineering Internship Assignment — BE-04