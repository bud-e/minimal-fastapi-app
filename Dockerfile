FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/minimal-fastapi-app/

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y vim && \
    apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl poppler-utils && \
    pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

RUN bash -c 'ls'

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
