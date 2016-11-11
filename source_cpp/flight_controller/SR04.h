/*
Translator: Jay (Jackie/Philip) Field
Original Author: Sean Hamilton
Description: Interface for the SR04 Ultrasonic Sensor.
Used to detect the ground and other nearby objects
References: SR04 Datasheet
Description: SR04 Translation
*/

#ifndef SR04_H
#define SR04_H
class SR04 {
private: //constants
  unsigned short triggerPin;
  unsigned short echoPin;
public:
  //initialize GPIO pins for sensor interface
  SR04(unsigned short trigger, unsigned short echo) {
    triggerPin = trigger;
    echoPin = echo;
    pinMode(triggerPin, OUTPUT);
    pinMode(echoPin, INPUT);
  }
  //Measures and returns distance (cm)
  unsigned short getDistance() {
    //send 10us pulse through trigger to begin measurement
    digitalWrite(triggerPin, LOW);//Cut off power to pin
    delay(50);
    digitalWrite(triggerPin, HIGH);//Send pulse to begin measurement.
    delayMicroseconds(10);//10us delay specified in datasheet
    digitalWrite(triggerPin, LOW);
    //Read echo duration
    unsigned short pulse_duration, distance;
    pulseIn(echoPin, HIGH);
    pulse_duration = pulseIn(echoPin, HIGH);
    //Calculate and return distance in cm.
    distance = pulse_duration / 58; //Distance in centimeters
     
    return distance;
  }
};
#endif
