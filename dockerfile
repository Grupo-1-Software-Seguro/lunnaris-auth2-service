FROM python:3.11-alpine3.19

WORKDIR /app

COPY ./src /app/
COPY requirements.txt /app/requirements.txt

RUN rm .env

RUN pip install --no-cache -r requirements.txt

EXPOSE 5020

CMD ["gunicorn","-w","3","app:app","-b","0.0.0.0:5020"]

