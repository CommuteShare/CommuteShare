# syntax=docker/dockerfile:1

FROM python:3.10.11-slim-buster

WORKDIR /app1

COPY . /app1

#RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --no-cache-dir

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
