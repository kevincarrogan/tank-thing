import random
import redis
import time

r = redis.Redis()

temperature = random.randint(0, 50)

while True:
    temperature = random.randint(temperature - 2, temperature + 2)
    temperature = max(0, temperature)
    temperature = min(50, temperature)
    r.publish('temperature', temperature)
    r.set('temperature', temperature)
    time.sleep(0.17)
