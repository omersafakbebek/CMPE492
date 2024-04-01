FROM --platform=linux/amd64 python:3.8-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3000

ENV IN_CLUSTER true

CMD ["python", "main.py"]
