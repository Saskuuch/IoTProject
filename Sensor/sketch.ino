#define METHANE A1
#define CARBONMON A2
#define AIRQUALITY A3
#define BUTANE A4
#include <WiFiNINA.h>
#include <WiFiSSLClient.h>
#include <Arduino_JSON.h>
#include <LiquidCrystal.h>
const int rs = 2;
const int en = 3;
const int d4 = 6;
const int d5 = 7;
const int d6 = 8;
const int d7 = 9;

#define BUZZER_PIN 9

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

const char* googleApiKey = "AIzaSyBhtNkbQ5YXhmec7bhffRRaONVgl6g76mA";
#define SECRET_SSID "KarenNurlybekovIphone"
#define SECRET_PASS "Qwe12345"
char server[] = "www.googleapis.com";             // Geolocation server
WiFiSSLClient client;

const int loadResistor = 10;   // Load resistor value in kilo-ohms
String latitude, longitude = "";
// Baseline resistance values for each sensor
float R_0_methane = 0.0;
float R_0_carbonmon = 0.0;
float R_0_airquality = 0.8;
float R_0_butane = 0.1;
// Constants for each sensor (curve and constant values from datasheets)
float sensorCurve_methane = 0.3, gasConstant_methane = -0.38;    // MQ4: Methane
float sensorCurve_carbonmon = 0.4, gasConstant_carbonmon = -0.45; // MQ7: Carbon Monoxide
float sensorCurve_airquality = 0.35, gasConstant_airquality = -0.47; // MQ135: NH3
float sensorCurve_butane = 0.5, gasConstant_butane = -0.46;    // MQ6: Butane

char serverflask[] = "flasktest-f0ctd4emdsgkffea.canadacentral-01.azurewebsites.net";

void setup() {
  Serial.begin(9600);

  delay(2000);
  lcd.begin(16, 2);

  Serial.println("Starting sensor calibration...");
delay(1000);
  // Run calibration in clean air for each sensor
  R_0_methane = calibrateSensor(METHANE, 10);
  R_0_carbonmon = calibrateSensor(CARBONMON, 10);
  R_0_airquality = calibrateSensor(AIRQUALITY, 10);
  R_0_butane = calibrateSensor(BUTANE, 10);

  // Print calibration results
  Serial.print("MQ4 (Methane) Calibration completed. R_0 = ");
  Serial.print(R_0_methane);
  Serial.println(" kOhms");

  Serial.print("MQ7 (Carbon Monoxide) Calibration completed. R_0 = ");
  Serial.print(R_0_carbonmon);
  Serial.println(" kOhms");

  Serial.print("MQ135 (Air Quality) Calibration completed. R_0 = ");
  Serial.print(R_0_airquality);
  Serial.println(" kOhms");

  Serial.print("MQ6 (Butane) Calibration completed. R_0 = ");
  Serial.print(R_0_butane);
  Serial.println(" kOhms");

  // Connect to WiFi with timeout
  Serial.println("Connecting to WiFi...");
  unsigned long startAttemptTime = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) { // 10 seconds timeout
    WiFi.begin(SECRET_SSID, SECRET_PASS);
    delay(1000);
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected to WiFi");
  } else {
    Serial.println("Failed to connect to WiFi. Proceeding without connection.");
  }

  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW); // Ensure the buzzer is off at startup
}

void loop() {
 if (WiFi.status() == WL_CONNECTED) {
    // Get sensor and geolocation data
    String sensorData = readSensorData();      // Get sensor values
    //String locationData = fetchGeolocation();   // Get latitude and longitude
    Serial.println(sensorData);
    lcd.setCursor(0,0);
    lcd.print("sensorData");
    // Combine them into a single JSON object
    //String jsonData = "{" + sensorData + "," + locationData + "}";

    // Print or send jsonData to the server
    //Serial.println("Combined JSON Data: " + jsonData);

    // Send data to Flask server
    //sendDataToFlask(jsonData);
  } else{
    reconnectWiFi();
  }
  lcd.clear();
  delay(1000); // Wait before the next loop
}

void reconnectWiFi() {
  Serial.println("Reconnecting to WiFi...");
  WiFi.begin(SECRET_SSID, SECRET_PASS);
  unsigned long startAttemptTime = millis();

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Reconnected to WiFi.");
  } else {
    Serial.println("Failed to reconnect.");
  }
}

String fetchGeolocation() {
  Serial.println("Connecting to Google Geolocation server...");
  if (client.connect(server, 443)) {
    Serial.println("Connected to the server!");
    
    String payload = "{\"wifiAccessPoints\": []}";

    // Send HTTP POST request
    client.println("POST /geolocation/v1/geolocate?key=" + String(googleApiKey) + " HTTP/1.1");
    client.println("Host: www.googleapis.com");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(payload.length());
    client.println("Connection: close");
    client.println();
    client.println(payload);

    // Collect response
    String response = "";
    unsigned long startTime = millis();
    while ((client.connected() || client.available()) && (millis() - startTime < 5000)) {
      if (client.available()) {
        response += client.readString();
      }
    }
    client.stop();

    int latIndex = response.indexOf("\"lat\":");
  int lngIndex = response.indexOf("\"lng\":");
  if (latIndex != -1 && lngIndex != -1) {
    String latitude = response.substring(latIndex + 6, response.indexOf(",", latIndex));
    String longitude = response.substring(lngIndex + 6, response.indexOf("\n", lngIndex));

    // Return latitude and longitude as a simple comma-separated string
    return "\"latitude\":" + latitude + ",\"longitude\":" + longitude;
  } else {
    Serial.println("Latitude and Longitude not found in response.");
    return "\"latitude\":\"\",\"longitude\":\"\"";
  }
  }
}



