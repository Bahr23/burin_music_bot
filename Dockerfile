FROM python:3.11.1-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y netcat git

COPY bot-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY app/config.py /app/config.py

ENTRYPOINT ["bash", "/app/docker-entrypoint.sh"]