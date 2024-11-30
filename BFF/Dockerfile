FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && apt-get clean

COPY BFF/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY BFF/ .

EXPOSE 5003

CMD ["python", "app.py"]