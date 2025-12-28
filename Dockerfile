# Базовый образ Python
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Экспонируем порт для health check
EXPOSE 8080

# Стартуем контейнер
CMD ["python", "aiogram_run.py"]
