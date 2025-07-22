from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Enable CORS so React can connect to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database"
tasks_db = []
next_task_id = 0

# Pydantic model
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None

# Helper: find task index by ID
def find_task_index(task_id: int):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            return index
    return None

# Helper: check for duplicate title
def is_duplicate_title(title: str, exclude_id: Optional[int] = None) -> bool:
    for task in tasks_db:
        if task.title.lower() == title.lower() and task.id != exclude_id:
            return True
    return False

@app.get("/")
def read_root():
    return {"message": "FastAPI Task Manager backend is running."}

# ✅ Get all tasks
@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks_db

# ✅ Create a new task
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    global next_task_id
    if is_duplicate_title(task.title):
        raise HTTPException(status_code=400, detail="Task with this title already exists")
    
    task.id = next_task_id
    next_task_id += 1
    tasks_db.append(task)
    return task

# ✅ Get task by ID
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    index = find_task_index(task_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[index]

# ✅ Update task by ID
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    index = find_task_index(task_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if is_duplicate_title(updated_task.title, exclude_id=task_id):
        raise HTTPException(status_code=400, detail="Another task with this title already exists")
    
    updated_task.id = task_id
    tasks_db[index] = updated_task
    return updated_task

# ✅ Delete task by ID
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    index = find_task_index(task_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db.pop(index)
