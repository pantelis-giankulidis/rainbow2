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
    key_count: int = Query(default=10, ge=1, le=1_000),
) -> dict[str, Any]:
    producer: AIOKafkaProducer = app.state.kafka_producer
    key_partitions: dict[str, set[int]] = {}
    try:
        for index in range(count):
            key = f"customer-{index % key_count}"
            event = {
                "event_id": f"experiment-1-{index:06d}",
                "event_type": "partitioning_demo",
                "entity_id": key,
                "sequence": index,
            }
            metadata = await producer.send_and_wait(
                TOPIC,
                json.dumps(event).encode("utf-8"),
                key=key.encode("utf-8"),
            )
            key_partitions.setdefault(key, set()).add(metadata.partition)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Unable to publish messages to Kafka") from exc

    partition_map = {
        key: sorted(partitions) for key, partitions in sorted(key_partitions.items())
    }
    return {
        "status": "sent",
        "count": count,
        "topic": TOPIC,
        "key_count": key_count,
        "key_partitions": partition_map,
        "same_key_same_partition": all(
            len(partitions) == 1 for partitions in partition_map.values()
        ),
    }
