#!/usr/bin/python

'''
SR04 test
'''
from SR04 import SR04

u = SR04(17, 22) #trigger, echo

print u.getDistance()