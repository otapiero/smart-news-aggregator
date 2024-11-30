FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && apt-get clean


COPY LLMSummarizationAPIAccessor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY LLMSummarizationAPIAccessor/ .

EXPOSE 50054

CMD ["python", "service.py"]
