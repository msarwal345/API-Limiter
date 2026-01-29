import redis

try:
    r = redis.Redis(
        host="localhost",
        port=6789,
    )
    result = r.ping()

    print("Redis connected:", result)

except redis.ConnectionError as e:
    print("Redis connection failed:", e)
