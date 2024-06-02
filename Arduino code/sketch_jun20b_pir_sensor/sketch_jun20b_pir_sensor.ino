int pirPin = 2; // PIR Out pin
int pirStat = 0; // PIR status

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(pirPin, INPUT); // Set the PIR pin as input
}

void loop() {
  pir_value(); // Call the function to check PIR sensor value
}

void pir_value() {
  pirStat = digitalRead(pirPin); // Read PIR sensor value

  if (pirStat == HIGH) { // If motion detected
    Serial.println("Theft Alert");
    // digitalWrite(ledPin, HIGH); // Turn on an LED if needed
    delay(500); // Delay to avoid multiple detections
  } else {
    Serial.println("Theft not Alert");
    delay(500); // Delay to avoid multiple detections
    // digitalWrite(ledPin, LOW); // Turn off the LED if needed
  }
}
