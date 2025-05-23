import redis
r = redis.Redis(host="localhost", port=6379, db=0)
key = "NAIC Principles for the Use of Artificial Intelligence in the Insurance Industry"
summary = r.get(key)
print(summary.decode("utf-8") if summary else "❌ Not found")
