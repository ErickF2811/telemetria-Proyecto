from fastapi import FastAPI, Query, Request, HTTPException
from pydantic import BaseModel

from datetime import datetime


from fastapi.responses import HTMLResponse, JSONResponse
from clickhouse_driver import Client
import clickhouse_connect
import socket
import threading

import time
import requests




# Conectar a ClickHouse


app = FastAPI()

# Modelo de datos para la solicitud de inserción en la tabla FlujoAgua
class FlujoAguaRequest(BaseModel):
    ID_esp: int
    Flujo_de_agua: float
    Cantidad_agua: float

@app.get("/")
def read_root():
    # Verificar la conexión a ClickHouse
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='')
    result = client.query("SELECT 'Conexión Exitosa!'")
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='example_db')
    result = client.query("SHOW TABLES")
    print(result.result_rows)  # This should list all tables in 'example_db'

    return {"message": result.result_rows}

@app.post("/insert_flujo_agua")
def insert_flujo_agua(data: FlujoAguaRequest):
    try:
        # Conexión a ClickHouse
        client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='example_db')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Consulta de inserción en la tabla FlujoAgua
        query = f"""
    INSERT INTO example_db.FlujoAgua (ID_esp, Time_stam, Flujo_de_agua, Cantidad_agua)
    VALUES ({data.ID_esp}, '{current_time}', {data.Flujo_de_agua}, {data.Cantidad_agua})"""

        client.command(query, {
            "ID_esp": data.ID_esp,
            "Time_stam":current_time,
            "Flujo_de_agua": data.Flujo_de_agua,
            "Cantidad_agua": data.Cantidad_agua
        })
        return {"message": "Datos insertados correctamente en FlujoAgua"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")