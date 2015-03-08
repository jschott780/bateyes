
/*  
  sends ping output to xbee

  The circuit: 
  * RX is digital pin 2 (connect to TX of XBee)
  * TX is digital pin 3 (connect to RX of XBee)
  * PING is digital pin 7
  
*/
#include <SoftwareSerial.h>

int XBEE_RX = 2;
int XBEE_TX = 3;
int PING = 4;

SoftwareSerial xbee(XBEE_RX, XBEE_TX);

void setup()  {
   Serial.println( "starting arduino sensors..." );
   Serial.begin(9600);
   xbee.begin( 9600 );
   Serial.println( "startup complete. waiting for data..." );
}

void loop()  {
  // establish variables for duration of the ping, 
  // and the distance result in inches and centimeters:
  long duration, inches, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(PING, OUTPUT);
  digitalWrite(PING, LOW);
  delayMicroseconds(2);
  digitalWrite(PING, HIGH);
  delayMicroseconds(5);
  digitalWrite(PING, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(PING, INPUT);
  duration = pulseIn(PING, HIGH);
  
  String outPacket = "{\"ping\": \"" + String(duration) + "\"}";
  
  // send the message
  Serial.println(outPacket);
  xbee.print( outPacket );
  
  delay( 1000 );
}




