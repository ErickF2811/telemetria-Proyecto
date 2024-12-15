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

# Modelos de datos
class UmbralUpdate(BaseModel):
    ID_esp: int
    nuevo_umbral: str
    password: str

class PasswordUpdate(BaseModel):
    ID_esp: int
    nueva_password: str

@app.get("/")
def read_root():
    #enviar_resultado_bot()
    #socket.socket().connect(('telemetria-proyecto-clickhouse-1', 8123))
    print("Conexión establecida correctamente")
    #return {"message": "Hola, este es mi microservicio con FastAPI y ClickHouse"}
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='')

    # Ejemplo de consulta para verificar conexión
    result = client.query("SELECT * from  riego.FlujoAgua;")
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
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='riego')

    # Ejemplo de consulta para verificar conexión
    result = client.query("SELECT * from  riego.FlujoAgua;")
    print(result.result_rows)
    """
    client = clickhouse_connect.get_client(host='clickhouse', username='default', password='')
    result = client.query("SELECT 'Conexión Exitosa!'")
    """
    return {"message": result.result_rows}

# Endpoint para visualizar datos de consumo
@app.get("/consumo")
def get_consumo(ID_esp: int):
    try:
        query = f"SELECT Time_stam, Cantidad_agua FROM riego.FlujoAgua WHERE ID_esp = {ID_esp} ORDER BY Time_stam;"
        result = client.query(query).result_rows
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron datos para el ID especificado.")
        return {"consumo": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar el umbral
@app.put("/umbral")
def update_umbral(data: UmbralUpdate):
    try:
        # Verificar contraseña
        query_password = f"SELECT Contra FROM riego.Umbral WHERE ID_esp = {data.ID_esp};"
        result = client.query(query_password).result_rows
        if not result or result[0][0] != data.password:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta.")
        
        # Actualizar umbral
        update_query = f"ALTER TABLE riego.Umbral UPDATE Umbral = '{data.nuevo_umbral}' WHERE ID_esp = {data.ID_esp};"
        client.command(update_query)
        return {"message": "Umbral actualizado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar la contraseña
@app.put("/password")
def update_password(data: PasswordUpdate):
    try:
        # Actualizar contraseña
        update_query = f"ALTER TABLE riego.Umbral UPDATE Contra = '{data.nueva_password}' WHERE ID_esp = {data.ID_esp};"
        client.command(update_query)
        return {"message": "Contraseña actualizada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))