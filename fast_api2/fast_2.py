from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from clickhouse_driver import Client
import clickhouse_connect
import socket
import threading

import time
import requests




# Conectar a ClickHouse



app = FastAPI()

@app.get("/")
def read_root():
    #enviar_resultado_bot()
    #socket.socket().connect(('telemetria-proyecto-clickhouse-1', 8123))
    print("Conexión establecida correctamente")
    #return {"message": "Hola, este es mi microservicio con FastAPI y ClickHouse"}
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='')

    # Ejemplo de consulta para verificar conexión
    result = client.query("SELECT * from  example_db.FlujoAgua;")
    print(result.result_rows)
    """
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='')
    result = client.query("SELECT 'Conexión Exitosa!'")
    """
    return {"message": result.result_rows}


@app.get("/visualizar")
def visualizar():
    #enviar_resultado_bot()
    #socket.socket().connect(('telemetria-proyecto-clickhouse-1', 8123))
    print("Conexión establecida correctamente")
    #return {"message": "Hola, este es mi microservicio con FastAPI y ClickHouse"}
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='example_db')

    # Ejemplo de consulta para verificar conexión
    result = client.query("SELECT * from  example_db.FlujoAgua;")
    print(result.result_rows)
    """
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='')
    result = client.query("SELECT 'Conexión Exitosa!'")
    """
    return {"message": result.result_rows}
