FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./backend/requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./backend /app/

RUN python3 -m pytest

EXPOSE 8000
