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
initialRoll, initialPitch = rp.getAngles()
initialYaw = 0 # currently unused

# Motor object initialization
frequency = 55
maxThrottle = 10
minThrottle = 5

# motorNumber, motorPin, frequency, maxThrottle, minThrottle
t1 = Throttle(1, 12, frequency, maxThrottle, minThrottle)
t2 = Throttle(2, 13, frequency, maxThrottle, minThrottle)
t3 = Throttle(3, 16, frequency, maxThrottle, minThrottle)
t4 = Throttle(4, 18, frequency, maxThrottle, minThrottle)

# Controller object initialization
# roll controller variables
rSetPoint = 0
rIntegralThreshold = 100
rKP = 1
rKI = 1
rKD = 1

# pitch controller variables
pSetPoint = 0
pIntegralThreshold = 100
pKP = 1
pKI = 1
pKD = 1

# altitude controller variables
aSetPoint = 1
aIntegralThreshold = 100
aKP = 1
aKI = 1
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

while True:
	(xAngle, yAngle) = rp.getAngles()
	aVal = cAltitude.getThrottlePercent(a.getAltitude())
	rVal = cRoll.getThrottlePercent(xAngle)
	pVal = cPitch.getThrottlePercent(yAngle)
	yVal = 0 #currently unused
	
	t1.setThrottle(aVal, rVal, pVal, yVal)
	t2.setThrottle(aVal, rVal, pVal, yVal)
	t3.setThrottle(aVal, rVal, pVal, yVal)
	t4.setThrottle(aVal, rVal, pVal, yVal)