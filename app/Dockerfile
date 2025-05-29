FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip -r requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh
RUN ls
ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "PaymentSystem.wsgi:application", "--bind", "0.0.0.0:8000"]