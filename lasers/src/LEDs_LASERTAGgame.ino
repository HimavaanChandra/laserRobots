#include <FastLED.h>
int i;
int health = 10; //initial health
int mode = 0; //initial mode
int send_flag = 1;

#define receiver 3 //receiver (interrupt) pin
#define laser 8 //laser pin
#define NUM_LEDS 6 //number of LEDS per strip
#define DATA_PIN 7 //LED data pin

CRGB leds [NUM_LEDS]; //setting up array to manipulate tl set/clear LED data
void setup()
{
  pinMode (receiver, INPUT); //receiver pin as input
  pinMode (laser, OUTPUT);
  digitalWrite (laser, HIGH);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS); //strand of neopixels on pin 7, those leds use array "leds" with 6 points
  attachInterrupt (1, receiver_hit, RISING);; //if receiver is hit run the laser_hit function
  Serial.begin(9600);
}

void loop()
{
  send_to_pi(health);
  switch (mode)
  {
    case 0: //********************************case 1 - not being hit
      i = 0;
      if (health <= 0)
      {
        for (i; i < NUM_LEDS; i++)// turn led red
        {
          leds[i] = CRGB::Red;
        }
        FastLED.show();
      }
      
      else if (health <= 3 & health > 0) //turn led yellow
      {
        for (i; i < NUM_LEDS; i++)
        {
          leds[i] = CRGB::Orange;
        }
        FastLED.show();
      }
      
      else 
      {
        for (i; i < NUM_LEDS; i++) //turn led green
        {
          leds[i] = CRGB::Green;
        }
        FastLED.show();
      }
      
      break;

    case 1: // ***************************case 2 - after being hit, then back to first case
      i = 0;
      for (i; i < NUM_LEDS; i++) //flash led red for 100ms, then back to green
      {
        leds[i] = CRGB::Red;
      }
      FastLED.show();

      delay (250);
  
      mode = 0; // backt to first mode

      break;
  }
  get_from_pi();
}


void receiver_hit ()
{
  if (mode == 0) 
  {
    if (health > 0) {
      health--;
      mode = 1;
      send_flag = 1;
    }
  }
}



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

void get_from_pi()
{
  if (Serial.available())
  { //From RPi to Arduino
    String s = Serial.readStringUntil("\n");
    Serial.print("Pi Says: ");
    Serial.print(s);
  }
}
