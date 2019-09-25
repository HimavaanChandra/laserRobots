#include <avr/io.h>
#include <stdio.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd (8, 9, 4, 5, 6, 7);
#define shot_time 500 //in milliseconds
#define RECEIVER 12
int shot_warmdown = (shot_time * 2);
int health = 10;
int hitBUTTON = 0;

void setup()
{
  //*********************ININTIALISE PORTS**************************************//
  DDRB |= (1 << 5);  //initialise pin 13 as output
  PORTB |= (1 << 5); //turn on laser
  DDRB &= ~(1 << 4); //initialise pin 12 as input (for receiver)

  // **********************LCD initializations ***********************
  lcd.begin (16,2); //start LCD library
  lcd.setCursor (0,0);
  lcd.print ("Health:");
}

void loop()
{

  PORTB |= (1 << 5);
  delay(shot_time);
  PORTB &= ~(1 << 5);
  delay(shot_warmdown);

  // lcd.setCursor (7,0);
  // lcd.print (health); //display the health levels on the lcd

  if (hitBUTTON == 1 & (digitalRead(RECEIVER) == LOW)) // if been hit and then laser turns off
  {
    hitBUTTON = 0;
  }

  if ((hitBUTTON == 0) & (digitalRead(RECEIVER) == HIGH)) // if laser hits receiver
  {
    health--;
    hitBUTTON = 1;
  }
}
