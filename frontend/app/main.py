from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

MICROSERVICE_URL = "http://localhost:8010"  # Cambiar según el host y puerto de FastAPI

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/visualizar")
def visualizar():
    response = requests.get(f"{MICROSERVICE_URL}/visualizar")
    return jsonify(response.json())

@app.route("/umbral", methods=["PUT"])
def update_umbral():
    data = request.json
    response = requests.put(f"{MICROSERVICE_URL}/umbral", json=data)
    return jsonify(response.json())

@app.route("/password", methods=["PUT"])
def update_password():
    data = request.json
    response = requests.put(f"{MICROSERVICE_URL}/password", json=data)
    return jsonify(response.json())

@app.route("/consumo", methods=["GET"])
def get_consumo():
    ID_esp = request.args.get("ID_esp", default=1, type=int)
    fecha_inicio = request.args.get("fecha_inicio", type=str)
    fecha_fin = request.args.get("fecha_fin", type=str)

    # Validar fechas
    if not fecha_inicio or not fecha_fin:
        return jsonify({"error": "fecha_inicio y fecha_fin son requeridos"}), 400

    # Llamar al microservicio
    response = requests.get(
        f"{MICROSERVICE_URL}/consumo",
        params={"ID_esp": ID_esp, "fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin}
    )
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(debug=True)
