from elasticsearch import Elasticsearch
import pandas as pd

# Connect to ElasticSearch
es = Elasticsearch("http://localhost:9200")

# Load and clean data
df = pd.read_parquet("data/blogs.parquet")
df = df.dropna(subset=["title", "content"])

# Create index if not exists
if not es.indices.exists(index="blogs"):
    es.indices.create(
        index="blogs",
        mappings={
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "tags": {"type": "keyword"},
                "url": {"type": "keyword"}
            }
        }
    )
    print("🆕 Created 'blogs' index.")
else:
    print("ℹ️ Index 'blogs' already exists.")

# Index each blog
for i, row in df.iterrows():
    doc = {
        "title": row["title"],
        "content": row["content"],
        "tags": row.get("tags", ""),
        "url": row.get("url", "")
    }
    es.index(index="blogs", id=i, document=doc)

print(f"✅ Indexed {len(df)} blog posts.")
