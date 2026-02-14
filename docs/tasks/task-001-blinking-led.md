# Task 001: Blinking LED & Toolchain Validation

## 📝 Übersicht

Dieses Ticket markiert den "Hello World"-Meilenstein für die **MAV Drive Unit**. Ziel war es nicht nur, eine LED zum Leuchten zu bringen, sondern die gesamte Entwicklungsumgebung (Windows -> WSL -> ESP32) sowie die modulare C++ Struktur zu validieren.

**Status:** ✅ Abgeschlossen

**Komponente:** `firmware/drive_unit`

**Hardware:** ESP32 DevKitC

---

## 🎯 Lernziele & Anforderungen

* **Toolchain-Check:** Funktioniert der USB-Durchgriff von Windows zu WSL via `usbipd`?
* **Build-System:** Kompiliert PlatformIO innerhalb der Docker/WSL-Umgebung korrekt?
* **Hardware-Abstraktion:** Anwendung des "Clean Code"-Prinzips durch Kapselung der LED-Logik in einer Klasse (statt nackter `digitalWrite`-Aufrufe).

---

## 🛠 Implementierungsdetails

### 1. Hardware-Anbindung (Windows Host)

Da die Entwicklung in der WSL-Umgebung stattfindet, muss die serielle Schnittstelle des ESP32 vom Windows-Host an WSL "durchgereicht" werden. Dafür wurde ein Helper-Script erstellt:

**Datei:** `firmware/drive_unit/helper_scripts/esp_attach.bat`

> Dieses Skript automatisiert das Identifizieren der `VID:PID` und das Binden des Geräts an die WSL-Instanz.

### 2. Software-Architektur (Firmware)

Entsprechend der Projektphilosophie wurde die LED-Logik in eine eigene Library ausgelagert.

#### Die `StatusLed` Klasse

Anstatt Pins global zu definieren, kapselt `StatusLed` die Hardware-Details. Dies ermöglicht es, später die LED-Logik (z.B. für Blink-Muster oder PWM-Dimmen) zu erweitern, ohne den `main.cpp` Code anzupassen.

```cpp
// StatusLed.hpp
class StatusLed {
public:
    explicit StatusLed(int pin) : _pin(pin) {}
    void begin() { 
        pinMode(_pin, OUTPUT); 
    }
    void on() { digitalWrite(_pin, HIGH); }
    void off() { digitalWrite(_pin, LOW); }
private:
    int _pin;
};

```

#### Main Logic

Die `main.cpp` nutzt die Klasse und bietet über den Seriellen Monitor (115200 Baud) Telemetrie-Daten an, um den Status der Drive Unit zu überwachen.

---

## 💡 Begründungen & Entscheidungen (ADR-Light)

* **Warum eine Klasse für eine einfache LED?** Im Sinne des Projekts ("Software läuft isoliert von Hardware") verhindern wir so, dass Hardware-spezifische Arduino-Befehle überall im Code verteilt sind. Die `main.cpp` weiß nur, dass es ein Objekt gibt, das `on()` oder `off()` kann.
* **Warum `usbipd`?** Es ermöglicht eine nahtlose Integration in die Linux-basierte ROS 2 Toolchain, während die gewohnte Windows-Oberfläche für die Entwicklung genutzt werden kann.
* **Code-Kommentar (LED AUS):** Im aktuellen Stand ist der "Aus"-Teil auskommentiert, um ein dauerhaftes Leuchten zur ersten Validierung der Stromversorgung und des Pin-Mappings zu erzwingen.

---

## 🏁 Verifizierung

1. **Build:** `pio run` via Terminal erfolgreich.
2. **Upload:** `esp_attach.bat` ausgeführt -> `pio run -t upload` erfolgreich.
3. **Funktion:** Die onboard LED (Pin 2) leuchtet dauerhaft.
4. **Telemetrie:** Serial Monitor zeigt korrekt "MAV Drive Unit gestartet..." an.

---

## ⏭ Nächste Schritte

Nachdem die Hardware-Basis steht, werden wir in **Task 002** die Brücke zu ROS 2 schlagen:

* Einrichtung des micro-ROS Agents.
* Erstellen eines Publishers, der den LED-Status als `std_msgs/Bool` an den ROS-Graph sendet.