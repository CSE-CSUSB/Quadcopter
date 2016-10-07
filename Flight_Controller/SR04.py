'''
Author: Sean R Hamilton
QA: 
Date: 10/02/2016
References: SR04 Datasheet
Description: interface for the SR04 Ultrasonic Sensor.
	The sensor is used to detect the ground and other nearby objects
'''
import RPi.GPIO as GPIO #loads general purpose input/output library
import time #loads time library

GPIO.setmode(GPIO.BCM) #pin assignments mapped to values on board

class SR04:
	# constants
	__triggerPin = 0
	__echoPin = 0

	# initializes GPIO pins for sensor interface
	def __init__(self, trigger, echo):
		self.__triggerPin = trigger
		self.__echoPin = echo
		GPIO.setup(self.__triggerPin, GPIO.OUT)
		GPIO.setup(self.__echoPin, GPIO.IN)

	# measures and returns distance in cm
	def getDistance(self):
		#send 10us pulse through trigger to begin measurement
		GPIO.output(self.__triggerPin, False) #cutoff power to pin
		time.sleep(.005)
		GPIO.output(self.__triggerPin, True) #send pulse to begin measurement
		time.sleep(0.00001) #10us delay specified in datasheet
		GPIO.output(self.__triggerPin, False)

		#read echo duration
		while GPIO.input(self.__echoPin) == 0:
			pulse_start = time.time()
		while GPIO.input(self.__echoPin) == 1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start

		#calculate and return distance in cm
		distance = pulse_duration * pow(10, 6) #convert seconds to milliseconds
		distance /= 58 #calculate distance in centimeters

		return distance