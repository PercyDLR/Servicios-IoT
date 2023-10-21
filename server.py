from fastapi import FastAPI
from pydantic import BaseModel
from getpass import getpass
import funciones as fun

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

@app.post("/medicion")
async def nuevaMedicion(medicion: Medicion):
    
    # A partir del ID Sensor obtengo el IDlugar
    sensor = fun.getSensor(pwd,medicion.id_sensor)

    # Con esta infrmación ya se puede guardar la medición
    fun.insertMedicion(pwd,medicion.dict(),sensor)

    return sensor