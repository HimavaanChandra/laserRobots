#include <Servo.h>

Servo Red_Servo;
Servo Blue_Servo;

int Red_Angle = 0; // These angles should be inputted from the aiming code
int Blue_Angle = 0; // These angles should be inputted from the aiming code

void setup() 
{

  Red_Servo.attach (9);
  Red_Servo.attach (8);
  
}

void loop() 
  {
  
    Red_Servo.write(Red_Angle);
    Blue_Servo.write(Blue_Angle);
    delay(10);
    
  }
}
