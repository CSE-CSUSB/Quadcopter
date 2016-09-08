#!/usr/bin/python

'''
Author:	Sean R Hamilton
QA:	
Date:	08/24/2016
References: N/A
Description: manages motor output based on sensor input and user destination settings.
'''

import time
from BMP180 import BMP180
from MPU6050 import MPU6050
from Throttle import Throttle
from Controller import Controller

# Sensor object initialization
a = BMP180()
rp = MPU6050()
initialAltitude = a.getAltitude()
(initialRoll, initialPitch) = rp.getAngles()
initialYaw = 0 # currently unused

# Motor object initialization
frequency = 55
maxThrottle = 10
minThrottle = 5

# motorNumber, motorPin, frequency, maxThrottle, minThrottle
t1 = Throttle(1, 12, frequency, maxThrottle, minThrottle)
t2 = Throttle(2, 13, frequency, maxThrottle, minThrottle)
t3 = Throttle(3, 22, frequency, maxThrottle, minThrottle)
t4 = Throttle(4, 18, frequency, maxThrottle, minThrottle)

# Controller object initialization
# roll controller variables
rSetPoint = 0
rIntegralThreshold = 90
rKP = 0.9
rKI = 0
rKD = 0.1

# pitch controller variables
pSetPoint = 0
pIntegralThreshold = 90
pKP = 0.9
pKI = 0
pKD = 0.1

# altitude controller variables
aSetPoint = 0.05
aIntegralThreshold = 10
aKP = 10
aKI = 0
aKD = 1

# yaw controller variables, currently unused
ySetPoint = 0
yIntegralThreshold = 100
yKP = 1
yKI = 1
yKD = 1

# initialSensorValue, maxThrottle, minThrottle, setPoint, integralThreshold, kP, kI, kD
cRoll = Controller(initialRoll, maxThrottle, minThrottle, rSetPoint, rIntegralThreshold, rKP, rKI, rKD)
cPitch = Controller(initialPitch, maxThrottle, minThrottle, pSetPoint, pIntegralThreshold, pKP, pKI, pKD)
cAltitude = Controller(initialAltitude, maxThrottle, minThrottle, aSetPoint, aIntegralThreshold, aKP, aKI, aKD)
#cYaw = Controller(initialYaw, maxThrottle, minThrottle, ySetPoint, yIntegralThreshold, yKP, yKI, yKD)

time.sleep(5)

while True:
	(xAngle, yAngle) = rp.getAngles()
	
	aVal = cAltitude.getThrottlePercent(a.getAltitude());
	rVal = cRoll.getThrottlePercent(xAngle);
	pVal = cPitch.getThrottlePercent(yAngle);
	yVal = 0 #currently unused
	
	print aVal,	rVal,	pVal
	
	#t1.setThrottle(7, 0, 0, 0)
	#t2.setThrottle(7, 0, 0, 0)
	#t3.setThrottle(7, 0, 0, 0)
	#t4.setThrottle(7, 0, 0, 0)
	
	t1.setThrottle(aVal, rVal, pVal, yVal)
	t2.setThrottle(aVal, rVal, pVal, yVal)
	t3.setThrottle(aVal, rVal, pVal, yVal)
	t4.setThrottle(aVal, rVal, pVal, yVal)