import random
import redis
import time

r = redis.Redis()

while True:
    temperature = random.randint(0, 50)
    r.publish('temperature', temperature)
    r.set('temperature', temperature)
    time.sleep(2)
