import random
import redis
import time

from w1thermsensor import W1ThermSensor

r = redis.Redis()

sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    r.publish('temperature', temperature)
    r.set('temperature', temperature)
    time.sleep(0.17)
