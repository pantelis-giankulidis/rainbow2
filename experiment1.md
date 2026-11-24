# Experiment 1: Kafka keys and partition assignment

## Goal

Send JSON events to Kafka with a record key, then check that repeated copies of a key are stored in the same partition.

## Producer changes

`app.py`'s `POST /triggerMessages` endpoint generates events with a sequential `event_id`, an `event_type`, an `entity_id`, and a `sequence` number. It cycles through `customer-0` to `customer-(key_count - 1)`, so each key is reused across multiple events. The JSON event is the Kafka record value; the matching `customer-N` string is separately UTF-8 encoded and sent as the Kafka record key.

The producer awaits `send_and_wait` for each record. Kafka's returned record metadata includes the assigned partition. The endpoint collects partitions by key and returns them as `key_partitions`; `same_key_same_partition` is true only when each key in this request was acknowledged in one unique partition.

The endpoint defaults to 10,000 events and 10 keys. For the check below, it was called with 20 events and 4 keys, yielding five records per key.

## Procedure

The existing `demo-messages` topic initially had one partition. Since every record would then necessarily land in partition 0, it was expanded to six partitions for this experiment:

```sh
docker compose exec -T kafka-1 /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server kafka-1:29092 \
  --alter --topic demo-messages --partitions 6
```

Then the app containers were rebuilt and restarted to load the updated `app.py`:

```sh
docker compose up -d --build \
  message-app-1 message-app-2 message-app-3 message-app-4
```

The following request published the sample events:

```sh
curl --request POST \
  'http://localhost:8001/triggerMessages?count=20&key_count=4'
```

The response included the broker-acknowledged partition mapping:

```json
{
  "status": "sent",
  "count": 20,
  "topic": "demo-messages",
  "key_count": 4,
  "key_partitions": {
    "customer-0": [1],
    "customer-1": [3],
    "customer-2": [2],
    "customer-3": [4]
  },
  "same_key_same_partition": true
}
```

To verify the stored records independently, Kafka's console consumer was run with key and partition printing enabled:

```sh
docker compose exec -T kafka-1 /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server kafka-1:29092 \
  --topic demo-messages --from-beginning --max-messages 20 \
  --timeout-ms 10000 \
  --property print.key=true --property print.partition=true
```

The consumer showed all five `customer-0` records in partition 1, all five `customer-1` records in partition 3, all five `customer-2` records in partition 2, and all five `customer-3` records in partition 4. For example, records with sequences 0, 4, 8, 12, and 16 all had key `customer-0` and appeared in partition 1. The same-key check passed in both producer metadata and the consumed records, while different keys were distributed across four partitions.

## Conclusion

Within a topic with a fixed partition count and partitioning configuration, Kafka consistently assigned each repeated key to the same partition. This preserves ordering for records with that key within the partition. Increasing a topic's partition count can change key-to-partition assignments, so the consistency check assumes the topic's partition count remains fixed during the experiment.
