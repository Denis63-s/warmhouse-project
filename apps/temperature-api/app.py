from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import random

app = FastAPI(
    title="API Датчика Температуры",
    description="Сервис, который возвращает рандомную температуру по локации или sensorID.",
    version="1.0.0"
)

@app.get("/temperature", summary="Получить температуру по локации или sensorID")
def get_temperature(
    location: str = Query(default=None, description="Название комнаты (например, 'Living Room')"),
    sensorID: str = Query(default=None, description="Идентификатор датчика (например, '1')")
):
    # Определение location по sensorID
    if location is None:
        if sensorID == "1":
            location = "Living Room"
        elif sensorID == "2":
            location = "Bedroom"
        elif sensorID == "3":
            location = "Kitchen"
        else:
            location = "Unknown"
    
    # Определение sensorID по location
    if sensorID is None:
        if location == "Living Room":
            sensorID = "1"
        elif location == "Bedroom":
            sensorID = "2"
        elif location == "Kitchen":
            sensorID = "3"
        else:
            sensorID = "0"
    
    # Генерация случайной температуры
    temperature = round(random.uniform(-20.0, 40.0), 2)

    return JSONResponse(content={
        "sensorID": sensorID,
        "location": location,
        "temperature": temperature
    })
