from fastapi import FastAPI
from pydantic import BaseModel
from getpass import getpass
from datetime import datetime
import funciones as fun
import csv

pwd = getpass("Ingrese la contraseña de la db: ")

# Inicializamos la db
try:
    mydb = fun.inicializarDB(pwd)
    mydb.close()
except:
    print("No se pudo acceder a la DB, verifique la información registrada")
    exit()

# Se define la información que recibirá el request
class Medicion(BaseModel):
    id_sensor: int
    temp_avg: float
    hum_avg: float
    bateria: float

app = FastAPI()


class SigfoxMessage(BaseModel):
    deviceId: str
    time: str
    humedad: float
    temperatura: float
    bateria: float

@app.post("/sigfox")
async def create_sigfox_message(message: SigfoxMessage):
    with open('sigfox_data.csv', mode ='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["deviceId", "time", "humedad", "temperatura", "bateria"])
        if file.tell() == 0:
            writer.writeheader()  # If file is empty, write a header
        writer.writerow(message.dict())
    return {"message": message}


@app.post("/medicion")
async def nuevaMedicion(medicion: Medicion):
    
    # A partir del ID Sensor obtengo el IDlugar
    sensor = fun.getSensor(pwd,medicion.id_sensor)

    # Con esta infrmación ya se puede guardar la medición
    medicionID, bateriaID = fun.insertMedicion(pwd,medicion.dict(),sensor)

    response = {
        "sensor": {
            "id": sensor["id"],
            "nombre": sensor["nombre"],
            "id_lugar": sensor["id_lugar"],
            "estado": sensor["estado"]
        },
        "medicion": {
            "id": medicionID,
            "id_lugar": sensor["id_lugar"],
            "temp_avg": medicion.temp_avg,
            "hum_avg": medicion.hum_avg,
            "timestamp": datetime.now()
        },
        "bateria": {
            "id": bateriaID,
            "valor": medicion.bateria,
            "timestamp": datetime.now()
        }
    }

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)