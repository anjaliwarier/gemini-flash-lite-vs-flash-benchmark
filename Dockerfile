FROM python:3.11-slim

WORKDIR /app

COPY server.py .
COPY benchmark_10k_ocr.py .
COPY index.html .
COPY sec_10k_sample.txt .

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD ["python", "server.py"]
