# Usar una imagen oficial de Python 3.8 como base
FROM python:3.8-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo el archivo requirements.txt para aprovechar el cache de Docker
COPY fast_api2/requirements.txt .

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . .

# Asegurarse de que uvicorn esté instalado si no está en requirements.txt
RUN pip install --no-cache-dir uvicorn clickhouse_connect

# Exponer el puerto 8000
EXPOSE 8000

# Ejecutar FastAPI con Uvicorn como servidor ASGI
CMD ["uvicorn", "fast_api2.fast_2:app", "--host", "0.0.0.0", "--port", "8000"]
