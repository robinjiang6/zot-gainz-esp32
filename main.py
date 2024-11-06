from machine import I2C, Pin
from imu import MPU6050
from time import sleep_ms
from fusion import Fusion

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
while True:
    f.update_nomag(imu.accel.xyz, imu.gyro.xyz)
    print(pretty_print(f.heading), pretty_print(f.pitch), pretty_print(f.roll))
    #print(imu.accel.xyz)
    #print(imu.gyro.xyz)
    #print(imu.temperature)
    #print(imu.accel.z)
    sleep_ms(100)
