FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ /app
COPY templates/ /app/templates
COPY static/ /app/static
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
