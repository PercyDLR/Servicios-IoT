from mysql import connector
from datetime import datetime

def inicializarDB(pwd) -> connector.connection.MySQLConnection: 
    mydb = connector.connect(
        host="ec2-3-140-98-238.us-east-2.compute.amazonaws.com",
        user="root",
        password=pwd,
        database="IoT_DB"
    )
    return mydb

def getSensor(pwd: str, sensorID: str):
    sensor = {}

    with inicializarDB(pwd) as mydb:
        # Existe el sensor
        try:
            cursor = mydb.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM sensor WHERE id={sensorID}")
            sensor = cursor.fetchone()

            # print(f"Se obtuvo {sensor=}")
        # El sensor no existe
        except:
            query = "INSERT INTO sensor (id, id_lugar, nombre, estado) VALUES (%s,%s,%s,%s)"
            valores = (sensorID,1,sensorID,1)
            cursor = mydb.cursor(dictionary=True)
            cursor.execute(query,valores)
            mydb.commit()

            sensor = {
                "id": sensorID,
                "id_lugar": 1,
                "nombre": sensorID,
                "estado": 1
            }
            # print(f"Se creó el {sensor=}")

    # print(f"Sensor en la salida = {sensor}")
    return sensor

def insertMedicion(pwd: str, datos: dict, sensor: dict):

    with inicializarDB(pwd) as mydb:
        query = "INSERT INTO medicion (id_lugar, temp_avg, humedad_avg) VALUES (%s,%s,%s)"
        valores = (sensor["id_lugar"],datos["temperatura"],datos["humedad"])

        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query,valores)
        mydb.commit()
        medicionID = cursor.lastrowid

        cursor.execute("INSERT INTO bateria (id_sensor,valor) VALUES (%s,%s)",(datos['deviceId'],datos['bateria']))
        mydb.commit()
        bateriaID = cursor.lastrowid


        return (medicionID,bateriaID)