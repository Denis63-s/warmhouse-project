from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from random import uniform

app = FastAPI()

# Входная модель (без id)
class SensorIn(BaseModel):
    name: str
    type: str
    location: str
    unit: str

# Полная модель (с id и value)
class Sensor(SensorIn):
    id: str
    value: Optional[float] = None

# Хранилище сенсоров (в памяти)
sensors_db = {}

# GET /temperature
@app.get("/temperature")
def get_temperature(location: str = Query(None), sensorId: str = Query(None)):
    if not location:
        location = {
            "1": "Living Room",
            "2": "Bedroom",
            "3": "Kitchen"
        }.get(sensorId, "Unknown")
    if not sensorId:
        sensorId = {
            "Living Room": "1",
            "Bedroom": "2",
            "Kitchen": "3"
        }.get(location, "0")
    temperature = round(uniform(18.0, 28.0), 2)
    return {"sensorId": sensorId, "location": location, "temperature": temperature}

# POST /api/v1/sensors
@app.post("/api/v1/sensors", response_model=Sensor)
def create_sensor(sensor_data: SensorIn):
    sensor_id = str(uuid4())
    sensor = Sensor(**sensor_data.dict(), id=sensor_id)
    sensors_db[sensor.id] = sensor
    return sensor

# GET /api/v1/sensors
@app.get("/api/v1/sensors", response_model=List[Sensor])
def get_all_sensors():
    for s in sensors_db.values():
        if s.type == "temperature":
            s.value = round(uniform(18.0, 28.0), 2)
    return list(sensors_db.values())
