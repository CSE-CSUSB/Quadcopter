/*
Author: Sean Hamilton
QA: 
Date: 11/04/2016
References: Throttle.py
Description: manages motor output based on sensor input
*/

#ifndef THROTTLE_H
#define THROTTLE_H

class Throttle {
private:
  //storage variables
  unsigned short
    __max_throttle = 0, //maximum allowable throttle
    __min_throttle = 0, //minimum allowable throttle
    __motor_pin[4], //io pin corresponding to the motor
    __throttle[4]; //stores motor throttle values

  /*
  Custom PWM assignment function.
  @param: pin - arduino pin the change applies to
  @param: us - time in microseconds to modulate the signal
  */
  void change_duty_cycle(unsigned short pin, unsigned short us){
    digitalWrite(pin, HIGH);
    delayMicroseconds(us);
    digitalWrite(pin, LOW);
    delayMicroseconds(18350 - us);//18350 is the constant calculated to output a signal at 54Hz
  }
public:
  /*
  Constructor, initializes storage variables.
  @param: motor_1_pin - the pin corresponding to motor 1
  @param: max_throttle - the maximum allowable throttle to control the motor
  @param: min_throttle - the minimum allowable throttle to control the motor
  */
  Throttle(unsigned short motor_1_pin, unsigned short motor_2_pin, unsigned short motor_3_pin, unsigned short motor_4_pin, unsigned short max_throttle, unsigned short min_throttle)
  {
    __motor_pin[0] = motor_1_pin;
    __motor_pin[1] = motor_2_pin;
    __motor_pin[2] = motor_3_pin;
    __motor_pin[3] = motor_4_pin;
    __max_throttle = max_throttle;
    __min_throttle = min_throttle;
    __throttle[0] = min_throttle;
    __throttle[1] = min_throttle;
    __throttle[2] = min_throttle;
    __throttle[3] = min_throttle;
  }

  /*
  Assigns new throttle value to the motor based on the quadcopter's orientation parameters
  @param: altitude - quadcopter's altitude parameter
  @param: roll - quadcopter's left/right tilt parameter
  @param: pitch - quadcopter's forward/backward tilt parameter
  @param: yaw - quadcopter's direction parameter
  */
  unsigned short setThrottle(float altitude, float roll, float pitch, float yaw)
  {
    //assign x-configuration throttle to motors 1 - 4
    __throttle[0] = altitude + pitch + roll + yaw;
    __throttle[1] = altitude + pitch - roll - yaw;
    __throttle[2] = altitude - pitch + roll - yaw;
    __throttle[3] = altitude - pitch - roll + yaw;

    //force throttle within desired range and assign value
    for(short i = 0; i < 4; ++i){
      if(__throttle[i] > __max_throttle)
        __throttle[i] = __max_throttle;
      else if(__throttle[i] < __min_throttle)
        __throttle[i] = __min_throttle;
      change_duty_cycle(__motor_pin[i], __throttle[i]);
    }
  }
  
  /*
  Sets throttle to a safe no-movement value
  */
  throttleEnd()
  {
    for(short i = 0; i < 4; ++i){
      change_duty_cycle(__motor_pin[i], __min_throttle);
    }
  }
};

#endif
