FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./fetcher/
RUN pip install --no-cache-dir -r ./fetcher/requirements.txt

COPY . ./fetcher

RUN adduser --disabled-password simple
USER simple

CMD ["python", "fetcher/main.py"]