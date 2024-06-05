FROM --platform=linux/amd64 python:3.8-slim

RUN apt-get update && apt-get install -y \
    buildah \
    libgpgme11 \
    libassuan0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
