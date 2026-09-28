import sqlite3

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Deploy an AI project", "done": False},
]

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

app = FastAPI(
    title="Task API",
    description="A simple CRUD API built using FastAPI.",
    version="1.0"
)

DB_NAME = "tasks.db"

conn = sqlite3.connect(DB_NAME)

conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0
    )
""")

conn.commit()

cursor = conn.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    conn.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        [
            ("Learn FastAPI", 0),
            ("Build CRUD API", 0),
            ("Test API", 1),
        ]
    )
    conn.commit()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid task data"}
    )

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": task.done
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{id}")
def update_task(id: int, task_update: TaskUpdate):
    if task_update.title is None and task_update.done is None:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided"
        )

    for task in tasks:
        if task["id"] == id:

            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )
                task["title"] = task_update.title

            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )

@app.get("/tasks", summary="Get all tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}", summary="Get a task by ID")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )



@app.get("/", summary="Get API information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get("/health", summary="Health check")
def health():
    return {
        "status": "ok"
    }

# Tested on Swagger UI and all endpoints are working as expected.