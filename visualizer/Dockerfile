FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    curl \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./visualizer/
RUN pip install --no-cache-dir -r ./visualizer/requirements.txt

COPY . ./visualizer
EXPOSE 8000

RUN adduser --disabled-password simple
USER simple

ENTRYPOINT ["uvicorn", "visualizer.main:app", "--host", "0.0.0.0", "--port", "8000"]