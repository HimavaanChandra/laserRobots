
//assigning pins
#define laser_beam 7
#define laser_receiver 3 // Uno interrupt pin 1
#define interrupt_pin 2 // Uno interrupt pin 0
int health = 10;
//int receiver_button = 0; //flag to ensure health doesn't continuously drop when receiver being hit --- may not be needed when using interrupts

void setup() 
{
  Serial.begin (9600); //initialise serial monitor
  Serial.print ("START\nHealth: ");
  Serial.print (health);
  
  
  pinMode (laser_beam, OUTPUT);//set laser beam pin as output
  pinMode (laser_receiver, INPUT); //set laser receiver pin as input
  pinMode (interrupt_pin, OUTPUT); //set the interrupt pin as out (so I can toggle manually), this will tie into Olly's function to shoot -- NEEDS TO BE CHANGED TO INPUT WHEN INTEGRATED
  digitalWrite (laser_beam, LOW); //initially set as low
  
//  attachInterrupt (0, laser_shoot, RISING); //interrupt to turn on laser with olly's command to shoot to arduino
//  attachInterrupt (0, laser_off, FALLING); //interrupt to turn off laser when pin goes low
  attachInterrupt (1, receiver_hit, RISING); //interrupt to drop health when receiver is hit
}

void loop() 
{
  digitalWrite (laser_beam, HIGH);

  /*******following may not be needed when using interrupt - receiver_hit function occurs quicker without
  if ((digitalRead(laser_receiver) == LOW) & (receiver_button == 1)) //if receiver is not being hit but button is on
  {
    receiver_button = 0;
  }*/
}

//void laser_shoot ()//function to turn on laser beam
//{
//  digitalWrite (laser_beam, HIGH);
//}
//
//void laser_off () //function to turn off laser beam
//{
//  digitalWrite (laser_beam, LOW);
//}

void receiver_hit ()
{
//  if (receiver_button == 0)
//  {
    health--;
    if (health >= 1)
    {
      Serial.print ("Hit! \nHealth: ");
      Serial.print (health);
      Serial.print ("\n\n");
//      receiver_button = 1;
    }

    else if (health == 0)
    {
      Serial.print ("GAME OVER!!!!\n");
    }
//  }
}