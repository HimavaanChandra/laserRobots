#include <AccelStepper.h>

AccelStepper LeftWheel(1, 2, 3); // (Type:driver, STEP, DIR) - Stepper1
AccelStepper RightWheel(1, 4, 5); // Stepper2

int wheelSpeed = 800;
int Delay = 2;
int newPos;
int requiredAng;
int currentAng;
#define DIS 1000
#define LDIS 1700
#define NUMBERTOCONVERTSTEPSTOANG 1000
#define RIGHT 0
#define LEFT 1


void setup() {
  // Set initial speed values for the steppers
  LeftWheel.setMaxSpeed(3000);
  RightWheel.setMaxSpeed(3000);
}


void loop() {
  //Need 10 switch cases, corresponding to the 8 points around the robot (as well as staying stationary) and one additional to fire the laser
  //Make each movement move in grids of 5mm
  delay(5);
  Movement(requiredAng, currentAng, newPos);

  // Model the code in each switch case to be similar to this, with left, right, up, down only having a distance measurement and diagonal movement having an additional angle movement
  //    for (int x = 0; x < Distance(1000); x++) {
  //      moveForward();
  //      motorGo();
  //    }

}

//Use these functions in the code
void moveForward() {
  LeftWheel.setSpeed(wheelSpeed);
  RightWheel.setSpeed(-wheelSpeed);
}
//  void moveBackward() {
//    LeftWheel.setSpeed(-wheelSpeed);
//    RightWheel.setSpeed(wheelSpeed);
//  }
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

void motorGo() {
  delay(Delay);
  LeftWheel.runSpeed();
  RightWheel.runSpeed();
}

void Move(int dis) {
  for (int x = 0; x < dis; x++) {
    moveForward();
    motorGo();
  }
}


//  int Distance(int dis) {
//    //Check final code which was uploaded to git for demonstration, number in that should be reflected here. Similar with the angle number.
//    //  return (int)(dis*1.099557);
//    //  return (int)(dis / 0.95);
//    return (int)(dis);
//
//  }
int Movement(int requiredAng,int currentAng,int newPos) {
  int turn;
  if (newPos == 0) {  //don't move
    stopMoving();
    motorGo();
  } else if (newPos == 9) {  //pew pew
    stopMoving();
    motorGo();
  }
  else {
    turn = requiredAng + (-1 * currentAng);

    if (turn > 0 && turn <= 180) {
      Rotate(turn , RIGHT);
    } else if (turn > 0 && turn > 180) {
      Rotate(turn , LEFT);
    } else if (turn < 0 && turn >= -180) {
      Rotate(turn , LEFT);
    } else if (turn < 0 && turn < 180) {
      Rotate(turn , RIGHT);
    }
    currentAng = requiredAng;
    if (currentAng % 90 == 0) {
      Move(DIS);
    } else {
      Move(LDIS);
    }
  }
}



void Rotate(int ang, bool dir) {
  ang = ang*NUMBERTOCONVERTSTEPSTOANG;
  switch (dir) {
    case 0:
      for (int x = 0; x < ang; x++) {
        rotateRight();
        motorGo();
      }
      break;

    case 1:
      for (int x = 0; x < ang; x++) {
        rotateLeft();
        motorGo();
      }
      break;
  }
}

//
//  int Angle(int ang) {
//    //  return (int)(ang*1.82537);
//    return (int)(ang * 2.5);
//  }
