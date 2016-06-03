#!/usr/bin/python
import time
from BMP180 import BMP180
from MPU6050 import MPU6050

i = BMP180()
m = MPU6050()

while True:
	print i.getAltitude()
	print m.getAngles()
	time.sleep(1)