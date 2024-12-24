#include "WiFiSetup.h"

// Variables to store WiFi SSID and password
String wifiSSID;
String wifiPassword;

void connectToWiFi() {
    // Prompt the user to enter WiFi SSID
    Serial.println("Enter WiFi SSID:");
    
    // Wait for user input of WiFi SSID
    while (wifiSSID.isEmpty()) {
        if (Serial.available()) {
            // Read the SSID entered by the user until a newline character
            wifiSSID = Serial.readStringUntil('\n');
            wifiSSID.trim(); 
        }
    }

    // Prompt the user to enter WiFi password
    Serial.println("Enter WiFi Password (leave empty for no password):");
    
    while (true) {
        if (Serial.available()) {
            // Read the password entered by the user until a newline character
            wifiPassword = Serial.readStringUntil('\n');
            wifiPassword.trim(); 

            // If the password is empty, allow connection without password
            if (wifiPassword.length() == 0) {
                Serial.println("WiFi Password is empty, connecting without password...");
                break; 
            }
        }
    }

    // Display the SSID the program will connect to
    Serial.print("Connecting to WiFi: ");
    Serial.println(wifiSSID);
    
    // Try connecting to the WiFi network
    if (wifiPassword.isEmpty()) {
        WiFi.begin(wifiSSID.c_str());
    } else {
        WiFi.begin(wifiSSID.c_str(), wifiPassword.c_str());
    }

    // Wait for WiFi connection
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);  
        Serial.print(".");  
    }

    // Once connected, print success message and display the IP address
    Serial.println("\nConnected to WiFi");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
}
