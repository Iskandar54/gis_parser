FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y cron && \
    pip install python-crontab && \
    apt-get clean

ENV TZ=Europe/Moscow

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY db_manager.py .
COPY logger_config.py .
COPY main.py .
COPY parser.py .
COPY tg_sendmess.py .
COPY utils.py .
COPY init_cron.py .
COPY entrypoint.sh .

RUN mkdir -p /app/logs && \
    touch /app/logs/cron.log && \
    chmod 666 /app/logs/cron.log

RUN chmod +x entrypoint.sh
CMD ["sh", "/app/entrypoint.sh"]