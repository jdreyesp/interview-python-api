# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /src/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

CMD ["gunicorn", "src.app.main:app"]