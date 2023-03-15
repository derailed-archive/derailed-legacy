FROM python:3.11-alpine

WORKDIR /
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "gunicorn" ]