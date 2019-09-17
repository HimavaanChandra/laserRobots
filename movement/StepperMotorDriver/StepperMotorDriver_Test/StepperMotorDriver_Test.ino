#include <bitswap.h>
#include <chipsets.h>
#include <color.h>
#include <colorpalettes.h>
#include <colorutils.h>
#include <controller.h>
#include <cpp_compat.h>
#include <dmx.h>
#include <FastLED.h>
#include <fastled_config.h>
#include <fastled_delay.h>
#include <fastled_progmem.h>
#include <fastpin.h>
#include <fastspi.h>
#include <fastspi_bitbang.h>
#include <fastspi_dma.h>
#include <fastspi_nop.h>
#include <fastspi_ref.h>
#include <fastspi_types.h>
#include <hsv2rgb.h>
#include <led_sysdefs.h>
#include <lib8tion.h>
#include <noise.h>
#include <pixelset.h>
#include <pixeltypes.h>
#include <platforms.h>
#include <power_mgt.h>

//Stepper Motor Driver Code for MX2 Movement

#include <AccelStepper.h>


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
int CurrentPos = 0;
int CurrentDir = 0;

//Laser Variables
#define ShotTime 500
#define Receiver 12

int ShotCooldown = (ShotTime * 2);
int Health = 10;
int HitButton = 0;


void setup() {
  //Movement
  //Set max speed in steps per second
  LeftStepper.setMaxSpeed(1000);
  RightStepper.setMaxSpeed(1000);



  //Lasers
  pinMode(13, OUTPUT); //Initialise for laser output
  pinMode(12, INPUT); //Initialise for receiver input
  digitalWrite(13, LOW); //Turn off
}

void loop() {
  //Set current position to 0
  //Calls movement function.
  Movement(0, 200, 200);


}

//When called input Movement (Direction,Speed)
void Movement(int StepperDir, int StepperDistance, int StepperSpeed)
{
  //Motor rotation for movement
  //L-CW & R-CCW = Forward
  //L-CCW & R-CW = Backward
  //L-CW & R-CW = Turn Right
  //L-CCW & R-CCW = Turn Left


  //Steps Vs. Distance

  LStepperPos = (int)(StepperDir / 1.825397);
  RStepperPos = (int)(StepperDir / 1.825397);

  LStepperDir = (int)(StepperDistance / 1.099557);
  RStepperDir = (int)(StepperDistance / 1.099557);


  // If not at desired position keep rotating
  while (CurrentDir != LStepperPos)
  {
    //Make an if statement working out if the angle is greater than 0. If it is, stepper speed should be positive.
    if (StepperDir > 0)
    {
      LeftStepper.setSpeed(StepperSpeed);
      RightStepper.setSpeed(StepperSpeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      CurrentDir +=1;
//      Laser();
    }
    //Else statement with stepper speed being negative and same four lines of code as above
    else
    {
      LeftStepper.setSpeed(-StepperSpeed);
      RightStepper.setSpeed(-StepperSpeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      CurrentDir +=1;
//      Laser();
    }
    
  }


  //while loop
  while (CurrentPos != LStepperDir)
  {
    //If statement checking if distance is greater than zero. If it is then motor speed should be set to ensure forward movement.
    if (StepperDistance > 0)
    {
      LeftStepper.setSpeed(StepperSpeed);
      RightStepper.setSpeed(-StepperSpeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      CurrentPos +=1;
//      Laser();
    }
    //Else statement with motor speed set to make backwards movement.
    else
    {
      LeftStepper.setSpeed(-StepperSpeed);
      RightStepper.setSpeed(StepperSpeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      CurrentPos+=1;
//      Laser();
    }
    
  }
  CurrentPos = 0;
  CurrentDir = 0;
}


void Laser()
{

  digitalWrite(13, HIGH);
  delay(ShotTime);
  digitalWrite(13, LOW);
  delay(ShotCooldown);

  if ((HitButton == 1) && (digitalRead(Receiver) == LOW)) //If hit lasers turn off
  {
    HitButton = 0;
  }
  if ((HitButton == 0) && (digitalRead(Receiver) == HIGH))
  {
    Health--;
    HitButton = 1;
  }
}
