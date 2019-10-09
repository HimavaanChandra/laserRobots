#include <stdio.h>
#include <string.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);
void setup()
{
  Serial.begin(9600);
  lcd.begin(16, 2);
}
int health = 7;
int m = 0, send_flag = 0;
unsigned int integerValue = 0;

void loop()
{

  //get_from_pi();
  send_flag = 1;
  send_to_pi(health);
  health++;
  delay(1000);
}

void send_to_pi(int f_health)
{
  if (send_flag == 1)
  {
    Serial.print("Health:");
    Serial.print(f_health);
    Serial.print("\n");
  }
  send_flag = 0
}

void get_from_pi()
{
  if (Serial.available())
  { //From RPi to Arduino
    String s = Serial.readStringUntil("\n");
    lcd.setCursor(0, 0);
    //lcd.print(s);
    if (s == "N\n")
    {
      lcd.print("North         ");
    }
    if (s == "S\n")
    {
      lcd.print("South         ");
    }
    if (s == "E\n")
    {
      lcd.print("East          ");
    }
    if (s == "W\n")
    {
      lcd.print("West          ");
    }
    if (s == "NE\n")
    {
      lcd.print("North-East    ");
    }
    if (s == "SW\n")
    {
      lcd.print("South-West    ");
    }
    if (s == "SE\n")
    {
      lcd.print("South-East    ");
    }
    if (s == "NW\n")
    {
      lcd.print("North-West    ");
    }
    if (s == "Shoot\n")
    {
      lcd.print("I'm Shooting  ");
      //digitalWrite(Laser_beam,HIGH);
    }
    if (s == "Reset\n")
    {
      lcd.print("I'm Resetting ");
      //Serial.write(s);
    }
    if (s == "Hit\n")
    {
      lcd.print("Got Hit       ");
    }

    if (s == "s_angle\n")
    {
      lcd.print("Value:     ");
      m = Serial.read();
      lcd.print(m);
    }
  }
}
