#include "Wire.h" //allows communication over i2c devices

const int pressureInput = A0; //select the analog input pin for the pressure transducer
const int pressureZero = 199; //analog reading of pressure transducer at 0psi
const int pressureMax = 1000; //analog reading of pressure transducer at 100psi
const int pressuretransducermaxPSI = 500; //psi value of transducer being used
const int baudRate = 9600; //constant integer to set the baud rate for serial monitor
const int sensorreadDelay = 250; //constant integer to set the sensor read delay in milliseconds

float pressureValue = 0; //variable to store the value coming from the pressure transducer


void setup() //setup routine, runs once when system turned on or reset
{
  Serial.begin(baudRate); //initializes serial communication at set baud rate bits per second
}

void loop() //loop routine runs over and over again forever
{
  pressureValue = analogRead(pressureInput); //reads value from input pin and assigns to variable
  Serial.print("Raw: "); //prints value from previous line to serial
  Serial.print(pressureValue); //prints value from previous line to serial
  pressureValue = ((pressureValue-pressureZero)*pressuretransducermaxPSI)/(pressureMax-pressureZero); //conversion equation to convert analog reading to psi
  Serial.print("Pressure:"); //prints label
  Serial.print(pressureValue, 1); //prints value from previous line to serial
  Serial.println("psi"); //prints label to serial
  delay(sensorreadDelay); //delay in milliseconds between read values
}
