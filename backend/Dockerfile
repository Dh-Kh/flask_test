FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

RUN useradd -ms /bin/bash myuser

WORKDIR /backend

COPY requirements.txt /backend

RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend

EXPOSE 8000

ENV PATH="/home/myuser/.local/bin:${PATH}"