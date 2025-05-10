# Dockerfile

# 1) Базовый образ с Python 3.11
FROM python:3.11-slim

# 2) Рабочая директория
WORKDIR /app

# 3) Копируем только список зависимостей и ставим их
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 4) Копируем весь код приложения
COPY . .

# 5) Прогоняем миграции
RUN alembic upgrade head

# 6) Открываем порт
EXPOSE 8000

# 7) Команда старта
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
