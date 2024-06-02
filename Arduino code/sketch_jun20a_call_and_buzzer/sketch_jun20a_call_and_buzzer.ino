#include <SoftwareSerial.h>

SoftwareSerial mySerial(11, 10);

#define playTime 8000
#define PLAY_E 6 // pin 3 is used for playback-edge trigger

int datafromUser = 0;
const int buzzer = 9; // Buzzer connected to Arduino pin 9

void setup() {
  pinMode(PLAY_E, OUTPUT); // Set the PLAY_E pin as output
  mySerial.begin(9600);
  Serial.begin(9600); // Set up Serial monitor
  pinMode(buzzer, OUTPUT); // Set buzzer pin as output    
}

void loop() {
  datafromUser = 0; // Reset datafromUser variable in each loop iteration

  if (Serial.available() > 0) {
    datafromUser = Serial.read(); // Read input from the serial monitor
  }

  if (datafromUser == '1') {
    tone(buzzer, 1000); // Send 1KHz sound signal to buzzer
    delay(1000); // Tone duration
    call_function();
  } else if (datafromUser == '0') {
    noTone(buzzer); // Stop buzzer sound
    delay(1000); // Delay after stopping buzzer
  }
}

void call_function() {
  mySerial.println("ATD+923491268829;"); // Make a call to the specified number
  delay(5000); // Wait for call connection
  for (int i = 0; i <= 3; i++) {
    digitalWrite(PLAY_E, HIGH); // Trigger playback
    delay(50); // Delay before setting PLAY_E low
    digitalWrite(PLAY_E, LOW); // End playback
    delay(playTime); // Playback duration
  }
  mySerial.println("ATH"); // End the call
}
