#include "WiFiSetup.h"
#include "DataServer.h"

const int SENSOR_ID = 11;

void setup() {
    Serial.begin(9600);
    connectToWiFi();
}

void loop() {
    float fillLevel = random(10, 100);

    sendToServer(SENSOR_ID, fillLevel);

    delay(60000); 
}