#include "DataServer.h"
#include <WiFi.h>

// Base URL for the API server
const String API_SERVER_BASE_URL = "http://rnlmj-91-146-250-0.a.free.pinggy.link/api/iotFillingContainers/";

/**
 * Sends container filling data to the server via HTTP POST request.
 *
 * @param containerIdFilling The ID of the container being filled.
 * @param sensorValue The sensor value indicating the container's fill level.
 */

void sendToServer(int containerIdFilling, float sensorValue) {
  // Check if the WiFi connection is active
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;

    // Begin the HTTP request to the server
    String url = API_SERVER_BASE_URL;
    http.begin(client, url);

    // Add the "Content-Type" header to specify JSON data
    http.addHeader("Content-Type", "application/json");

    // Create a JSON document for the payload
    StaticJsonDocument<200> doc;
    doc["container_id_filling"] = containerIdFilling;
    doc["sensor_value"] = sensorValue;

    // Serialize the JSON document into a string
    String payload;
    serializeJson(doc, payload);

    // Send the POST request and capture the HTTP response code
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
