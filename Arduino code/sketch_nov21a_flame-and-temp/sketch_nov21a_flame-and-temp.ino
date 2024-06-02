#include <dht.h>
#define dht_apin A0 // Analog Pin sensor is connected to temp sensor
const int buzzer = 9; // Buzzer to Arduino pin 9
dht DHT;
int flame_sensor = A11; // Analog pin for flame sensor
int flame_detected;
int datafromUser;

void setup() {
  Serial.begin(9600);
  pinMode(dht_apin, INPUT);
  pinMode(buzzer, OUTPUT); // Set buzzer pin as output
}

void loop() {
  temperature_value();
  flame_value();  

  if (Serial.available() > 0) {
    datafromUser = Serial.read();
  }

  if (datafromUser == '1') {
    tone(buzzer, 1000); // Turn on buzzer with frequency 1KHz
    delay(1000);
  } else if (datafromUser == '0') {
    noTone(buzzer); // Turn off buzzer
    delay(1000);
  }
}

void temperature_value() {
  DHT.read11(dht_apin);
  Serial.print("Temperature: ");
  Serial.print(DHT.temperature); 
  Serial.println("°C");
  delay(1000); // Delay before accessing sensor again
}

void flame_value() {
  flame_detected = digitalRead(flame_sensor);
  if (flame_detected == LOW) {
    Serial.println("FIRE ALERT");
  } else {
    Serial.println("FIRE not ALERT");
  }
  delay(1000);
}
