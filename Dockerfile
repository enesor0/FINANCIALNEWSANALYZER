FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY financial_news_analyzer/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY financial_news_analyzer /app/financial_news_analyzer

WORKDIR /app/financial_news_analyzer

EXPOSE 8080

CMD ["python", "nicegui_app.py"]
