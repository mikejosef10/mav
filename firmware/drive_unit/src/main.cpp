// src/drive_unit/src/main.cpp
#include <Arduino.h>
#include <StatusLed.hpp>

// Wir nutzen Pin 2 (G2) für deine LED
StatusLed statusLed(2);

void setup() {
    // Initialisiere die LED
    statusLed.begin();
    
    // Serielle Kommunikation für Debugging
    Serial.begin(115200);
    Serial.println("MAV Drive Unit gestartet...");
}

void loop() {
    statusLed.on();
    Serial.println("LED AN");
    delay(1000);

    /*statusLed.off();
    Serial.println("LED AUS");
    delay(1000);*/
}