from mysql import connector
from datetime import datetime

def inicializarDB(pwd) -> connector.connection.MySQLConnection: 
    mydb = connector.connect(
        host="localhost",
        user="percy",
        password=pwd,
        database="IoT_DB"
    )
    return mydb

def getSensor(pwd: str, sensorID: int):
    sensor = {}

    with inicializarDB(pwd) as mydb:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM sensor WHERE id={sensorID}")
        sensor = cursor.fetchone()
    return sensor

def insertMedicion(pwd: str, datos: dict, sensor: dict):

    with inicializarDB(pwd) as mydb:
        query = "INSERT INTO medicion (id_lugar, temp_avg, humedad_avg) VALUES (%s,%s,%s)"
        valores = (sensor["id_lugar"],datos["temp_avg"],datos["hum_avg"])

        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query,valores)

        medicionID = cursor.lastrowid

        cursor.execute(f"INSERT INTO bateria (id_sensor,valor) VALUES ({datos['id_sensor']},{datos['bateria']})")
        bateriaID = cursor.lastrowid

        return (medicionID,bateriaID)