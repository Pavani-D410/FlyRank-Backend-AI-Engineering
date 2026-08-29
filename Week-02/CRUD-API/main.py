from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# Model for creating a task
class TaskCreate(BaseModel):
    title: str


# Model for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# In-memory list of tasks
tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Build API", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": True}
]


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# Get one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Create a new task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_task = {
        "id": max([task["id"] for task in tasks], default=0) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    for task in tasks:

        if task["id"] == task_id:

            # Update title if provided
            if updated_task.title is not None:

                if not updated_task.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )

                task["title"] = updated_task.title

            # Update done status if provided
            if updated_task.done is not None:
                task["done"] = updated_task.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )