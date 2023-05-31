# syntax=docker/dockerfile:1

<<<<<<< HEAD
FROM python:3.10.11-slim-buster

WORKDIR /app1

COPY . /app1

#RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --no-cache-dir

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
=======
FROM 3.10.11-slim-buster

WORKDIR /app

COPY ../CommuteShare ./

RUN pip install --upgrade pip --no-cache-dir

RUN pip3 install -r /app/requirements.txt --no-cache-dir

EXPOSE 8000
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
>>>>>>> 4d5e6f507b985955032fdc122a282fcd95df8f36
