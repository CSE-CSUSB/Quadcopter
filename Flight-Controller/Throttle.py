'''
Author:	Samuel Montes
		Sean R Hamilton
QA:	
Date: 05/27/2016
References: raspberry pi GPIO library
Description: manages motor output based on sensor values
'''

import RPi.GPIO as GPIO	# loads General Purpose Input/Output library

GPIO.setmode(GPIO.BOARD)	# pins assignments mapped to printed values on board

class Throttle:
	# constants
	__motor1 = 1
	__motor2 = 2
	__motor3 = 3
	#__motor4 = 4#commented out because motor4 is the default case in setThrottle
	
	# storage variables
	__motorNumber = 0	# designates physical motor number (1-4)
	__motorPin = 0	# GPIO pin controlling the motor
	__maxThrottle = 0	# maximum duty cycle
	__minThrottle = 0	# minimum duty cycle
	__throttle = 0	# duty cycle
	__frequency = 0 # pwm frequency in Hz
	
	# initializes storage variables and PWM object for throttle control
	def __init__(self, motorNumber, motorPin, frequency, maxThrottle, minThrottle):
		self.__motorNumber = motorNumber
		self.__motorPin = motorPin
		self.__frequency = frequency
		self.__maxThrottle = maxThrottle
		self.__minThrottle = minThrottle
		GPIO.setup(self.__motorPin, GPIO.OUT) # defines motor pin as an output
		self.__throttle = GPIO.PWM(self.__motorPin, self.__frequency) #PWM object. GPIO.PWM(pin number, frequency in Hz)
		self.__throttle.start(self.__minThrottle) #Sets initial duty cycle to minimum to arm motor
	
	# assignes a new throttle output to motors
	def setThrottle(self, Altitude, Roll, Pitch, Yaw):
		if (self.__motorNumber == self.__motor1):
			newThrottle = Altitude - Pitch + Yaw
		elif (self.__motorNumber == self.__motor2):
			newThrottle = Altitude - Roll + Yaw
		elif (self.__motorNumber == self.__motor3):
			newThrottle = Altitude + Pitch + Yaw
		else:	# motor 4
			newThrottle = Altitude + Roll + Yaw
			
		if (newThrottle > self.__maxThrottle):
			newThrottle = self.__maxThrottle
		elif (newThrottle < self.__minThrottle):
			newThrottle = self.__minThrottle
			
		self.__throttle.ChangeDutyCycle(newThrottle)	# assign new duty cycle
		return newThrottle
	
	# stops motor and releases GPIO control
	def throttleEnd(self):
		self.__throttle.stop() #Stops all signals going to the motor
		GPIO.cleanup() #erases pin setup