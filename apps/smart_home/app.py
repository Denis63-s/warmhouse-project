from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import os

app = FastAPI(
    title="Smart Home API",
    description="Управление датчиками температуры через базу данных PostgreSQL.",
    version="1.0.0"
)

# Модель данных для сенсора
class Sensor(BaseModel):
    name: str
    location: str

# Функция подключения к БД
async def connect_db():
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        database=os.getenv("POSTGRES_DB", "smarthome"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    return conn

@app.post("/sensors", summary="Создать новый сенсор")
async def create_sensor(sensor: Sensor):
    conn = await connect_db()
    await conn.execute(
        'INSERT INTO sensors (name, location, temperature) VALUES ($1, $2, $3)',
        sensor.name, sensor.location, 0.0
    )
    await conn.close()
    return {"message": "Сенсор успешно создан"}

@app.get("/sensors", summary="Получить список всех сенсоров")
async def get_sensors():
    conn = await connect_db()
    rows = await conn.fetch('SELECT id, name, location, temperature FROM sensors')
    await conn.close()
    sensors = [
        {
            "id": row["id"],
            "name": row["name"],
            "location": row["location"],
            "temperature": row["temperature"]
        }
        for row in rows
    ]
    return sensors
