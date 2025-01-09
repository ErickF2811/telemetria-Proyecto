from flask import Flask, render_template, jsonify, request
import clickhouse_connect
from clickhouse_driver import Client 
app = Flask(__name__)

# Configurar ClickHouse
client = clickhouse_connect.get_client(host='clickhouse', username='default', password='', database='riego')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/consumo", methods=["GET"])
def consumo():
    try:
        result = client.query("SELECT Time_stam, Cantidad_agua FROM riego.FlujoAgua ORDER BY Time_stam;").result_rows
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/umbral", methods=["PUT"])
def actualizar_umbral():
    data = request.json
    nuevo_umbral = data.get("nuevo_umbral")
    password = data.get("password")

    try:
        # Verificar contraseña
        query_password = f"SELECT Contra FROM riego.Umbral WHERE ID_esp = 1;"  # Ajusta el ID según tu necesidad
        result = client.query(query_password).result_rows
        if not result or result[0][0] != password:
            return jsonify({"error": "Contraseña incorrecta."}), 401

        # Actualizar umbral
        update_query = f"ALTER TABLE riego.Umbral UPDATE Umbral = '{nuevo_umbral}' WHERE ID_esp = 1;"
        client.command(update_query)
        return jsonify({"message": "Umbral actualizado correctamente."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
