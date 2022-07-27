#include <Stepper.h>
#define trigPin 15
#define echoPin 14

//bool fHasLooped = false;

const int stepsPerRevolution = 2048;

const int stepsPRevolution = 0;// change this to fit the number of steps per revolution
// ULN2003 Motor Driver Pins
#define IN1 6
#define IN2 7
#define IN3 8
#define IN4 9

#define IN6 2
#define IN7 3
#define IN8 4
#define IN9 5

// initialize the stepper library
Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);
Stepper myStepper2(stepsPerRevolution, IN6, IN7, IN8, IN9);

void setup() {
Serial.begin (9600);
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);
// set the speed at 5 rpm
  myStepper.setSpeed(10);
   myStepper2.setSpeed(10);
  // initialize the serial port
  Serial.begin(115200);
}

String incomingdata = "";


void loop() {
long duration, distance;
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance = (duration/2) / 29.1;
if (distance < 10) {


Serial.write("detected");
//delay(150);
}



incomingdata = Serial.readString();
if(incomingdata=="Cat")
{ 
  bool fHasLooped = false;
  if ( fHasLooped == false)
    {
  for(int x=0;x<5;x++)
    { 
  
  Serial.print("clockwise");
  myStepper.step(stepsPerRevolution);
  myStepper.step(stepsPRevolution);
  }

  }
  fHasLooped = true;
}

if(incomingdata == "Dog")
{
  bool fHasLooped = false;
if ( fHasLooped == false)
    {
  for(int x=0;x<5;x++)
    { 
  
  Serial.print("clockwise");
  myStepper.step(stepsPerRevolution);
  myStepper.step(stepsPRevolution);
  }

  }
  fHasLooped = true;
}

}
long microsecondsToInches(long microseconds) {
   return microseconds / 74 / 2;
}
