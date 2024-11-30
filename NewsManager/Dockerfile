FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential && apt-get clean

WORKDIR /app

COPY NewsManager/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY NewsManager/ .

EXPOSE 50053

CMD ["python", "server.py"]
