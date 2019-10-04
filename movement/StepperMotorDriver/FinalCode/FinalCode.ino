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

#include <AccelStepper.h>

AccelStepper LeftWheel(1, 2, 3); // (Type:driver, STEP, DIR) - Stepper1
AccelStepper RightWheel(1, 4, 5); // Stepper2

int wheelSpeed = 800;
int Delay = 2;

#define NUM_LEDS 6
CRGB leds[NUM_LEDS];
#define PIN 6

void setup() {
  // Set initial seed values for the steppers
  pinMode(LED_BUILTIN, OUTPUT);
  LeftWheel.setMaxSpeed(3000);
  RightWheel.setMaxSpeed(3000);

  FastLED.addLeds<WS2811, PIN, GRB>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
}

void loop() { ////REDO BY MANUAL DOING MOVEMENTS AND RECORDING IT THEN COPY PASTE

  delay(5000);
  // put your main code here, to run repeatedly:
  for (int x = 0; x < Distance(1000); x++) {
    moveForward();
    //ledBlink(500);
    motorGo();
    

  }

  delay(5000);

  for (int x = 0; x < Distance(500); x++) {
    moveForward();
    //ledBlink(500);
    motorGo();

  }
}
void moveForward() {
  LeftWheel.setSpeed(wheelSpeed);
  RightWheel.setSpeed(-wheelSpeed);
}
void moveBackward() {
  LeftWheel.setSpeed(-wheelSpeed);
  RightWheel.setSpeed(wheelSpeed);
}
void rotateLeft() {
  LeftWheel.setSpeed(-wheelSpeed);
  RightWheel.setSpeed(-wheelSpeed);
}
void rotateRight() {
  LeftWheel.setSpeed(wheelSpeed);
  RightWheel.setSpeed(wheelSpeed);
}
void stopMoving() {
  LeftWheel.setSpeed(0);
  RightWheel.setSpeed(0);
}
void ledBlink(int Delay) {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(Delay);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(Delay);                       // wait for a secon
}

void motorGo() {
  delay(Delay);
  LeftWheel.runSpeed();
  RightWheel.runSpeed();
}

int Distance(int dis) {
  //  return (int)(dis*1.099557);
//  return (int)(dis / 0.95);
  return (int)(dis);

}

int Angle(int ang) {
  //  return (int)(ang*1.82537);
  return (int)(ang * 2.5);
}

//LED Stuff
void rainbowCycle(int SpeedDelay) {
  byte *c;
  uint16_t i, j;

  for (j = 0; j < 256 * 5; j++) { // 5 cycles of all colors on wheel
    for (i = 0; i < NUM_LEDS; i++) {
      c = Wheel(((i * 256 / NUM_LEDS) + j) & 255);
      setPixel(i, *c, *(c + 1), *(c + 2));
    }
    showStrip();
    delay(SpeedDelay);
  }
}

// used by rainbowCycle and theaterChaseRainbow
byte * Wheel(byte WheelPos) {
  static byte c[3];

  if (WheelPos < 85) {
    c[0] = WheelPos * 3;
    c[1] = 255 - WheelPos * 3;
    c[2] = 0;
  } else if (WheelPos < 170) {
    WheelPos -= 85;
    c[0] = 255 - WheelPos * 3;
    c[1] = 0;
    c[2] = WheelPos * 3;
  } else {
    WheelPos -= 170;
    c[0] = 0;
    c[1] = WheelPos * 3;
    c[2] = 255 - WheelPos * 3;
  }

  return c;
}
// *** REPLACE TO HERE ***



// ***************************************
// ** FastLed/NeoPixel Common Functions **
// ***************************************

// Apply LED color changes
void showStrip() {
#ifdef ADAFRUIT_NEOPIXEL_H
  // NeoPixel
  strip.show();
#endif
#ifndef ADAFRUIT_NEOPIXEL_H
  // FastLED
  FastLED.show();
#endif
}

// Set a LED color (not yet visible)
void setPixel(int Pixel, byte red, byte green, byte blue) {
#ifdef ADAFRUIT_NEOPIXEL_H
  // NeoPixel
  strip.setPixelColor(Pixel, strip.Color(red, green, blue));
#endif
#ifndef ADAFRUIT_NEOPIXEL_H
  // FastLED
  leds[Pixel].r = red;
  leds[Pixel].g = green;
  leds[Pixel].b = blue;
#endif
}

// Set all LEDs to a given color and apply it (visible)
void setAll(byte red, byte green, byte blue) {
  for (int i = 0; i < NUM_LEDS; i++ ) {
    setPixel(i, red, green, blue);
  }
  showStrip();
}
