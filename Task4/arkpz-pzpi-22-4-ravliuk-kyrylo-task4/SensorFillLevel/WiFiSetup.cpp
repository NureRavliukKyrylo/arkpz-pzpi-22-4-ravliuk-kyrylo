#include "WiFiSetup.h"

const char* WIFI_SSID = "";
const char* WIFI_PASSWORD = "";

void connectToWiFi() {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
}
