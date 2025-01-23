FROM python:3.9-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app

WORKDIR /app

CMD ["python" "main.py"]
