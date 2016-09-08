'''
Author: Sean R Hamilton
Date: 05/06/2016
References: InvenSense MPU6050 Datasheet and Register Map, Andrew Birkett's Raspberry Pi Blog
Description: Reads gyro and accelerometer data from the MPU6050 and calculates the orientation of the quadcopter.
Assumes the code is being run from the raspi B rev 1
'''

import smbus
import math
import time

class MPU6050:
	# MPU6050 i2c address
	__ADDR = 0x68
	
	# initialize smbus for i2c interface
	__bus = smbus.SMBus(1)
	
	# Power management register addresses
	__POWER_MGMT_1 = 0x6b
	__POWER_MGMT_2 = 0x6c
	
	# Gyro/Accelerometer scale values from register map
	__GYRO_SCALE = 131.0
	__ACCEL_SCALE = 16384.0
	
	# Gyro/Accel register addresses
	__GYRO_DATA = 0x43
	__ACCEL_DATA = 0x3B
	
	# Gyro/Accelerometer calculation storage
	__gyroX = 0
	__gyroY = 0
	__accelX = 0
	__accelY = 0
	__accelZ = 0
	__gyroOffsetX = 0
	__gyroOffsetY = 0
	
	# Storage for previous x and y angles
	__prevX = 0
	__prevY = 0
	
	# Gyro filter constants
	__k = 0.98
	__k1 = 1 - __k
	__timeDiff = 0.01
	
	# Initialize the sensor
	def __init__(self):
		self.__bus.write_byte_data(self.__ADDR, self.__POWER_MGMT_1, 0)
		time.sleep(0.005)
		
		# initial read of gyro/accel to establish base values
		self.__readRawGyroAccel()	# load most recent data to storage var
		
		self.__gyroOffsetX = self.__gyroX
		self.__gyroOffsetY = self.__gyroY
		gyroScaledX = self.__gyroX * self.__timeDiff
		gyroScaledY = self.__gyroY * self.__timeDiff
		rotationX = self.__getXRotation()
		rotationY = self.__getYRotation()
		
		# calculate initial x and y angles for filter algorithm
		#self.__prevX = self.__k * (rotationX + gyroScaledX) + (self.__k1 * rotationX)
		#self.__prevY = self.__k * (rotationY + gyroScaledY) + (self.__k1 * rotationY)
	
	# Calculate two's complement
	def __twosComp(self, val):
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else:
			return val
	
	# Calculate hypotenuse (distance) of xyz values
	def __dist(self, a, b):
		return math.sqrt((a * a) + (b * b))
	
	# Calculate y-axis rotation from accelerometer readings
	def __getYRotation(self):
		radians = math.atan2(self.__accelX, self.__dist(self.__accelY, self.__accelZ))
		return -math.degrees(radians)
		
	# Calculate x-axis rotation from accelerometer readings
	def __getXRotation(self):
		radians = math.atan2(self.__accelY, self.__dist(self.__accelX, self.__accelZ))
		return math.degrees(radians)
	
	# Read raw gyro and accelerometer data into storage variable
	def __readRawGyroAccel(self):
		rawGyroData = self.__bus.read_i2c_block_data(self.__ADDR, self.__GYRO_DATA, 6)
		rawAccelData = self.__bus.read_i2c_block_data(self.__ADDR, self.__ACCEL_DATA, 6)
		
		self.__gyroX = self.__twosComp((rawGyroData[0] << 8) + rawGyroData[1]) / self.__GYRO_SCALE
		self.__gyroY = self.__twosComp((rawGyroData[2] << 8) + rawGyroData[3]) / self.__GYRO_SCALE
		self.__accelX = self.__twosComp((rawAccelData[0] << 8) + rawAccelData[1]) / self.__ACCEL_SCALE
		self.__accelY = self.__twosComp((rawAccelData[2] << 8) + rawAccelData[3]) / self.__ACCEL_SCALE
		self.__accelZ = self.__twosComp((rawAccelData[4] << 8) + rawAccelData[5]) / self.__ACCEL_SCALE
	
	# Calculate and return angle along x-axis
	def getAngleX(self):
		(angleX, unused) = getAngles()		
		return angleX
		
	# Calculate and return angle along y-axis
	def getAngleY(self):
		(unused, angleY) = getAngles()		
		return angleY
		
	# Calculate and return angles along x-axis and y-axis
	# During implementation, it is best to call this function once per 
	# loop iteration, then send its outputs to the roll and pitch 
	# Controllers for processing
	def getAngles(self):
		# initial read of gyro/accel to establish base values
		self.__readRawGyroAccel()	# load most recent data to storage var
		
		gyroDeltaX = self.__gyroX - self.__gyroOffsetX
		gyroDeltaY = self.__gyroY - self.__gyroOffsetY
		gyroScaledX = gyroDeltaX * self.__timeDiff
		gyroScaledY = gyroDeltaY * self.__timeDiff
		rotationX = self.__getXRotation()
		rotationY = self.__getYRotation()
		
		# calculate x and y angle outputs
		angleX = self.__k * (self.__getXRotation() + gyroScaledX) + (self.__k1 * rotationX)
		#angleX = self.__k * (self.__prevX + gyroScaledX) + (self.__k1 * rotationX)#filtered output
		angleY = self.__k * (self.__getYRotation() + gyroScaledY) + (self.__k1 * rotationY)
		#angleY = self.__k * (self.__prevY + gyroScaledY) + (self.__k1 * rotationY)#filtered output
		
		# store new value as previous for filtered output
		#self.__prevX = angleX 
		#self.__prevY = angleY
		
		return (angleX, angleY)