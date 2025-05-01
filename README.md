# Real-Time Data Pipeline

A real-time data pipeline using Kafka, Spark Structured Streaming, and PostgreSQL.

## How it works
- Python producer simulates user activity and publishes to Kafka
- Spark consumes the messages, parses them, and writes to PostgreSQL
- PostgreSQL stores the cleaned data for BI tools

## Run Locally
```bash
cd infrastructure
docker-compose up
```

In another terminal:
```bash
cd data-producer
python producer.py
```

Start the Spark job:
```bash
cd spark-job
spark-submit main.py
```
