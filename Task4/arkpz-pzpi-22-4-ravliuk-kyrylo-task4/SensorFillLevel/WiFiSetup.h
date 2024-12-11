#ifndef WIFISETUP_H
#define WIFISETUP_H

#include <ESP8266WiFi.h>

extern const char* WIFI_SSID;      
extern const char* WIFI_PASSWORD;  

void connectToWiFi();

#endif 
