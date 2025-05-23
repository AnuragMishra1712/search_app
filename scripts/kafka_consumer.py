# scripts/kafka_consumer.py

from kafka import KafkaConsumer
import redis
import json
import subprocess

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Set up Kafka consumer
consumer = KafkaConsumer(
    'search_queries',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='summary-consumer-group'
)

print("🧠 Kafka consumer is listening for summary requests...")

# Function to call Ollama to generate summary
def generate_summary_ollama_mistral(text):
    prompt = f"""Summarize the following blog:
{text}

Summary:"""
    result = subprocess.run(
        ["ollama", "run", "llama3.2"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        return result.stdout.decode("utf-8")
    else:
        print(f"❌ Error summarizing: {result.stderr.decode('utf-8')}")
        return None

for message in consumer:
    data = message.value
    title = data.get("title", "Untitled")
    content = data.get("content", "")
    print(f"\n📥 Received blog: {title}")

    summary = generate_summary_ollama_mistral(content)
    if summary:
        redis_key = title.strip().lower().replace(" ", "_")
        redis_client.set(redis_key, summary)
        print(f"✅ Summary stored in Redis for: {title} [key: {redis_key}]")
    else:
        print(f"❌ Failed to summarize blog: {title}")