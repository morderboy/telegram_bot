# Установка Python
FROM python:3.9.13 as base
LABEL maintainer="ChatGPT, DALL-E <telegram.bot>"

# Инициализация проекта
WORKDIR /telegram_bot

ENV PYTHONDONTWRITEBYTECODE 0
ENV PYTHONUNBUFFERED 1

# Копирование файла requirements.txt в образ
COPY requirements.txt /telegram_bot/requirements.txt

# Установка зависимостей из файла requirements.txt 
RUN pip install -r requirements.txt

COPY . /telegram_bot/

# Команда запуска приложения
CMD [ "python3", "main.py" ]