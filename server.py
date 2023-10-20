from fastapi import FastAPI
from pydantic import BaseModel

# Se define la clase del body
class Medicion(BaseModel):
    id_sensor: int
    temp_avg: float
    hum_avg: float

app = FastAPI()

@app.post("/")
async def nuevaMedicion(medicion: Medicion):
    return medicion