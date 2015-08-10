import random
import redis
import time

r = redis.Redis()

while True:
    r.publish('temperature', random.randint(0, 50))
    time.sleep(2)
