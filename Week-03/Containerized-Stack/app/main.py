from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.repository import PostgresTaskRepository


app = FastAPI(
    title="Containerized Task API"
)

repository = PostgresTaskRepository()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.get("/")
def home():
    return {
        "message": "Containerized Task API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/tasks")
def get_tasks():
    return repository.get_all_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    task = repository.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    return repository.create_task(task.title)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):

    if task.title is not None and not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    updated_task = repository.update_task(
        task_id,
        task.title,
        task.done
    )

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    deleted = repository.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return None