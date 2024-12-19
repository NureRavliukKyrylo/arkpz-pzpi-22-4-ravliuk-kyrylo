#include "DataServer.h"
#include <WiFi.h>

const String API_SERVER_BASE_URL = "http://rnlmj-91-146-250-0.a.free.pinggy.link/api/iotFillingContainers/";

void sendToServer(int containerIdFilling, float sensorValue) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;

    String url = API_SERVER_BASE_URL;
    http.begin(client, url);

    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    doc["container_id_filling"] = containerIdFilling;
    doc["sensor_value"] = sensorValue;

    String payload;
    serializeJson(doc, payload);

    Serial.println("\nSending POST to server...");
    Serial.print("Request Body: ");
    Serial.println(payload);

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      Serial.print("HTTP code response: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("Response server:");
      Serial.println(response);
    } else {
      Serial.print("Error of HTTP: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi is not connected");
  }
}
