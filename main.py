from machine import I2C, Pin
from resources.imu import MPU6050
from time import sleep_ms
from resources.fusion import Fusion
from resources.data import Reading

from micropython import const

import asyncio
import resources.aioble as aioble
import bluetooth

import random
import struct

import network
import espnow

# replace this with the mac address of the receiver
MAIN_ESP_MAC = b'\xa0\xb7e"\xff\xe0'

i2c= I2C(scl=Pin(22), sda=Pin(21))
imu = MPU6050(i2c)
f = Fusion()

# # org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)
print("here")
_BODY_POS_UUID = bluetooth.UUID('0fb69140d0074a11b33198fa2666fb65')
_BODY_POS_THIGH_UUID = bluetooth.UUID('57ad3f96cfb843a1af3e17400f5a6cd3')
print('here2')

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

# body_pos_service = aioble.Service(_BODY_POS_UUID)
# thigh_characteristic = aioble.Characteristic(
#     body_pos_service, _BODY_POS_THIGH_UUID, read=True, notify=True
# )
# aioble.register_services(body_pos_service)

# Register GATT server.
temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic(
    temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
)
aioble.register_services(temp_service)


# Helper to encode the temperature characteristic encoding (sint16, hundredths of a degree).
def _encode_temperature(temp_deg_c):
    return struct.pack("<h", int(temp_deg_c * 100))

def _encode_roll(roll):
    return struct.pack(">h", int(roll))


# This would be periodically polling a hardware sensor.
async def sensor_task():
    t = 24.5
    while True:
        temp_characteristic.write(_encode_temperature(t), send_update=True)
        t += random.uniform(-0.5, 0.5)
        await asyncio.sleep_ms(1000)
async def imu_task():
    print("starting imu_task")
    while True:
        f.update_nomag(imu.accel.xyz, imu.gyro.xyz)
        thigh_characteristic.write(_encode_roll(f.roll), send_update=True)
        print(int(f.roll))
        print(_encode_roll(f.roll))
        await asyncio.sleep_ms(500)



# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="zotgainz",
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
        ) as connection:
            print("Connection from", connection.device)
            await connection.disconnected(timeout_ms=None)


# ESPNOW, communication between ESP32 devices:
# https://docs.micropython.org/en/latest/library/espnow.html
# A WLAN interface must be active to send()/recv()

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)
def espnow_add_peer(esp_now, mac: bytes):
    esp_now.add_peer(mac)
    print(esp_now.get_peers())
    print(esp_now.get_peer(mac))

if sta.config('mac') != MAIN_ESP_MAC:
    # not receiver
    espnow_add_peer(e, MAIN_ESP_MAC)
    e.send(MAIN_ESP_MAC, "Starting...")
data = Reading(name="leg_sensor_1")

async def esp_send_task():
    while True:
        # collect rolling average every 10ms

        # change range from 10 to 1 for more frequent data send
        for _ in range(10):
            f.update_nomag(imu.accel.xyz, imu.gyro.xyz)
            data.add_reading(f.heading, f.pitch, f.roll)
            await asyncio.sleep_ms(10)
        e.send(MAIN_ESP_MAC, data.prepare_reading(), True)

def receive_data():
    while True:
        host, msg = e.recv()
        if msg:             # msg == None if timeout in recv()
            print(host, msg)
            if msg == b'end':
                break

if sta.config('mac') == MAIN_ESP_MAC:
    print(sta.config('mac')) # get current mac address
    receive_data()

# async def peripheral_task():
#     while True:
#         async with await aioble.advertise(
#             _ADV_INTERVAL_MS,
#             name="zotgainz",
#             services=[_BODY_POS_UUID],
#         ) as connection:
#             print("Connection from", connection.device)
#             await connection.disconnected(timeout_ms=None)


# Run both tasks.
async def main():
    #t1 = asyncio.create_task(sensor_task())
    #t2 = asyncio.create_task(peripheral_task())
    t3 = asyncio.create_task(esp_send_task())
    await asyncio.gather(t3)


asyncio.run(main())
