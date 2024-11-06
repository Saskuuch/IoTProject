#define METHANE A1
#define CARBONMON A2
#define AIRQUALITY A3
#define BUTANE A4
// #include <string>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int meth, carb, airq, but;
  meth = analogRead(METHANE);
  carb = analogRead(CARBONMON);
  airq = analogRead(AIRQUALITY);
  but = analogRead(BUTANE);

  String output = "{\"methane\":";
  output += meth;
  output +=  ",\"carbonmonoxide\":";
  output += carb;
  output += ",\"airquality\":";
  output += airq;
  output += ",\"butane\":";
  output += but;
  output += "}";

  Serial.println(output);

  delay(5000);
}
