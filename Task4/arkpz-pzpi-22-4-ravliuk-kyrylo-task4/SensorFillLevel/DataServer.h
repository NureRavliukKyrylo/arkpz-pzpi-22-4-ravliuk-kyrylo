#ifndef DATASENDER_H
#define DATASENDER_H

#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

void sendToServer(int sensorId, float fillLevel);

#endif 
