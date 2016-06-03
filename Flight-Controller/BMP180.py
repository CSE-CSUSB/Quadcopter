'''
Author: Sean R Hamilton
Date: 05/06/2016
References: BOSCH BMP180 Datasheet, Adafruit_Python_GPIO and Adafruit_Python_BMP git repositories
Description: Reads tempurature and pressure data from the BMP180 via i2c interface and uses it to calculate altitude.
Assumes the program is being run from the raspi B rev 1
'''
import smbus
import time

class BMP180:
	# BMP180 i2c address.
	__ADDR = 0x77
	
	# initialize smbus for i2c interface
	__bus = smbus.SMBus(1)
	
	# Operating Modes
	__ULTRALOWPOWER = 0
	__STANDARD = 1
	__HIGHRES = 2
	__ULTRAHIGHRES = 3

	# Calibration Register Addresses
	__CAL_AC1 = 0xAA
	__CAL_AC2 = 0xAC
	__CAL_AC3 = 0xAE
	__CAL_AC4 = 0xB0
	__CAL_AC5 = 0xB2
	__CAL_AC6 = 0xB4
	__CAL_B1 = 0xB6
	__CAL_B2 = 0xB8
	__CAL_MB = 0xBA
	__CAL_MC = 0xBC
	__CAL_MD = 0xBE
	__CONTROL = 0xF4
	
	# Raw Temp/Pressure Data Storage
	__TEMPDATA = 0xF6
	__PRESSUREDATA = 0xF6
	
	# Calibration Register Variables
	__cal_AC1 = 0	# INT16
	__cal_AC2 = 0	# INT16
	__cal_AC3 = 0	# INT16
	__cal_AC4 = 0	# UINT16
	__cal_AC5 = 0	# UINT16
	__cal_AC6 = 0	# UINT16
	__cal_B1 =  0	# INT16
	__cal_B2 =  0	# INT16
	__cal_MB =  0	# INT16
	__cal_MC =  0	# INT16
	__cal_MD =  0 # INT16

	# Commands sensor to update temp/press registers
	__READTEMPCMD = 0x2E
	__READPRESSURECMD = 0x34
	
	
	# read 16 bit unsigned integer from register
	def __read16uint(self, addr, reg):
		result = self.__bus.read_word_data(addr, reg) & 0xFFFF	# value ANDed with 1's to remove any values outside the desired bit range
		result = ((result << 8) & 0xFF00) + (result >> 8)	# read_word_data assumes little-endian. The first and last 8 bits are swapped to convert the result to big-endian
		return result
	
	# read 16 bit signed integer from register
	def __read16sint(self	, addr, reg):
		result = self.__read16uint(addr, reg)
		if result > 32767:	# restrict values to signed 16 bit range
			result -= 65536
		return result
	
	#load calibration values from sensor register on initialization
	def __init__(self):
		self.__cal_AC1 = self.__read16sint(self.__ADDR, self.__CAL_AC1)	# INT16
		self.__cal_AC2 = self.__read16sint(self.__ADDR, self.__CAL_AC2)	# INT16
		self.__cal_AC3 = self.__read16sint(self.__ADDR, self.__CAL_AC3)	# INT16
		self.__cal_AC4 = self.__read16uint(self.__ADDR, self.__CAL_AC4)	# UINT16
		self.__cal_AC5 = self.__read16uint(self.__ADDR, self.__CAL_AC5)	# UINT16
		self.__cal_AC6 = self.__read16uint(self.__ADDR, self.__CAL_AC6)	# UINT16
		self.__cal_B1 =  self.__read16sint(self.__ADDR, self.__CAL_B1)	# INT16
		self.__cal_B2 =  self.__read16sint(self.__ADDR, self.__CAL_B2)	# INT16
		self.__cal_MB =  self.__read16sint(self.__ADDR, self.__CAL_MB)	# INT16
		self.__cal_MC =  self.__read16sint(self.__ADDR, self.__CAL_MC)	# INT16
		self.__cal_MD =  self.__read16sint(self.__ADDR, self.__CAL_MD)	# INT16
	
	
	# read and return raw tempurature value
	def __readRawTemp(self):
		self.__bus.write_byte_data(self.__ADDR, self.__CONTROL, self.__READTEMPCMD)	# tell BMP180 to update temperature register
		time.sleep(0.005)	# delay specified by datasheet
		return self.__read16uint(self.__ADDR,self.__TEMPDATA)
	
	# read and return raw pressure value
	def __readRawPressure(self):
		self.__bus.write_byte_data(self.__ADDR, self.__CONTROL, self.__READPRESSURECMD + (self.__STANDARD << 6))
		time.sleep(0.008)	# delay specified by datasheet
		msb = self.__bus.read_byte_data(self.__ADDR, self.__PRESSUREDATA) & 0xFF
		lsb = self.__bus.read_byte_data(self.__ADDR, self.__PRESSUREDATA + 1) & 0xFF
		xlsb = self.__bus.read_byte_data(self.__ADDR, self.__PRESSUREDATA + 2) & 0xFF
		return ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self.__STANDARD)
		
	# calculate tempurature variables from raw value
	def __calcTemp(self):
		X1 = ((self.__readRawTemp() - self.__cal_AC6) * self.__cal_AC5) / 32768
		X2 = ((self.__cal_MC) * 2048) / (X1 + self.__cal_MD)
		B5 = X1 + X2
		#T = (B5 + 8) * 0.1 / 16	# this line is in the datasheet but does not appear to have any use for calculating altitude
		return B5
		
	# calculate and return pressure from raw value
	def __calcPressure(self):
		B6 = self.__calcTemp() - 4000
		X1 = (self.__cal_B2 * (B6 * B6) / 4096) / 2048
		X2 = (self.__cal_AC2 * B6) / 2048
		X3 = X1 + X2
		B3 = (((self.__cal_AC1 * 4 + X3) << self.__STANDARD) + 2) / 4
		X1 = (self.__cal_AC3 * B6) / 8192
		X2 = (self.__cal_B1 * ((B6 * B6) / 4096)) / 65536
		X3 = ((X1 + X2) + 2) / 4
		B4 = (self.__cal_AC4 * (X3 + 32768)) / 32768
		B7 = ( self.__readRawPressure() - B3) * (50000 >> self.__STANDARD)
		if (B7 < 0x80000000):
			p = (B7 * 2) / B4
		else:
			p = (B7 / B4) * 2
		#X1 = (p / 256) * (p / 256)
		#X1 = (X1 * 3038) / 65536
		X1 = (pow(p / 256, 2) * 3038) / 65536	# revised form of above lines from datasheet
		X2 = (-7357 * p) / 65536
		return p + ((X1 + X2 + 3791) / 16)
		
	# returns altitude in meters
	def getAltitude(self):
		i = 0
		avg = 0
		limit = 5
		while i < limit:
			avg += 44330.0 * (1.0 - pow(self.__calcPressure() / 101325.0, (1.0/5.255)))
			i += 1
		return avg / limit
		#return 44330.0 * (1.0 - pow(self.__calcPressure() / 101325.0, (1.0/5.255)))
		

