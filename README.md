# Quadcopter
Student led Computer Science and Engineering project at CSU San Bernardino that aims to design and build a quadcopter capable of autonomous flight and visual object tracking.

## Quarterly Goals
FA15 - Test Motor Control w/Remote Joystick [ACCOMPLISHED]  
WI16 - Establish Autonomous Motor Control and Sensor Input [ACCOMPLISHED]  
SP16 - Implement Altitude Control Algorithm [ACCOMPLISHED]  
FA16 - Perform Autonomous Hover Test [IN PROGRESS]  
WI17 - Stabilize Hover Algorithm  
SP17 - Implement Simple Visual Object Tracking  

## Files
BMP180.py - defines the api for the barometer  
MPU6050.py - defines the api for the gyro/accelerometer  
Throttle.py - manages motor interface  
Controller.py - translates sensor inputs into motor outputs  
flightController.py - contains the other classes and receives user input  
