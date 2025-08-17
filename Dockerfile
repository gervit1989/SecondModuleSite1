#Python Version
FROM python:3.13-slim

# Рабочая директория
WORKDIR /app

# Копируем необходимое
COPY requirements.txt .

#Развертываем
RUN pip install --no-cache-dir -r requirements.txt

#Копируем все
COPY . .

#Выполняем команду
CMD ["python", "app.py"]