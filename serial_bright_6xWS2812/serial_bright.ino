#include <FastLED.h>

#define LED_PIN      D8    
#define NUM_LEDS    6   
uint8_t x,y,z;
CRGB leds[NUM_LEDS];
CHSV BLUE(170,255,0);
CHSV RED(0,255,0);
CHSV GREEN(95,255,0);
byte buffer[3];
void setup() {
  FastLED.addLeds<WS2812, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(64); 
  Serial.begin(9600);
}

void loop() {
   if (Serial.available()) {//从串口中读取数据
    Serial.readBytes(buffer,3);  
    x=buffer[0];
    y=buffer[1];
    z=buffer[2];
    BLUE.v=x;
    RED.v=y;
    GREEN.v=z;
   }
   else{ 
    x=0;
    y=0;
    z=0;

   }
   Serial.print(x);
    fill_solid(leds, 2, BLUE);
    fill_solid(leds+2, 2, RED);
    fill_solid(leds+4, 2, GREEN);
    FastLED.show();
    delay(5000);
 
}
