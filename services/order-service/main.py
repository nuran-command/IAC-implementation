from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sqlite3
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "kanban.db"
IN_MEMORY_DB = {}

# SRE Incident Simulator check
def check_database_healthy():
    db_host = os.getenv("DB_HOST", "db")
    if db_host == "db_wrong":
        return False
    return True

# Initialize SQLite database schema
def init_db():
    if not check_database_healthy():
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS active_tasks (
                id TEXT PRIMARY KEY,
                title TEXT,
                desc TEXT,
                priority TEXT,
                points INTEGER,
                col TEXT,
                assignee_id TEXT,
                assignee_name TEXT
            )
        """)
        conn.commit()
        
        # Seed initial data if empty
        cursor.execute("SELECT COUNT(*) FROM active_tasks")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO active_tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                           ("task-5", "Implement OpenTelemetry Tracing", "Integrate Jaeger distributed tracing inside the payment API gateway.", "High", 5, "in_progress", "user-1", "Alice Cooper"))
            cursor.execute("INSERT INTO active_tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                           ("task-6", "Scale Swarm replica counts", "Increase worker instances for notification-service to handle alerts spikes.", "Medium", 3, "done", "user-2", "Bob Marley"))
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"SRE Fallback: Failed to initialize SQLite '{e}'. Using safe in-memory fallback state.")

# Load dynamic board items
def get_tasks():
    if not check_database_healthy():
        raise HTTPException(status_code=500, detail="Database connection failed")
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_tasks")
        rows = cursor.fetchall()
        conn.close()
        
        tasks_list = []
        for r in rows:
            tasks_list.append({
                "id": r[0], "title": r[1], "desc": r[2], "priority": r[3],
                "points": r[4], "column": r[5], "assignee_id": r[6], "assignee_name": r[7]
            })
        return tasks_list
    except Exception:
        # Return fallback in-memory state if SQLite fails
        if not IN_MEMORY_DB:
            IN_MEMORY_DB["task-5"] = {"id": "task-5", "title": "Implement OpenTelemetry Tracing", "desc": "Integrate Jaeger distributed tracing inside the payment API gateway.", "priority": "High", "points": 5, "column": "in_progress", "assignee_id": "user-1", "assignee_name": "Alice Cooper"}
            IN_MEMORY_DB["task-6"] = {"id": "task-6", "title": "Scale Swarm replica counts", "desc": "Increase worker instances for notification-service to handle alerts spikes.", "priority": "Medium", "points": 3, "column": "done", "assignee_id": "user-2", "assignee_name": "Bob Marley"}
        return list(IN_MEMORY_DB.values())

# Update task position/assignee
def update_task_state(task_id: str, col: str, assignee_id: str = None, assignee_name: str = None):
    if not check_database_healthy():
        raise HTTPException(status_code=500, detail="Database connection failed")
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM active_tasks WHERE id = ?", (task_id,))
        exists = cursor.fetchone()[0]
        
        if exists > 0:
            cursor.execute("UPDATE active_tasks SET col = ?, assignee_id = ?, assignee_name = ? WHERE id = ?", 
                           (col, assignee_id, assignee_name, task_id))
        else:
            # If moving from backlog/todo catalog, we insert it!
            title_mock = f"Imported Task {task_id}"
            desc_mock = "Imported from backlog catalog."
            cursor.execute("INSERT INTO active_tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (task_id, title_mock, desc_mock, "Medium", 3, col, assignee_id, assignee_name))
        conn.commit()
        conn.close()
    except Exception:
        # In-memory fallback
        if task_id in IN_MEMORY_DB:
            IN_MEMORY_DB[task_id]["column"] = col
            IN_MEMORY_DB[task_id]["assignee_id"] = assignee_id
            IN_MEMORY_DB[task_id]["assignee_name"] = assignee_name
        else:
            IN_MEMORY_DB[task_id] = {
                "id": task_id, "title": f"Imported Task {task_id}", 
                "desc": "Imported from backlog catalog.", "priority": "Medium",
                "points": 3, "column": col, "assignee_id": assignee_id, "assignee_name": assignee_name
            }

# Initialize on module loading
try:
    init_db()
except Exception:
    pass

@app.get("/")
def root():
    if not check_database_healthy():
        return {"service": "Order/Board Manager", "status": "offline", "error": "Database connection failed"}
    
    return {"service": "Order/Board Manager", "status": "online", "tasks": get_tasks()}

@app.post("/move")
def move_task(payload: dict):
    task_id = payload.get("task_id")
    new_col = payload.get("column")
    assignee_id = payload.get("assignee_id")
    assignee_name = payload.get("assignee_name")
    
    if not task_id or not new_col:
        raise HTTPException(status_code=400, detail="Missing task_id or column parameters")
        
    update_task_state(task_id, new_col, assignee_id, assignee_name)
    return {"status": "success", "msg": f"Moved task {task_id} to column {new_col}"}

@app.get("/health")
def health():
    if not check_database_healthy():
        return {"status": "unhealthy", "error": "Database connection failed"}
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    if not check_database_healthy():
        return "# HELP order_service_status Status of order service\n# TYPE order_service_status gauge\norder_service_status 0\n"
    return "# HELP order_service_status Status of order service\n# TYPE order_service_status gauge\norder_service_status 1\n"