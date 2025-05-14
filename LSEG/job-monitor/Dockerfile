FROM python:3.10-slim

WORKDIR /app

RUN apt-get -o Acquire::AllowInsecureRepositories=true update && \
    apt-get -o Acquire::AllowInsecureRepositories=true install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

CMD ["python", "src/jobMonitor.py"]
