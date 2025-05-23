# scripts/elastic_utils.py
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def search_similar_blogs(text, top_n=10):
    response = es.search(
        index="blogs",
        query={
            "more_like_this": {
                "fields": ["title", "content"],
                "like": text,
                "min_term_freq": 1,
                "max_query_terms": 12
            }
        },
        size=top_n
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]
