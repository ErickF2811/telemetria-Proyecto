FROM python:3.8-slim
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir requests Flask clickhouse-driver==0.2.0 clickhouse_connect
COPY app/ /app
COPY templates/ /app/templates
COPY static/ /app/static
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
