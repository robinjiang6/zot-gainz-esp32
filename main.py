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

i2c= I2C(scl=Pin(22), sda=Pin(21))
imu = MPU6050(i2c)
f = Fusion()
def pretty_print(data: float):
    add = ""
    if data >= 0:
        add = " "
    if abs(data) < 10:
        data = f"{data:.5f}"
    elif abs(data) < 100:
        data = f"{data:.4f}"
    else:
        data = f"{data:.3f}"
    return add + data

def test_IMU():
    while True:
        f.update_nomag(imu.accel.xyz, imu.gyro.xyz)
        print(pretty_print(f.heading), pretty_print(f.pitch), pretty_print(f.roll))
        sleep_ms(100)



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
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)


asyncio.run(main())
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
print(sta.config('mac'))

e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")
for i in range(100):
    e.send(peer, str(i)*20, True)
e.send(peer, b'end')

while True:
    f.update_nomag(imu.accel.xyz, imu.gyro.xyz)
    print(pretty_print(f.heading), pretty_print(f.pitch), pretty_print(f.roll))
    #print(imu.accel.xyz)
    #print(imu.gyro.xyz)
    #print(imu.temperature)
    #print(imu.accel.z)
    sleep_ms(100)
