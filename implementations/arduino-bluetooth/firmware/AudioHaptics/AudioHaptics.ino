#include <SoftwareSerial.h>
#include <stdlib.h>
#include <stdio.h>

int period = 100;
unsigned long time_now = 0; 
 
void print_time(unsigned long time_millis);

char c=' '; 

// Bluetooth serial communication (RX=17, TX=16)
SoftwareSerial Bluetooth(17, 16);

// the on-board LED
int LED = 13;// Arduino pin numbers

// Haptic motor PWM pins
int LEDPins[] = { 5, 6, 9, 10, 11 };

int FrontLeft = 5;
int FrontRight = 11;
int SideLeft = 6;
int SideRight = 10;
int Center = 9;

int CW[ ] = { Center, SideLeft, FrontLeft, FrontRight, SideRight, Center }; //3
int CCW[ ] =  { Center, SideRight, FrontRight, FrontLeft, SideLeft, Center }; //4
int PULSE[ ] = { Center, SideLeft, FrontLeft, Center, SideRight, FrontRight }; //7
int PULSX[] = { Center, SideRight, FrontRight, Center, SideLeft, FrontLeft };

int FRONT[] = { 5, 6 };
int BACK[ ] = { 10, 11, 9 };

int FL[ ] = { 5, 5 }; // 5, 13
int FR[ ] = { 11, 11 };
int SL[ ] = { 6, 6 };
int SR[ ] = { 10, 10 };
int C[ ] = { 9, 9 };
int BUZZ[ 2 ] = { 5, 5 };

char bundleIN[ 4 ] = { };
int index;
int jindex;
int reps;
int count;
int freq;

boolean full = false;
boolean lights = false;
boolean newIN = false;

int i;
int numC;
int freqC;
int buzzC;

void LED_wave( int PINS[], int PINlength, int count, int freq) {
  Serial.println("\nlights on");
  int delayTime = freq*100;
  Serial.print(delayTime);
  Serial.print("\n");
  for ( jindex = 0; jindex < count; jindex++ ) {
    for ( index = 0; index < PINlength; index++ ) {
       digitalWrite( PINS[ index ], HIGH );
       delay( delayTime );
       digitalWrite( PINS[ index ], LOW );
    }
  }
  Serial.println("lights off\n");
  lights = true;
  newIN = false;
}

void setup() {
  Bluetooth.begin(57600);
  Serial.begin(57600);
  pinMode( LED, OUTPUT );
  for ( index = 0; index <= 5; index++ ) {
    pinMode( LEDPins[ index ], OUTPUT );
  }
}

void loop() {
  int size;
  int data = 4;
  delay(500);
  if ((size = Bluetooth.available()) > 0) {
    lights = false;
    Serial.println(data);
    while (size--) {
      if (full == false) {
        bundleIN[i] = Bluetooth.read();
        i++;
        if(i==data) {
          newIN=true;
          i=0;
        }
      }
    }
  }
  if (newIN==true) {
    for(int x=0; x<data; x++) {
     Serial.print(bundleIN[x]);
    }
    if(lights==false){
      numC = bundleIN[2] - '0';
      freqC = bundleIN[3] -'0';
      lights = true;
      newIN = false;
      if(bundleIN[0]=='2'){
        if(bundleIN[1]=='5'){
          LED_wave( PULSE, 6, numC, freqC );
          lights = true;
          newIN = false;
        } else if(bundleIN[1]=='6') {
          LED_wave( CCW, 6, numC, freqC);
          lights = true;
          newIN = false;         
        } else if (bundleIN[1]=='4') {
          for ( jindex = 0; jindex < numC; jindex++ ) {
            digitalWrite(9, HIGH);   
            delay(freqC*100);
            digitalWrite(9, LOW);   
            delay(freqC*25);
            digitalWrite(9, HIGH);   
            delay(freqC*50);
            digitalWrite(9, LOW);
            digitalWrite(6, HIGH);   
            digitalWrite(10, HIGH);
            delay(freqC*100);    
            digitalWrite(10, LOW);
            digitalWrite(6, LOW);   
            digitalWrite(9, HIGH);
            delay(freqC*25);
            digitalWrite(9, LOW);          
            delay(freqC*50);
            digitalWrite(9, HIGH);   
            delay(freqC*50);
            digitalWrite(9, LOW);
            digitalWrite(6, HIGH);   
            digitalWrite(10, HIGH);
            delay(freqC*50);    
            digitalWrite(6, LOW);   
            digitalWrite(10, LOW);
            digitalWrite(5, HIGH);
            digitalWrite(11, HIGH);
            delay(freqC*150);
            digitalWrite(5, LOW);   
            digitalWrite(11, LOW);
            digitalWrite(6, HIGH);
            digitalWrite(10, HIGH);
            delay(freqC*25); 
            digitalWrite(10, LOW);
            digitalWrite(6, LOW);   
            digitalWrite(9, HIGH);
            delay(freqC*25);
            digitalWrite(9, LOW);
            delay(freqC*100);
          }
          lights = true;
          newIN = false;
        } else if (bundleIN[1]=='1') {
          for ( jindex = 0; jindex < numC; jindex++ ) {
            digitalWrite(9, HIGH);   
            delay(freqC*25);
            digitalWrite(9, LOW);   
            delay(freqC*25);
          }
          lights = true;
          newIN = false;
        } else if (bundleIN[1]=='2') {
          for ( jindex = 0; jindex < numC; jindex++ ) {
            digitalWrite(9, HIGH);
            delay(freqC*25);
            digitalWrite(9, LOW);
            digitalWrite(6, HIGH);
            digitalWrite(10, HIGH);
            delay(freqC*25);
            digitalWrite(10, LOW);
            digitalWrite(6, LOW);
            delay(freqC*25);
           }
          lights = true;
          newIN = false;
        } else if (bundleIN[1]=='3') {
          for ( jindex = 0; jindex < numC; jindex++ ) {
            digitalWrite(9, HIGH);
            delay(freqC*25);
            digitalWrite(9, LOW);
            delay(freqC*25);
            digitalWrite(6, HIGH);
            digitalWrite(10, HIGH);
            delay(freqC*25);
            digitalWrite(10, LOW);
            digitalWrite(6, LOW);
            digitalWrite(11, HIGH);
            digitalWrite(5, HIGH);
            delay(freqC*25);
            digitalWrite(5, LOW);
            digitalWrite(11, LOW);
            delay(freqC*25);
          }
          lights = true;
          newIN = false;
        } else {
          lights = true;
          newIN = false;  
        }               
      } else if(bundleIN[0]=='1') {
        buzzC = bundleIN[1] - '0';
        if( buzzC == 7 || buzzC == 8) {
          buzzC=buzzC+3;  
        }
        BUZZ[0] = buzzC;
        LED_wave( BUZZ, 2, numC, freqC);
        lights = true;
        newIN = false;
      } else {
        lights = true;
        newIN = false;      
      }
    }
  }
} 
