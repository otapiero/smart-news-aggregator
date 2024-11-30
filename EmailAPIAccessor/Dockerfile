FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && apt-get clean

COPY EmailAPIAccessor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY EmailAPIAccessor/ .

EXPOSE 50055

CMD ["python", "app.py"]