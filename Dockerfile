FROM python:3.14-alpine AS base
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip && \
    apk upgrade --no-cache

FROM base
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "url.py"]
