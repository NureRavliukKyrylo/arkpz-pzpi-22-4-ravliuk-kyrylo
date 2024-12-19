#include "WiFiSetup.h"
#include "DataServer.h"
#include "KalmanFilter.h"

const int CONTAINER_ID = 1;
KalmanFilter kalmanFilter;

void setup() {
    Serial.begin(9600);
    connectToWiFi();
}

void loop() {
    float rawDistance = random(10, 100);
    float filteredDistance = kalmanFilter.filter(rawDistance);
    float fillLevel = (100 - filteredDistance) / 100 * 100;

    sendToServer(CONTAINER_ID, fillLevel);

    delay(6000); 
}