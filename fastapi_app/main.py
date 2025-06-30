from fastapi import FastAPI
import os
import asyncpg

app = FastAPI()

async def get_db_connection():
    return await asyncpg.connect(
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        database=os.getenv("POSTGRES_DB", "postgres"),
        host=os.getenv("POSTGRES_HOST", "db"),
    )

@app.on_event("startup")
async def startup():
    conn = await get_db_connection()
    await conn.execute(
        "CREATE TABLE IF NOT EXISTS items(id serial PRIMARY KEY, name text);"
    )
    await conn.close()

@app.get("/items")
async def read_items():
    conn = await get_db_connection()
    rows = await conn.fetch("SELECT id, name FROM items;")
    await conn.close()
    return [dict(r) for r in rows]

@app.post("/items/{name}")
async def create_item(name: str):
    conn = await get_db_connection()
    await conn.execute("INSERT INTO items(name) VALUES($1);", name)
    await conn.close()
    return {"message": "item created"}
