#include <AccelStepper.h>

AccelStepper LeftWheel(1,2,3);   // (Type:driver, STEP, DIR) - Stepper1
AccelStepper RightWheel(1,4,5);  // Stepper2

int wheelSpeed = 1500;
int Delay = 2;

void setup() {
  // Set initial seed values for the steppers
  pinMode(LED_BUILTIN, OUTPUT);
  LeftWheel.setMaxSpeed(3000);
  RightWheel.setMaxSpeed(3000);

  
}

void loop() { ////REDO BY MANUAL DOING MOVEMENTS AND RECORDING IT THEN COPY PASTE
  delay(10000);
  // put your main code here, to run repeatedly:
  for(int x=0; x<Distance(1000);x++){   
    moveForward();
    //ledBlink(500);
   motorGo();
  }

  delay(5000);

  for(int x=0; x<Distance(500);x++){   
    moveForward();
    //ledBlink(500);
   motorGo();
  }
}
void moveForward() {
  LeftWheel.setSpeed(wheelSpeed);
  RightWheel.setSpeed(-wheelSpeed);
}
void moveBackward() {
  LeftWheel.setSpeed(-wheelSpeed);
  RightWheel.setSpeed(wheelSpeed);
}
void rotateLeft() {
  LeftWheel.setSpeed(-wheelSpeed);
  RightWheel.setSpeed(-wheelSpeed);
}
void rotateRight() {
  LeftWheel.setSpeed(wheelSpeed);
  RightWheel.setSpeed(wheelSpeed);
}
void stopMoving() {
  LeftWheel.setSpeed(0);
  RightWheel.setSpeed(0);
}
void ledBlink(int Delay) {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(Delay);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(Delay);                       // wait for a secon
}

void motorGo(){
  delay(Delay);
  LeftWheel.runSpeed();
  RightWheel.runSpeed();
  }

int Distance(int dis){
  return (int)(dis/1.099557);
}

int Angle(int ang){
  return (int)(ang*1.82537);
}
