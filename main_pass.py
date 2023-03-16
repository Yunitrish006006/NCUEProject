import machine
import network
import urequests
import ujson
import logging
from machine import Pin
from machine import PWM
from time import sleep_ms

# Wi-Fi credentials
WIFI_SSID = '603'
WIFI_PASSWORD = '0937565253'

# IR receiver pin
IR_PIN = 34

# IR codes for the remote control buttons
IR_CODES = {
    'power': [0x00, 0xFD, 0x02],
    'volume_up': [0x00, 0xFD, 0x48],
    'volume_down': [0x00, 0xFD, 0x08],
    'mute': [0x00, 0xFD, 0x18]
}

# Connect to Wi-Fi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        logging.info('Connecting to Wi-Fi...')
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    logging.info('Wi-Fi connected.')
    logging.info(sta_if.ifconfig())

# Send IR signal


def send_ir_signal(code):
    pwm = PWM(Pin(18), freq=38000, duty_u16=512)
    for i in range(2):
        pwm.duty_u16(512)
        sleep_ms(9)
        pwm.duty_u16(0)
        sleep_ms(4)
    for i in range(len(code)):
        for j in range(8):
            if code[i] & (1 << j):
                pwm.duty_u16(512)
                sleep_ms(1)
                pwm.duty_u16(0)
                sleep_ms(1)
            else:
                pwm.duty_u16(512)
                sleep_ms(1)
                pwm.duty_u16(0)
                sleep_ms(1)
        sleep_ms(14)
# Receive IR signal


def receive_ir_signal(ir_pin):
    ir = machine.Pin(ir_pin, machine.Pin.IN, machine.Pin.PULL_UP)
    while ir.value():
        pass
    while not ir.value():
        pass
    start = machine.ticks_us()
    while ir.value():
        pass
    duration = machine.ticks_diff(machine.ticks_us(), start)
    if duration > 1000:
        return None
    bits = []
    while len(bits) < 32:
        while ir.value():
            pass
        while not ir.value():
            pass
        bit_duration = machine.ticks_diff(machine.ticks_us(), start)
        if bit_duration > 1000:
            return None
        bits.append(1 if bit_duration > 400 else 0)
        start = machine.ticks_us()
    if bits[0] == 0 and bits[1] == 1:
        return bits[8:24]
