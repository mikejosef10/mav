Link: [ESP32S Dev Kit](https://www.az-delivery.de/en/products/esp32-nodemcu-module-wlan-wifi-dev-kit-c-development-board-mit-cp2102-und-usb-c-anschluss-esp-32-esp32-wroom-32-kompatibel-mit-arduino?_pos=1&_psq=ESP32+NodeMCU+Module+WLAN+WiFi+Dev+Kit+C+Development+Board+mit+CP2102+und+USB-C+Anschluss&_ss=e&_v=1.0&variant=46038922297611)

Kostenloses Ebook: [Ebook](https://www.az-delivery.de/en/products/esp32s-dev-kit-c-v4-nodemcu-wlan-development-board-kompatibel-mit-arduino-nachfolger-modul-von-esp32s-dev-kit-c-v2-1?_pos=1&_psq=ESP32+DEV+Kit+C+V2+ebook&_ss=e&_v=1.0)
## 🧠 Recheneinheit & Speicher (The "Brain")

Für ein Echtzeitsystem wie das MAV ist die Rechenleistung entscheidend, um Odometrie-Daten zu berechnen und gleichzeitig den ROS-Stack zu bedienen.

| Feature | Spezifikation | Relevanz für MAV |
| --- | --- | --- |
| **Prozessor** | Xtensa® Dual-Core 32-bit LX6 | Ermöglicht Multithreading (z.B. Core 0 für micro-ROS, Core 1 für Motor-Regelung). |
| **Taktfrequenz** | Bis zu 240 MHz | Hohe Performance für moderne C++20 Features (Ranges, Lambdas). |
| **SRAM** | 520 KB | Ausreichend Puffer für XRCE-DDS (micro-ROS) Middleware. |
| **Flash** | 4 MB | Genug Platz für umfangreiche Firmware und Log-Daten. |

---

## 🌐 Konnektivität & Kommunikation

Da dein Projekt auf eine verteilte Architektur setzt, bietet der ESP32 hier maximale Flexibilität.

* **USB-Schnittstelle:** USB-C (CP2102 Bridge). Dies ist deine primäre Verbindung zum Raspberry Pi (micro-ROS Agent).
* **WLAN (802.11 b/g/n):** Ermöglicht OTA (Over-the-Air) Updates oder Telemetrie-Streaming ohne Kabel.
* **Bluetooth (v4.2 BR/EDR & BLE):** Optional für eine Smartphone-Fernsteuerung oder Setup-App.
* **Bus-Systeme:**
* **2x I2C:** Für Sensoren (IMU, ToF-Sensoren).
* **3x SPI:** Für SD-Karten-Logging oder High-Speed-Sensoren.
* **3x UART:** Einer belegt durch USB, zwei frei für Peripherie (z.B. Lidar).



---

## ⚙️ I/O & Sensorik-Schnittstellen (Hardware-Abstraktion)

In deiner Hardware-Abstraktionsschicht wirst du diese Pins direkt ansprechen:

* **PWM (MCPWM & LEDC):** Der ESP32 hat spezielle Motor-PWM-Einheiten (MCPWM), die perfekt für die Ansteuerung von H-Brücken (Motoren) geeignet sind.
* **ADC (12-Bit):** 18 Kanäle zur Überwachung der Akkuspannung (via Spannungsteiler aus deinem Kit).
* **Hardware-Encoder:** Der ESP32 besitzt integrierte Puls-Zähler (PCNT), die Encodersignale von Motoren hardwareseitig zählen, ohne die CPU zu belasten – essenziell für präzise Odometrie.
* **GPIOs:** 3.3V Logik-Level (Vorsicht: Nicht 5V tolerant!).

---

## 🛠 Integration in die MAV-Architektur

In deinem ADR (Architecture Decision Record) kannst du diesen ESP32 wie folgt einordnen:

1. **Rolle:** "Low-Level Controller" (Real-Time Actor/Sensor Hub).
2. **Middleware:** Führt den **micro-ROS Client** aus. Nutzt das XRCE-DDS Protokoll über die USB-C serielle Schnittstelle.
3. **Vorteil gegenüber Arduino Uno:** Der ESP32 kann echte **FreeRTOS-Tasks** nutzen. Das erlaubt es dir, die Motorregelung (PID) in einem hochpriorisierten Task laufen zu lassen, während der ROS-Datenaustausch in einem anderen Task stattfindet, ohne das Timing zu stören.

---


**Kleiner Tipp vom "Peer":** Da du das AZDelivery Board hast, achte darauf, dass es im Breadboard oft sehr breit ist (nur eine Lochreihe bleibt auf einer Seite frei). Nutze am besten zwei Breadboards nebeneinander oder Jumperkabel von unten, um Platz für deine Sensoren zu haben.