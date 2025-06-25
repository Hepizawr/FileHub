FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev build-essential

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000
CMD ["flask", "run"]
