FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# FastAPI через uvicorn, порт 8080
CMD ["uvicorn", "aiogram_run:app", "--host", "0.0.0.0", "--port", "8080"]
