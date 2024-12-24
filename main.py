from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "glossary.db"

# Модель данных для термина
class Term(BaseModel):
    key: str
    value: str

@app.get("/terms", response_model=List[Term])
def get_all_terms():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM glossary")
        terms = cursor.fetchall()
    return [{"key": key, "value": value} for key, value in terms]

@app.get("/terms/{key}", response_model=Term)
def get_term(key: str):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM glossary WHERE key = ?", (key,))
        result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return {"key": result[0], "value": result[1]}

@app.post("/terms", response_model=Term)
def add_term(new_term: Term):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO glossary (key, value) VALUES (?, ?)", (new_term.key, new_term.value))
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Термин уже существует")
    return new_term

@app.put("/terms/{key}", response_model=Term)
def update_term(key: str, updated_term: Term):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE glossary SET value = ? WHERE key = ?", (updated_term.value, key))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Термин не найден")
        conn.commit()
    return updated_term

@app.delete("/terms/{key}", response_model=str)
def delete_term(key: str):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM glossary WHERE key = ?", (key,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Термин не найден")
        conn.commit()
    return f"Термин '{key}' успешно удалён"
