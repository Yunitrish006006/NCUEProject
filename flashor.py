from machine import Pin
import time
p0 = Pin(2, Pin.OUT)
while True:
    p0.value(0)
    time.sleep(2)
    p0.value(1)
