#!/usr/bin/python
import time
from BMP180 import BMP180
from MPU6050 import MPU6050
from Throttle import Throttle

i = BMP180()
m = MPU6050()
t1 = throttle('''motorNumber, motorPin, frequency, maxThrottle, minThrottle''')
t2 = throttle('''motorNumber, motorPin, frequency, maxThrottle, minThrottle''')
t3 = throttle('''motorNumber, motorPin, frequency, maxThrottle, minThrottle''')
t4 = throttle('''motorNumber, motorPin, frequency, maxThrottle, minThrottle''')

while True:
	print i.getAltitude()
	print m.getAngles()
	time.sleep(1)