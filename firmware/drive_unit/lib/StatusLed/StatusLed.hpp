// src/drive_unit/lib/StatusLed/StatusLed.hpp
#pragma once
#include <Arduino.h>

class StatusLed {
public:
    explicit StatusLed(int pin) : _pin(pin) {}

    void begin() {
        pinMode(_pin, OUTPUT);
        digitalWrite(_pin, LOW);
    }

    void on() { digitalWrite(_pin, HIGH); }
    void off() { digitalWrite(_pin, LOW); }

private:
    int _pin;
};