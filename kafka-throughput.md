# Local Kafka Throughput Benchmark

Run on 2026-11-24 against the Compose Kafka cluster.

## Setup

- Kafka image: `apache/kafka:4.1.1`, three brokers
- Benchmark topic: `throughput-benchmark`, 12 partitions, replication factor 3
- Producer: Kafka's `kafka-producer-perf-test.sh`, connected to `kafka-1:29092`
- Record size: 1,024 bytes; producer `acks=all`
- App instances and the other Compose services were running during the tests

The first sweep sent 100,000 records at each target rate. Follow-up runs sent 300,000 records per target; the final repeat sent 600,000 records at 150,000 records/s.

| Target (records/s) | Records per run | Measured (records/s) | Throughput (MB/s) |
|---:|---:|---:|---:|
| 5,000 | 100,000 | 4,995 | 4.88 |
| 10,000 | 100,000 | 9,976 | 9.74 |
| 25,000 | 100,000 | 24,888 | 24.30 |
| 50,000 | 100,000 | 46,838 | 45.74 |
| 100,000 | 100,000 | 64,725 | 63.21 |
| 200,000 | 100,000 | 49,875 | 48.71 |
| 50,000 | 300,000 | 49,636 | 48.47 |
| 75,000 | 300,000 | 74,074 | 72.34 |
| 100,000 | 300,000 | 84,698 | 82.71 |
| 150,000 | 300,000 | **104,421** | **101.97** |
| 200,000 | 300,000 | 99,404 | 97.07 |
| 300,000 | 300,000 | 71,770 | 70.09 |
| 500,000 | 300,000 | 94,221 | 92.01 |
| 1,000,000 | 300,000 | 88,235 | 86.17 |
| 150,000 (repeat) | 600,000 | 82,226 | 80.30 |

## Result

The highest observed run was **104,421 records/s (about 102 MB/s)** at a target of 150,000 records/s. Repeating that target with twice as many records yielded 82,226 records/s. Higher target rates did not produce higher throughput consistently, so treat 104k records/s as the best observed result for this run, not a stable or hardware-independent broker limit. Producer latency also rose sharply at the higher targets.
