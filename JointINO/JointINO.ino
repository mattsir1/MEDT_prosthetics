#include "Joint.h"
//#include <VarSpeedServo.h>
//Define attached pins
#define TESTPIN_1 2 
#define TESTPIN_2 3
#define TESTPIN_3 4
#define TESTPIN_4 8
#define TESTPIN_5 11

#define FSRPIN A0 //connect force sensor to A0 in series with 10K

int *ptr;

//Define Joints
TestJoint test1, test2, test3, test4, test5;
int speed = 100; //modify speed from 1-255 slower to faster

void setup() {
  Serial.begin(9600);
  Joint::setupTestSignalIn(FSRPIN);
  Joint::changeSpeedVals(speed);
  
//Attach pins to servos
  test1.init(TESTPIN_1);
  test2.init(TESTPIN_2);
  test3.init(TESTPIN_3);
  test4.init(TESTPIN_4);
  test5.init(TESTPIN_5);
}



void loop() {
  Joint::updateTestSig();
  ptr=Joint::getSignal();
  Serial.print("Signal value: ");
  Serial.println(*ptr);

  test1.calcAngle();
  test1.setAngle(0);

  test2.calcAngle();
  test2.setAngle(0);

  test3.calcAngle();
  test3.setAngle(0);

  test4.calcAngle();
  test4.setAngle(0);

  test5.calcAngle();
  test5.setAngle(0);
  
  Serial.print("Finger angle:");
  Serial.println(test1.getAngle());
}
