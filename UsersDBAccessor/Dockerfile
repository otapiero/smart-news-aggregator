FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential && apt-get clean

WORKDIR /app

COPY UsersDBAccessor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY UsersDBAccessor/ .

EXPOSE 50057

CMD ["python", "server.py"]
