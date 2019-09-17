//Stepper Motor Driver Code for MX2 Movement

#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Stepper.h>

//Movement Variables
//Define stepper motor connections and motor interface type(driver)
#define LMotorInterfaceType 1
#define LStepPin 2
#define LDirPin 3

#define RMotorInterfaceType 1
#define RStepPin 4
#define RDirPin 5

//Create a new instance of the AccelStepper class
AccelStepper LeftStepper = AccelStepper(LMotorInterfaceType, LStepPin, LDirPin);
AccelStepper RightStepper = AccelStepper(RMotorInterfaceType, RStepPin, RDirPin);

int RStepperPos = 0;
int LStepperPos = 0;
int RStepperDir = 0;
int LStepperDir = 0;
int StepperDir = 0;
int StepperSpeed = 0;
int StepDir = 0;
int StepSpeed = 0;
int StepperDistance = 0;

//Laser Variables
#define ShotTime 500
#define Receiver 12

int ShotCooldown = (ShotTime * 2);
int Health = 10;
int HitButton = 0;


void setup() {
  //Movement
  //Set max speed in steps per second
  LeftStepper.setMaxSpeed(400);
  RightStepper.setMaxSpeed(400);

  //Lasers
  pinMode(13, OUTPUT); //Initialise for laser output
  pinMode(12, INPUT); //Initialise for receiver input
  digitalWrite(13, LOW); //Turn off
}

void loop() {
  //Set current position to 0
  LeftStepper.setCurrentPosition(0);
  RightStepper.setCurrentPosition(0);

  //Calls movement function.
  Movement(0, 1000, 200);


}

//When called input Movement (Direction,Speed)
void Movement(int StepperDir, int StepperDistance, int StepperSpeed)
{
  //Motor rotation for movement
  //L-CW & R-CCW = Forward
  //L-CCW & R-CW = Backward
  //L-CW & R-CW = Turn Right
  //L-CCW & R-CCW = Turn Left

  //Set current position of both steppers to 0
  LeftStepper.setCurrentPosition(0);
  RightStepper.setCurrentPosition(0);

  //Steps Vs. Distance
  //Set 2 variables, one for each wheel for the amount of steps each wheel is required to turn to reach the required angle. Steps calculated by working out how many steps
  //are required to move the robot 1 degree then dividing the degree StepperDir variable by that number. Ensure that each variable remains an int even though the calculation
  //may result in a float value.
  LStepperPos = (int)(StepperDir / 1.825397);
  RStepperPos = (int)(StepperDir / 1.825397);

  //Set 2 variables, one for each wheel for the amount of steps each wheel is required to turn to reach the required distance. Steps calculated by working out the distance
  //travelled per step then dividing the StepperDistance variable by that value. Make one of the variables negative to ensure that the wheel will turn the opposite direction
  //to the other wheel, making forward/back motion/Ensure that each variable remains an int even though the calculation may result in a float value.
  LStepperDir = (int)(StepperDistance / 1.099557);
  RStepperDir = -1 * ((int)(StepperDistance / 1.099557));

  // If not at desired position keep rotating
  while (LeftStepper.currentPosition() != LStepperPos || RightStepper.currentPosition() != RStepperPos)
  {
    //Make an if statement working out if the angle is greater than 0. If it is, stepper speed should be positive.
    if (StepperDir > 0)
    {
      LeftStepper.setSpeed(StepperSpeed);
      RightStepper.setSpeed(StepperSpeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      Laser();
    }
    //Else statement with stepper speed being negative and same four lines of code as above
    else
    {
      LeftStepper.setSpeed(-StepperSpeed);
      RightStepper.setSpeed(-StepperSpeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      Laser();
    }
  }

  //New while loop which will run the robots in the forward/backwards directions. Set up same as previous loop but with the two distance variables set up before the first
  //Set current position of both steppers to 0
  LeftStepper.setCurrentPosition(0);
  RightStepper.setCurrentPosition(0);
  //while loop
  while (LeftStepper.currentPosition() != LStepperDir || RightStepper.currentPosition() != RStepperDir)
  {
    //If statement checking if distance is greater than zero. If it is then motor speed should be set to ensure forward movement.
    if (StepperDistance > 0)
    {
      LeftStepper.setSpeed(StepperSpeed);
      RightStepper.setSpeed(-StepperSpeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      Laser();
    }
    //Else statement with motor speed set to make backwards movement.
    else
    {
      LeftStepper.setSpeed(-StepperSpeed);
      RightStepper.setSpeed(StepperSpeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      Laser();
    }
  }
}


void Laser()
{
  digitalWrite(13, HIGH);
  delay(ShotTime);
  digitalWrite(13, LOW);
  delay(ShotCooldown);

  if ((HitButton == 1) && (digitalRead(Receiver) == HIGH)) //If hit lasers turn off
  {
    HitButton = 0;
  }
  if ((HitButton == 0) && (digitalRead(Reciever) == HIGH))
  {
    Health--;
    HitButton = 1;
  }
}
