#include <Servo.h>
Servo myservo; 
String inByte;
int pos;

void setup() {

  Serial.begin(9600);
  myservo.attach(8);
  myservo.write(0);
}

void loop()
{    
  if(Serial.available())  // if data available in serial port
    { 
    inByte = Serial.readStringUntil('\n'); // read data until newline

    if(inByte == "open") {
      Serial.print(inByte);
      delay(300);
      for(pos=0; pos<=90; pos+=5) {
        myservo.write(pos);
        delay(20);
      }
      delay(5000);
      for(pos=90; pos>=0; pos-=5) {
        myservo.write(pos);
        delay(20);
      }

      inByte = "";

      
    }

    }
}
