FROM --platform=linux/amd64 python:3.8-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
