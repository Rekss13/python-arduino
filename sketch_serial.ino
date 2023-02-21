#define PIN_13 13
const unsigned long SHORT_LAG = 20000;
const unsigned long LONG_LAG = 60000;
unsigned long previousMillis = 0;
unsigned long previousMillisError = 0;
unsigned long lag;
unsigned long lagError;
long delta;
bool isStop;

void setup() {
  digitalWrite(PIN_13, OUTPUT);
  Serial.begin(9600);
  setStart();  
}

void setStart() {
  lag = LONG_LAG;
  lagError = LONG_LAG * 2;
  previousMillis = millis();
  previousMillisError = millis();
  digitalWrite(PIN_13, LOW);
  isStop = false;
}

void setError() {
  digitalWrite(PIN_13, HIGH);
  delay(10000);
  setStart();
}

void loop() {
  unsigned long currentMillis = millis();
  if (!isStop && currentMillis - previousMillis >= lag) {   
    previousMillis = currentMillis;
    Serial.println("getState");
  }
  if (!isStop && currentMillis - previousMillisError >= lagError) {   
    previousMillisError = currentMillis;
    Serial.println("error");
    setError();
  }
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data == "start" || data == "work") {
      lag = SHORT_LAG;
      lagError = LONG_LAG;
      previousMillisError = currentMillis;
    } else if (data == "restart") {
      setStart();
    } else if (data == "stop") {
      isStop = true;
    } else if (data == "error") {
      setError();
    }
    Serial.print("You send me: ");
    Serial.println(data);
  } 
}
