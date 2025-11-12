FROM python:3.12-slim
ENV PYTHONDONTWRITECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY wait_for_db.py .

COPY config .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
