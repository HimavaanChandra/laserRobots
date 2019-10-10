#include <AccelStepper.h>
#include <Servo.h>

//***************************************************************DECLARATIONS****************************************************
AccelStepper LeftWheel(1, 4, 5); // (Type:driver, STEP, DIR) - Stepper1
AccelStepper RightWheel(1, 6, 7); // Stepper2
Servo Laser_Servo;

int Laser_Angle = 90; // Angle should be inputted from the aiming code
int Robot_Rotation_Angle = +0; // Positive = clockwise, Negative = counter clockwise, North facing robot = 0 degrees?
int Laser_Angle_Corrected = 0; // Corrected for robot rotation
int Position = 0; // Flag used in the "Servo_Sweep" function

int wheelSpeed = 800;
int Delay = 2;
int newPos;
int requiredAng = 0;
int currentAng = 0;
int pre_heading = 0;
int heading = 0;
char newPos2;
int health = 10; //global health variable of robot
String s;
int reading;

char hit = "C";

int angle = 40;
char shoot = 'S';
int m = 0, send_flag = 0;
unsigned int integerValue = 0;

#define DIS 50
#define LDIS 70.71067811
#define NUMBERTOCONVERTSTEPSTOANG 2.5
#define RIGHT 0
#define LEFT 1
#define laser_beam 8
#define laser_receiver 3 // Uno interrupt pin 1

//**************************************************************SETUP LOOP*************************************************************
void setup()
{
  //***SETUP LASERS**
  pinMode (laser_receiver, INPUT); //receiver pin as input
  pinMode (laser_beam, OUTPUT);
  digitalWrite (laser_beam, LOW);
  //***SETUP INTERRUPTS**
  attachInterrupt (1, receiver_hit, RISING); //interrupt to drop health when receiver is hit
  attachInterrupt (1, receiver_not_hit, FALLING);
  //***SETUP STEPPERS**
  LeftWheel.setMaxSpeed(3000);
  RightWheel.setMaxSpeed(3000);
  //***SETUP SERIAL**
  Serial.begin(9600);
  //SETUP SERVO
  Laser_Servo.attach(9);


}
//*************************************************************MAIN LOOP***************************************************************
void loop()
{
//  reading = get_from_pi();

  Movement(0);
//
//  Laser_Angle_Correction (Laser_Angle, Robot_Rotation_Angle);
//
//  Servo_Sweep(50);
//  Servo_Sweep(50);

//  send_to_pi(health);

}


//***********************************************************FUNCTION DEFINITIONS********************************************************
//*****************************MOVEMENT
void moveForward() {
  LeftWheel.setSpeed(wheelSpeed);
  RightWheel.setSpeed(-wheelSpeed);
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

void motorGo() {
  delay(Delay);
  LeftWheel.runSpeed();
  RightWheel.runSpeed();
}

void Servo_Sweep(int AOE) // "AOE" equals the spray angle of the laser
{
    if (Laser_Angle_Corrected >= 45 && Laser_Angle_Corrected <= 135) // Include if 360 degree servos not available
    {
        if (Position == 0)
        {
            Laser_Servo.write(Laser_Angle_Corrected + AOE / 2);
            Position = 1;
        }
        else if (Position == 1)
        {
            Laser_Servo.write(Laser_Angle_Corrected - AOE / 2);
            Position = 0;
        }
    }
// Laser_Servo.write(Laser_Angle);
}

void Laser_Angle_Correction (int Laser_Angle, int Robot_Rotation_Angle)
{
  // if (Robot_Rotation_Angle != 0)

    Laser_Angle_Corrected = Laser_Angle + Robot_Rotation_Angle;

    if (Laser_Angle_Corrected >= 360)
    {
        Laser_Angle_Corrected = Laser_Angle_Corrected % 360;
    }

    else
    {
        Laser_Angle_Corrected = Laser_Angle_Corrected + 360; // Converts from negative to postive angle equivelant
        Laser_Angle_Corrected = Laser_Angle_Corrected % 360;
    }

}

void Move(int dis) {
  for (int x = 0; x < dis; x++) {
    moveForward();
    motorGo();
  }
}

int Movement(int requiredAng) {
  digitalWrite (laser_beam, LOW);
  int turn;

//  if (newPos == 'A') {  //don't move
//    stopMoving();
//    motorGo();
//  } else if (newPos == "SHOOT") {  //pew pew
//    stopMoving();
//    motorGo();
//    digitalWrite (laser_beam, HIGH);
//  }
//  else {
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
//    }
  }
}

void Rotate(int ang, bool dir) {
  ang = ang * NUMBERTOCONVERTSTEPSTOANG;
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

//*********************LASERS
void receiver_not_hit ()
{
  hit = "C";
}

void receiver_hit ()
{
  hit = "H";
  health--;
  send_flag = 1;
}

//*********************SERIAL COMS
void send_to_pi(int f_health)
{
  if (send_flag == 1)
  {
    Serial.print("Health:");
    Serial.print(f_health);
    Serial.print("\n");
  }
  send_flag = 0;
}

int get_from_pi()
{
  if (Serial.available())
  { //From RPi to Arduino
    String s = Serial.readStringUntil("\n");
    if (s == "N\n")
    {
      heading = 0;
    }
    if (s == "S\n")
    {
      heading = 180;
    }
    if (s == "E\n")
    {
      heading = 90;
    }
    if (s == "W\n")
    {
      heading = -90;
    }
    if (s == "NE\n")
    {
      heading = 45;
    }
    if (s == "SW\n")
    {
      heading = -135;
    }
    if (s == "SE\n")
    {
      heading = 135;
    }
    if (s == "NW\n")
    {
      heading = -45;
    }
  }
  return heading;
}
