# syntax=docker/dockerfile:1

FROM 3.10.11-slim-buster

WORKDIR /app

COPY ../CommuteShare ./

RUN pip install --upgrade pip --no-cache-dir

RUN pip3 install -r /app/requirements.txt --no-cache-dir


CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]