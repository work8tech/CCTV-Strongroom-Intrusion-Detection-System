// Pin Definitions
const int pirPin = 2;       // PIR Sensor connected to digital pin 2

// Timing Variables
unsigned long detectionTime = 0;  // Stores the time when motion was detected
const unsigned long delayPeriod = 60000;  // 60 seconds in milliseconds

// State Flag
bool personDetected = false;

void setup() {
  pinMode(pirPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  int pirState = digitalRead(pirPin);

  if (pirState == HIGH && !personDetected) {
    // Motion detected and currently not in detection state
    Serial.println("Person Detected");
    personDetected = true;
    detectionTime = millis();  // Start 60-second timer
  }

  if (personDetected) {
    // Stay in detection state for 60 seconds
    if (millis() - detectionTime >= delayPeriod) {
      personDetected = false;  // Reset detection state
    }
  }
}
