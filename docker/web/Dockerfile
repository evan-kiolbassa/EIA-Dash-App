FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && apt-get install -y mingw-w64 && \
    apt-get install -y sudo && sudo apt-get install -y python3-dev

RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8050"]