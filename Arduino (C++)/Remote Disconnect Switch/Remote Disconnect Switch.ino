#define dirPin D4
#define stepPin D5
#define stepsPerRevolution 200

//Number of rotations - change here
#define desiredRotations 20
#define switchPressed D1
#define switchLogicPower D2



//limit switch wiring:
//Red wire on ground
//Green wire on D1
//Black wire on D2

//Please make sure there isn't a floating ground!
//Use pullup resistors to prevent this from happening (again)



void setup() {
  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(switchLogicPower, OUTPUT);
  digitalWrite(switchLogicPower, HIGH);
  Serial.begin(9600);
}

void loop() {
  Serial.write("switchPressed = ");

  

  if (digitalRead(switchPressed) == HIGH) {
    Serial.write("HIGH");
    Serial.println();
    // Set the spinning direction counter-clockwise:
    digitalWrite(dirPin, HIGH);

    // Spin the stepper motor 5 revolutions slow:
    for (int i = 0; i < desiredRotations * stepsPerRevolution; i++) {
      yield();
      // These four lines result in 1 step:
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(500);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(500);
    }
  }
  else {
    Serial.write("LOW");
    Serial.println();
  }

  delay(100);
  yield();


}