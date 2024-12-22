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
    Cantidad_agua: float

@app.get("/")
def read_root():
    # Verificar la conexión a ClickHouse
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='')
    result = client.query("SELECT 'Conexión Exitosa!'")
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='riego')
    result = client.query("SHOW TABLES")
    print(result.result_rows)  # This should list all tables in 'riego'

    return {"message": result.result_rows}

@app.post("/insert_flujo_agua")
def insert_flujo_agua(data: FlujoAguaRequest):
    try:
        # Conexión a ClickHouse
        client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='riego')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Consulta de inserción en la tabla FlujoAgua
        query = f"""
    INSERT INTO riego.FlujoAgua (ID_esp, Time_stam, Cantidad_agua)
    VALUES ({data.ID_esp}, '{current_time}', {data.Cantidad_agua})"""

        client.command(query, {
            "ID_esp": data.ID_esp,
            "Time_stam":current_time,
            "Cantidad_agua": data.Cantidad_agua
        })
        return {"message": "Datos insertados correctamente en FlujoAgua"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")

@app.get("/estado_umbral/{id_esp}")
def get_estado_umbral(id_esp: int):
    try:
        # Conexión a ClickHouse
        client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='riego')
        
        # Consulta para obtener el estado del umbral
        query = f"""
        SELECT Estado_Valvula
        FROM riego.EstadoValvula
        WHERE ID_esp = {id_esp}
        LIMIT 1
        """
        
        result = client.query(query)
        if not result.result_rows:
            return {"message": "No se encontraron datos para el ID_esp proporcionado."}
        
        umbral_superado = result.result_rows[0][0]
        return {"ID_esp": id_esp, "Estado_Valvula": umbral_superado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el estado del umbral: {str(e)}")