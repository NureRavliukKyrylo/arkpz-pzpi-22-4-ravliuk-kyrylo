#ifndef DATASENDER_H
#define DATASENDER_H

#include <HTTPClient.h>
#include <ArduinoJson.h>

void sendToServer(String API_SERVER_BASE_URL, int containerIdFilling, float fillLevel);

#endif 
