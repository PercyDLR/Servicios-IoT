from mysql import connector, MySQLConnection
import dataclasses

@dataclasses
class Lugar:
    id: int
    nombre: str
    latitud: float
    longitud: float
    
@dataclasses
class Sensor:
    id: int
    id_lugar: Lugar
    nombre: str
    estado: bool

@dataclasses
class Medicion:
    id: int
    id_lugar: Lugar
    temp_avg: float
    humedad_avg: float
    timestamp: int

@dataclasses
class Bateria:
    id: int
    id_sensor: Sensor
    valor: float
    timestamp: int

def inicializarDB(): 
    mydb = connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="servicios-iot"
    )
    return mydb

def getSensor(mydb: MySQLConnection, lugariD: int) -> Lugar:
    mydb.cursor().execute("SELECT * FROM sensor WHERE lug")
    