String readSensorData() {
  // Collect and return the JSON data string (reuse your JSON formatting block here)
  // For example:
  float ppm_methane = calculatePPM(METHANE, R_0_methane, sensorCurve_methane, gasConstant_methane);
  float ppm_carbonmon = calculatePPM(CARBONMON, R_0_carbonmon, sensorCurve_carbonmon, gasConstant_carbonmon);
  float ppm_airquality = calculatePPM(AIRQUALITY, R_0_airquality, sensorCurve_airquality, gasConstant_airquality);
  float ppm_butane = calculatePPM(BUTANE, R_0_butane, sensorCurve_butane, gasConstant_butane);

  return "\"methane\":" + String(ppm_methane, 2) +
         ",\"carbonmonoxide\":" + String(ppm_carbonmon, 2) +
         ",\"airquality\":" + String(ppm_airquality, 2) +
         ",\"butane\":" + String(ppm_butane, 2);
}

void sendDataToFlask(String jsonData) {
  Serial.println("Connecting to Flask server...");
  if (client.connect(serverflask, 443)) {
    // Construct HTTP request headers
    client.println("POST /receive_data HTTP/1.1");
    client.println("Host: " + String(serverflask));
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonData.length());
    client.println();
    client.println(jsonData);

    // Read the server response
    unsigned long timeout = millis();
    while (client.connected() || client.available()) {
      if (millis() - timeout > 5000) break; // Timeout after 5 seconds
      if (client.available()) {
        char c = client.read();
        Serial.print(c);
      }
    }
    client.stop(); // Close connection after sending data
    Serial.println("\nData sent and connection closed.");
  } else {
    Serial.println("Connection to Flask server failed");
  }
}


void requestDataFromFlask() {
  Serial.println("Connecting to Flask server...");
  if (client.connect(serverflask, 443)) { // Use 80 for HTTP or 443 for HTTPS
    // Construct HTTP GET request
    client.println("GET /receive_alert HTTP/1.1");
    client.println("Host: " + String(serverflask));
    client.println("Connection: close");
    client.println();

    Serial.println("GET request sent to Flask server.");

    // Wait for server response
    unsigned long timeout = millis();
    while (!client.available()) {
      if (millis() - timeout > 5000) {
        Serial.println(">>> Client Timeout !");
        client.stop();
        return;
      }
    }

    // Read status line
    String status_line = client.readStringUntil('\n');
    Serial.println("Status line: " + status_line);

    // Read headers
    String line = "";
    while (client.available()) {
      line = client.readStringUntil('\n');
      if (line == "\r" || line.length() == 1) {
        // Headers ended
        break;
      }
      Serial.println("Header: " + line);
    }

    // Read the body
    String response = "";
    while (client.available()) {
      response += client.readStringUntil('\n');
    }

    Serial.println("Server response: " + response);

    // Process the response
    response.trim(); // Remove any leading/trailing whitespace

    if (response == "alert") {
      // Activate buzzer
      digitalWrite(BUZZER_PIN, HIGH);
      Serial.println("Alert received. Buzzer activated.");
    } else if (response == "normal") {
      // Deactivate buzzer
      digitalWrite(BUZZER_PIN, LOW);
      Serial.println("Normal received. Buzzer deactivated.");
    } else {
      Serial.println("Unknown response.");
    }

    client.stop(); // Close connection after receiving data
    Serial.println("Connection closed.");
  } else {
    Serial.println("Connection to Flask server failed");
  }
}


float calibrateSensor(int sensorPin, int duration) {
  unsigned long startTime = millis();
  int readingsCount = 0;
  float sumR_s = 0.0;

  while (millis() - startTime < duration * 1000) {
    int sensorValue = analogRead(sensorPin);
    float sensorVoltage = (sensorValue / 1023.0) * 5.0;
    float R_s = loadResistor * (5.0 - sensorVoltage) / sensorVoltage;
    sumR_s += R_s;
    readingsCount++;
    delay(10000);  // Take a reading every second
  }
  
  return sumR_s / readingsCount;  // Return the average R_s as R_0
}

float calculatePPM(int sensorPin, float R_0, float sensorCurve, float gasConstant) {
  int sensorValue = analogRead(sensorPin);
  float sensorVoltage = (sensorValue / 1023.0) * 5.0;
  float R_s = loadResistor * (5.0 - sensorVoltage) / sensorVoltage;
  float ratio = R_s / R_0;
  return pow(10, (log10(ratio) - sensorCurve) / gasConstant);  // Convert ratio to ppm
}
