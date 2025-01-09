from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from clickhouse_driver import Client
from pydantic import BaseModel
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
@app.route('/consumo', methods=['GET'])
def get_consumo():
    # Obtener parámetros de la solicitud
    ID_esp = request.args.get('ID_esp', type=int)
    fecha_inicio = request.args.get('fecha_inicio', type=str)
    fecha_fin = request.args.get('fecha_fin', type=str)

    # Validar que los parámetros requeridos estén presentes
    if not ID_esp or not fecha_inicio or not fecha_fin:
        return jsonify({"error": "ID_esp, fecha_inicio y fecha_fin son requeridos"}), 400

    try:
        client = clickhouse_connect.get_client(host='clickhouse', username='default', password='')

        # Crear consulta SQL para filtrar por fechas
        query = text("""
            SELECT Time_stam, Cantidad_agua 
            FROM consumos 
            WHERE ID_esp = :ID_esp 
            AND DATE(Time_stam) BETWEEN :fecha_inicio AND :fecha_fin
            ORDER BY Time_stam
        """)
        client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='riego')
        result = client.query(query)
        rows = result.result_rows
        # Formatear los datos
        consumo_data = [{"Time_stam": row[0], "Cantidad_agua": row[1]} for row in rows]

        return jsonify({"ID_esp": ID_esp, "consumo": consumo_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al mostrar consumo: {str(e)}")

@app.get("/total_consumo")
def get_total_consumo():
    # Obtener parámetros de la solicitud
    ID_esp = request.args.get('ID_esp', type=int)
    fecha_inicio = request.args.get('fecha_inicio', type=str)
    fecha_fin = request.args.get('fecha_fin', type=str)
    # Validar que los parámetros requeridos estén presentes
    if not ID_esp or not fecha_inicio or not fecha_fin:
        return jsonify({"error": "ID_esp, fecha_inicio y fecha_fin son requeridos"}), 400


    try:
        # Conectar a ClickHouse
        client = get_client(host=CLICKHOUSE_HOST, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD, database=CLICKHOUSE_DB)

        # Crear la consulta SQL para calcular el total
        query = f"""
            SELECT SUM(Cantidad_agua) AS Total_Consumo
            FROM FlujoAgua
            WHERE ID_esp = {ID_esp}
              AND toDate(Time_stam) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
        """

        # Ejecutar la consulta
        result = client.query(query)
        total_consumo = result.result_rows[0][0] if result.result_rows else 0

        return {
            "ID_esp": ID_esp,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "total_consumo": total_consumo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular el total de consumo: {str(e)}")

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