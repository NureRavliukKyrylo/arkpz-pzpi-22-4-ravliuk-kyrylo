#include <Adafruit_SSD1306.h>
#include "WiFiSetup.h"
#include "DataServer.h"
#include "KalmanFilter.h"

// Pin assignments for the ultrasonic sensor
const int TRIG_PIN = 4;
const int ECHO_PIN = 5;

// Pin assignments for the LEDs
const int RED_LED = 18;
const int YELLOW_LED = 19;
const int GREEN_LED = 21;

// Container information
const int CONTAINER_ID = 1;
const int MAX_DISTANCE_CM = 100;

KalmanFilter kalmanFilter;

void setup() {
    Serial.begin(9600);

    // Configuration sensor pins
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    pinMode(RED_LED, OUTPUT);
    pinMode(YELLOW_LED, OUTPUT);
    pinMode(GREEN_LED, OUTPUT);

    // Connect to the WiFi network
    connectToWiFi();
}

// Measures the distance using the ultrasonic sensor
float measureDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    // Measure the duration of the echo signal
    long duration = pulseIn(ECHO_PIN, HIGH, 30000);
    if (duration == 0) {
        return MAX_DISTANCE_CM;
    }
    float distance = (duration * 0.034) / 2;
    return distance;
}

// Updates the LED indicators based on the fill level
void updateLEDs(float fillLevel) {
    if (fillLevel < 30) {
        digitalWrite(RED_LED, LOW);
        digitalWrite(YELLOW_LED, LOW);
        digitalWrite(GREEN_LED, HIGH);
    } else if (fillLevel >= 30 && fillLevel < 90) {
        digitalWrite(RED_LED, LOW);
        digitalWrite(YELLOW_LED, HIGH);
        digitalWrite(GREEN_LED, LOW);
    } else {
        digitalWrite(RED_LED, HIGH);
        digitalWrite(YELLOW_LED, LOW);
        digitalWrite(GREEN_LED, LOW);
    }
}

void loop() {
    // Measure the distance from the ultrasonic sensor
    float distance = measureDistance();

    // Apply Kalman filter to smooth the measured distance
    float filteredDistance = kalmanFilter.filter(distance);

    // Calculate the fill level as a percentage
    float fillLevel = (100 - filteredDistance) / MAX_DISTANCE_CM * 100;
    fillLevel = constrain(fillLevel, 0, 100);

    Serial.print("Measured Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    Serial.print("Fill Level: ");
    Serial.print(fillLevel);
    Serial.println(" %");

    // Send the fill level and container ID to the server
    sendToServer(CONTAINER_ID, fillLevel);

    // Update the LED indicators based on the fill level
    updateLEDs(fillLevel);

    delay(2000);
}
