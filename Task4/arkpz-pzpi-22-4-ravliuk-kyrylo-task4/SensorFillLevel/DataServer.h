#ifndef DATASENDER_H
#define DATASENDER_H

#include <HTTPClient.h>
#include <ArduinoJson.h>

void sendToServer(int sensorId, float fillLevel);

#endif 
