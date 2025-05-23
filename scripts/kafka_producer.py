# scripts/kafka_producer.py

from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_summary_request(title, content):
    if not title or not content:
        print("❌ Missing title or content — not sending to Kafka.")
        return

    message = {"title": title.strip(), "content": content.strip()}
    print(f"📤 Sending to Kafka: {message['title'][:50]}...")
    producer.send('search_queries', value=message)
    producer.flush()
