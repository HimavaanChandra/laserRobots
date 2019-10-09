#include <Servo.h>

Servo Laser_Servo;

int Laser_Angle = 90; // Angle should be inputted from the aiming code

int Robot_Rotation_Angle = +0; // Positive = clockwise, Negative = counter clockwise, North facing robot = 0 degrees?

int Laser_Angle_Corrected = 0; // Corrected for robot rotation

int Position = 0; // Flag used in the "Servo_Sweep" function


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
 

void setup()
{
    Laser_Servo.attach(9); // PWM pin
}

void loop()
{
   
    Laser_Angle_Correction (Laser_Angle, Robot_Rotation_Angle);
    
    Servo_Sweep(45);
    delay(5);
    Servo_Sweep(45);
    delay(5);
}
