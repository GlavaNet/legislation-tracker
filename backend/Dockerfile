FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -U appuser && \
    chown -R appuser:appuser /app && \
    mkdir -p /var/run/celery && \
    chown -R appuser:appuser /var/run/celery && \
    chmod -R 777 /var/run/celery

USER appuser

# Create and activate virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

COPY --chown=appuser:appuser requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=appuser:appuser . .

# Create directories needed for Celery
RUN mkdir -p /app/celery/{beat,worker} && \
    chmod -R 777 /app/celery

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
