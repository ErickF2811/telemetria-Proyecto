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

if __name__ == "__main__":
    app.run(debug=True)
