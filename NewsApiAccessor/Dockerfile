
FROM python:3.11-slim


WORKDIR /app

COPY NewsApiAccessor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY NewsApiAccessor/ .

EXPOSE 50051


CMD ["python", "service.py"]