FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app/backend

CMD ["bash", "-lc", "PYTHONPATH=/app/backend python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"]
