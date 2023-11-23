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

app = FastAPI()

# Se define la información que recibirá el request
class SigfoxMessage(BaseModel):
    deviceId: str
    time: str
    humedad: float
    temperatura: float
    bateria: float

@app.post("/sigfox")
async def create_sigfox_message(message: SigfoxMessage):

    """  
    # Lo guarda en un CSV
    with open('sigfox_data.csv', mode ='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["deviceId", "time", "humedad", "temperatura", "bateria"])
        if file.tell() == 0:
            writer.writeheader()  # If file is empty, write a header
        writer.writerow(message.model_dump()) 
    """

    # A partir del ID Sensor obtengo el IDlugar
    sensor = fun.getSensor(pwd,message.deviceId)

    # Con esta infrmación ya se puede guardar la medición
    medicionID, bateriaID = fun.insertMedicion(pwd,message.model_dump(),sensor)

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
            "temp_avg": message.temperatura,
            "hum_avg": message.humedad,
            "timestamp": datetime.now()
        },
        "bateria": {
            "id": bateriaID,
            "valor": message.bateria,
            "timestamp": datetime.now()
        }
    }

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)