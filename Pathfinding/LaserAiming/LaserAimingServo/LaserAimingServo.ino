#include <Servo.h>

Servo Red_Servo;
Servo Blue_Servo;

int Blue_Angle = 0; // These angles should be inputted from the aiming code
int Red_Angle = 0;  // These angles should be inputted from the aiming code

// Robot Rotation Correction

int Blue_Robot_Rotation_Angle = +0; // Positive = clockwise, Negative = counter clockwise, North facing robot = 0 degrees?
int Red_Robot_Rotation_Angle = +0;  // Positive = clockwise, Negative = counter clockwise, North facing robot = 0 degrees?

int Blue_Angle_Corrected = 0; // Corrected for robot rotation
int Red_Angle_Corrected = 0;  // Corrected for robot rotation

int Red_Out_of_FOV = 0; // Flag to alert when the red robot need to turn around to shoot
int Blue_Out_of_FOV = 0; // Flag to alert when the blue robot need to turn around to shoot

void setup()
{
    Red_Servo.attach(9);
    Red_Servo.attach(8);
}

void loop()
{

    // if (Blue_Robot_Rotation_Angle != 0)

    Blue_Angle_Corrected = Blue_Angle + Blue_Robot_Rotation_Angle;

    if (Blue_Angle_Corrected > 360)
    {
        Blue_Angle_Corrected = Blue_Angle_Corrected % 360;
    }

    else if (Blue_Angle_Corrected < 0)
    {
        Blue_Angle_Corrected = Blue_Angle_Corrected % 360;
    }

    // if (Red_Robot_Rotation_Angle != 0)

    Red_Angle_Corrected = Red_Angle + Red_Robot_Rotation_Angle;

    if (Red_Angle_Corrected > 360)
    {
        Red_Angle_Corrected = Red_Angle_Corrected % 360;
    }

    else if (Red_Angle_Corrected < 0)
    {
        Red_Angle_Corrected = Red_Angle_Corrected % 360;
    }

    // if (0<=Red_Angle_Corrected<=180)   // Add if 360 degree servos not available (other parts of code will probably also have to be modified aswell?)
    Red_Servo.write(Red_Angle_Corrected);
    // Red_Out_of_FOV = 0;

    // else
    // {
    //     Red_Out_of_FOV = 1;
    //     return Red_Out_of_FOV;
    // }

    // if (0<=Red_Angle_Corrected<=180)   // Add if 360 degree servos not available (other parts of code will probably also have to be modified aswell?)
    Blue_Servo.write(Blue_Angle_Corrected);
    // Blue_Out_of_FOV = 0;

    // else
    // {
    //     Blue_Out_of_FOV = 1;
    //     return Blue_Out_of_FOV;
    // }

        delay(10);
}
