import json
import os
from contextlib import asynccontextmanager
from typing import Any

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, HTTPException, Query

TOPIC = os.getenv("KAFKA_TOPIC", "demo-messages")
BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "kafka-1:29092,kafka-2:29092,kafka-3:29092"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    await producer.start()
    app.state.kafka_producer = producer
    try:
        yield
    finally:
        await producer.stop()


app = FastAPI(title="Kafka Message Demo", lifespan=lifespan)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/triggerMessages")
async def trigger_messages(
    count: int = Query(default=10_000, ge=1, le=100_000),
) -> dict[str, Any]:
    producer: AIOKafkaProducer = app.state.kafka_producer
    try:
        for index in range(count):
            # Replace this placeholder payload when the final message schema is defined.
            message = {"demo_message": {"sequence": index}}
            await producer.send_and_wait(TOPIC, json.dumps(message).encode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Unable to publish messages to Kafka") from exc

    return {"status": "sent", "count": count, "topic": TOPIC}
