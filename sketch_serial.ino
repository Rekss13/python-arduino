#define PIN_10 10
#define PIN_11 11
void setup() {
  pinMode(PIN_10, OUTPUT);
  pinMode(PIN_10, OUTPUT);
  Serial.begin(9600);
  digitalWrite(PIN_10, LOW);
  digitalWrite(PIN_11, HIGH);  
}
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
  }
}
