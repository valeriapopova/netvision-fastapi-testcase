FROM python:3.11-slim as builder

WORKDIR /app

COPY client.py .

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/client.py .

RUN pip install requests

ENV API_URL=http://server:8000

ENV PYTHONPATH /app

CMD ["python", "client.py"]