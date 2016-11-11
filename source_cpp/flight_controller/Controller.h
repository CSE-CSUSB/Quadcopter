/*
Translator: Jay (Jackie/Philip) Field
Original Author: Sean Hamilton
Description: Rough translation of python code to Controller into C++.
P.S: Sorry if it's bad. It's been a while.
Description: Receives sensor readings and calculates raw motor percentage to reach predefined setpoint.
*/

#ifndef CONTROLLER_H 
#define CONTROLLER_H
class Controller {
private:
    //Storage Variables
    unsigned short base; //Sensor value when vehicle is on the ground
    unsigned short maxThrottle; //Max motor duty cycle
    unsigned short minThrottle; //Min motor duty cycle
    unsigned short throttleRange; //motor duty cycle range
    unsigned short setPoint; //Destination Value
    unsigned short position;//Current sensor value    
    unsigned short maxInputValue;//max sensor value
    unsigned short minInputValue;//min sensor value
    unsigned short inputValueRange;//usable sensor value range
    unsigned short integral;//running sum of error values in getThrottlePercent
    unsigned short integralThreshold;//max value of integral
    unsigned short prevError;//Error from previous PID iteration in getThrottlePercent
    unsigned short kP;//Proportional Constant
    unsigned short kI;//Ingegral Constant
    unsigned short kD;//Derivative Constant
                      
public:
    Controller() {}//Default Constructor
    //Initializes storage values
    Controller(unsigned short _initialSensorValue, unsigned short _maxThrottle, unsigned short _minThrottle, unsigned short _setPoint,
    unsigned short _integralThreshold, unsigned short _kP, unsigned short _kI, unsigned short _kD) {
        base = _initialSensorValue;
        maxThrottle = _maxThrottle;
        minThrottle = _minThrottle;
        throttleRange = abs(maxThrottle - minThrottle);
        position = base;
        integralThreshold = _integralThreshold;
        kP = _kP;
        kI = _kI;
        kD = _kD;
        setPoint = _setPoint + _initialSensorValue;
    }
    //Updates position variable during flight
    void updatePosition(unsigned short _sensorValue) {
        position = _sensorValue;
    }
    //Assign controller's destination value mid-flight
    void setSetPoint(unsigned short _setPoint) {
        setPoint = _setPoint;
    }
    //Returns throttle value used to reach setPoint
    unsigned short getThrottlePercent(unsigned short _sensorValue) {
        updatePosition(_sensorValue);
        unsigned short error = setPoint - position;//Calculate new error value
        //Calculate new integral value
        if (abs(integral) > abs(integralThreshold)) {
            integral = 0;
        }
        else {
            integral = integral + error;
        }
        unsigned short derivative = error - prevError; //Calculate new derivative value 
        prevError = error;//Update previous error storage
        unsigned int adjustedOutput = (kP * error) + (kI * integral) + (kD * derivative);//Calculates motor compensation


        return adjustedOutput;
    }
    void land() {
        setSetPoint(base);
    }
//Safely return the vehicle to the base position. Will cause vehicle to plummet to the ground currently.
    
};
#endif
