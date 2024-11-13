FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y procps postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./fetcher/
RUN pip install --no-cache-dir -r ./fetcher/requirements.txt

COPY . ./fetcher

RUN adduser --disabled-password simple \
    && chmod +x fetcher/healthcheck.sh
USER simple

ENTRYPOINT ["python", "fetcher/main.py"]