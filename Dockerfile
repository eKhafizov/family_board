# Dockerfile

# 1) Базовый образ
FROM python:3.11-slim

# 2) Рабочая директория
WORKDIR /app

# 3) Сначала копируем только список зависимостей
COPY requirements.txt .

# 4) Устанавливаем их
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 5) Копируем весь остальной код
COPY . .

# 6) Открываем порт
EXPOSE 8000

# 7) На этапе запуска: сначала миграции, потом Uvicorn
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
