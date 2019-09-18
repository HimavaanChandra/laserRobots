void setup() {
Serial.begin(9600);
}

void loop() {

send_to_pi();
//while(1);  
}

void send_to_pi()
{

Serial.write('H');
delay(500);
Serial.write('A');
delay(500);
Serial.write('B');
delay(500);
Serial.write('C');
delay(500);
Serial.write('D');
delay(500);
Serial.write('E');
delay(500);
Serial.write('K');
delay(500);

}
