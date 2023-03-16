import machine
import time

led = machine.Pin(2, machine.Pin.OUT)
def flash_ever():
    while True:
        led.value(1)
        time.sleep(2)
        led.value(0)
        time.sleep(2)