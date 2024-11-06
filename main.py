from machine import I2C, Pin
from resources.imu import MPU6050
from time import sleep_ms
from resources.fusion import Fusion
from resources.data import Reading

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

def test_LED():
    led = Pin(2, Pin.OUT)
    while True:
        print(".")
        led.on()
        sleep_ms(500)
        led.off()
        sleep_ms(500)
test_LED()

while True:
    f.update_nomag(imu.accel.xyz, imu.gyro.xyz)
    print(pretty_print(f.heading), pretty_print(f.pitch), pretty_print(f.roll))
    #print(imu.accel.xyz)
    #print(imu.gyro.xyz)
    #print(imu.temperature)
    #print(imu.accel.z)
    sleep_ms(100)
