FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src src
COPY certs certs
COPY config.yml ./

CMD ["python3", "-u", "src/main.py"]