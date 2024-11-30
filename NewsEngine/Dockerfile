FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && apt-get clean


COPY NewsEngine/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY NewsEngine/ .

EXPOSE 5001

CMD ["python", "server.py"]
