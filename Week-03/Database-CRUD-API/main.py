from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()

DATABASE = "tasks.db"


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    if task_count == 0:
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Learn Python", False)
        )
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Build FastAPI", False)
        )
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Learn SQLite", True)
        )

    connection.commit()
    connection.close()


initialize_database()


@app.get("/")
def home():
    return {"message": "Task Database API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, False)
    )

    new_task_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": new_task_id,
        "title": task.title,
        "done": False
    }

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    # Check whether the task exists
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    # Validate title
    if updated_task.title is not None and not updated_task.title.strip():
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    if updated_task.title is not None:
        cursor.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (updated_task.title, task_id)
        )

    # Update done status if provided
    if updated_task.done is not None:
        cursor.execute(
            "UPDATE tasks SET done = ? WHERE id = ?",
            (updated_task.done, task_id)
        )

    connection.commit()

    # Get updated task
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()
    connection.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether the task exists
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    # Delete the task
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return