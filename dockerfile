FROM python:3.11-alpine3.19

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache -r requirements.txt

COPY ./src /app/

EXPOSE 5000

CMD ["gunicorn","-w","3","app:app","-b","0.0.0.0:5000"]

