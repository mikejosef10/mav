
## 🔌 Energieversorgung & Prototyping

Diese Komponenten bilden das physikalische Rückgrat für deine ersten Hardware-in-the-Loop (HIL) Tests.

| Komponente | Spezifikation / Kapazität | Einsatz im MAV-Projekt |
| --- | --- | --- |
| **Netzteilmodul** | Input: 6.5-12V (DC) / Output: 3.3V oder 5V (umschaltbar) | Versorgung der Schiene am Breadboard für MCU und Sensoren. |
| **830-Point Breadboard** | 830 Kontakte, Standard 2.54mm Pitch | Schneller Aufbau von Testschaltungen ohne Löten. |
| **Jumper Wire Set** | Mix aus M/M, F/M und starren Drähten | Signalverbindung zwischen ESP32/STM32 und Sensorik. |

---

## 🚦 Mensch-Maschine-Schnittstelle (HMI) & Indikatoren

Für einen autonomen Roboter ist visuelles und akustisches Feedback (z. B. ROS-Status-Diagnose) essenziell.

* **LEDs (Bunt & RGB):** * **Spec:** Standard 5mm, ca. 2V Vorwärtsspannung (Farbe beachten), 20mA max.
* **Projekt-Nutzen:** Visualisierung von ROS 2 Zuständen (z. B. Grün = `Active`, Blau = `Wait for Agent`, Rot = `Emergency Stop`). Die **RGB-LED** eignet sich perfekt für Error-Codes via PWM.


* **Summer (Aktiv/Passiv):**
* **Aktiv:** Erzeugt Ton bei konstanter Spannung (Logik-High).
* **Passiv:** Benötigt PWM-Signal zur Tonerzeugung (perfekt zum Testen deiner PWM-Treiber-Klasse).


* **Buttons (Taster):**
* **Spec:** 12x12mm taktile Schalter.
* **Projekt-Nutzen:** Manueller Reset oder "Start Mission" Trigger.



---

## 🧠 Signalverarbeitung & Logik-ICs

Diese Bauteile helfen dir, die Hardware-Abstraktion (HAL) für komplexe Funktionen zu schreiben.

* **74HC595 (8-Bit Shift Register):**
* **Spec:** Serial-In, Parallel-Out. Ermöglicht die Steuerung von 8 Ausgängen über nur 3 Pins.
* **Projekt-Nutzen:** Erweiterung der GPIOs für Status-Displays, falls die Pins am ESP32 knapp werden.


* **4N35 Optokoppler:**
* **Spec:** Galvanische Trennung mittels Licht.
* **Projekt-Nutzen:** Kritisch für die **Not-Aus-Logik**. Er trennt den empfindlichen MCU-Kreis vom (späteren) Lastkreis der Saugmotoren.


* **PN2222 (NPN-Transistoren):**
* **Spec:** Ic max 600mA.
* **Projekt-Nutzen:** Schalten von kleinen Lasten (wie dem aktiven Summer), die den GPIO-Strom des MCUs überschreiten würden.



---

## 🌡 Sensorik (Analog-Inputs)

Ideal zum Testen deiner ADC-Treiber (Analog-to-Digital Converter) in micro-ROS.

* **Fotowiderstand (LDR):** Misst Lichtintensität. Kann für eine einfache "Unter-Möbel-Erkennung" genutzt werden.
* **Thermistor (NTC):** Temperaturabhängiger Widerstand. Ideal für das Monitoring der **Battery-Health** oder MCU-Temperatur (wird in `/battery_state` publiziert).
* **Präzisionspotentiometer:** Zur Simulation von Sensorwerten (z. B. Distanz-Emulation), bevor du einen echten Lidar/Ultraschallsensor hast.

---

## 🛠 Fehlende Komponenten für die "Drive-Unit"

Da dein Ziel ein "Vakuum-Roboter" ist, fällt mir als "Peer" etwas auf: Das Kit ist fantastisch für die Logik, aber für die **Phase 1 (Drive-Unit)** deiner Roadmap fehlen noch zwei entscheidende Dinge:

1. **H-Brücke (Motortreiber):** z. B. ein L298N oder DRV8833, um die tatsächlichen Motoren anzusteuern.
2. **Motoren & Encoder:** Um echtes Feedback für `/odom` (Odometrie) zu generieren.

> **Pro-Tipp für dein C++20 Vorhaben:** Nutze die Widerstände aus dem Kit, um **Pull-Up/Pull-Down** Schaltungen hardwareseitig zu bauen, anstatt dich nur auf interne MCU-Pullups zu verlassen – das erhöht die Signalstabilität für deine ROS 2 Kommunikation massiv.