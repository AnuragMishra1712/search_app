from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def recommend_top_blogs(query, top_n=10):
    response = es.search(
        index="blogs",
        size=top_n,
        query={
            "multi_match": {
                "query": query,
                "fields": ["title^3", "content", "tags"]
            }
        }
    )
    return [
        {
            "title": hit["_source"].get("title", ""),
            "content": hit["_source"].get("content", ""),
            "tags": hit["_source"].get("tags", ""),
            "url": hit["_source"].get("url", "")
        }
        for hit in response["hits"]["hits"]
    ]
