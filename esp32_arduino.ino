/*
  ESP32 DHT11 to Flask API
  This code reads temperature and humidity from a DHT11 sensor 
  and sends it to the Flask server via HTTP POST.
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// --- Configuration ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_COMPUTER_IP:5000/sensor"; // Replace with your Flask server IP

#define DHTPIN 4          // GPIO pin where DHT11 is connected
#define DHTTYPE DHT11     // DHT 11
DHT dht(DHTPIN, DHTTYPE);

const char* deviceId = "ESP32_REAL_DEVICE_01";

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Prepare JSON payload
    StaticJsonDocument<200> doc;
    doc["device_id"] = deviceId;
    doc["ip_address"] = WiFi.localIP().toString();
    doc["temp"] = t;
    doc["humd"] = h;

    String jsonPayload;
    serializeJson(doc, jsonPayload);

    Serial.print("Sending: ");
    Serial.println(jsonPayload);

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  delay(2000); // Send data every 2 seconds
}
