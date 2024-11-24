
FROM python:3.11-slim


WORKDIR /app

COPY NewsDBAccessor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY NewsDBAccessor/ .

EXPOSE 50057

CMD ["python", "service.py"]