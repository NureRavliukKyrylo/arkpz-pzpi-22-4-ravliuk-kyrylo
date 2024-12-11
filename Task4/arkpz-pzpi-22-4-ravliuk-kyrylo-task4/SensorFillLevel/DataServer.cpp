#include "DataServer.h"
#include <ESP8266WiFi.h>

const String API_SERVER_BASE_URL = "http://127.0.0.1:8000";

void sendToServer(int sensorId, float fillLevel) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        WiFiClient client;

        String url = API_SERVER_BASE_URL + String(sensorId) + "/sensor-value-update/";
        http.begin(client, url);

        http.addHeader("Content-Type", "application/json");

        StaticJsonDocument<200> doc;
        doc["sensor_value"] = fillLevel;

        String payload;
        serializeJson(doc, payload);

        int httpResponseCode = http.sendRequest("PATCH", payload);

        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println("Data sent successfully. Response: " + response);
        } else {
            Serial.println("Error sending data: " + String(httpResponseCode));
        }

        http.end();
    } else {
        Serial.println("WiFi not connected");
    }
}
