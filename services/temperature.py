import math
import redis
import time

from RPi import GPIO

r = redis.Redis()

a_pin = 18
b_pin = 23

fiddle_factor = 0.9

def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.01)

def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    GPIO.output(a_pin, True)
    t1 = time.time()
    while not GPIO.input(b_pin):
        pass
    t2 = time.time()
    return (t2 - t1) * 1000000 # microseconds

def analog_read():
    discharge()
    return charge_time()

def read_resistance():
    n = 100
    total = 0;
    for i in range(1, n):
        total = total + analog_read()
    reading = total / float(n)
    # 6.05 was measured as the factor needed to convert reading to resistance (its linear)
    # with the sensor replaced by short circuit (i.e. using the timing for the 1k fixed resistor only)
    # 939 is the measured resistance of my supposed 1k resistor
    resistance = reading * 6.05 - 939
    return resistance

def temp_from_r(R):
    B = 3800.0          # The thermistor constant - change this for a different thermistor
    R0 = 1000.0         # The resistance of the thermistor at 25C -change for different thermistor
    t0 = 273.15         # 0 deg C in K
    t25 = t0 + 25.0     # 25 deg C in K
    # Steinhart-Hart equation - Google it
    inv_T = 1/t25 + 1/B * math.log(R/R0)
    T = 1/inv_T - t0
    return T * fiddle_factor

try:
    while True:
        temperature = int(temp_from_r(read_resistance()))
        r.publish('temperature', temperature)
        r.set('temperature', temperature)
        time.sleep(0.17)
finally:
    GPIO.cleanup()



