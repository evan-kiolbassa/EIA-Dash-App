FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && apt-get install -y mingw-w64
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:server", "-b", "0.0.0.0:8050"]