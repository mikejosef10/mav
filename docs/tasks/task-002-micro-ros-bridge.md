# TASK-001: Micro-ROS Communication Bridge

## 📝 Beschreibung
Etablierung einer stabilen Kommunikationsschicht zwischen dem ESP32 (Client) und dem ROS 2 Host (Agent). Dies ist das Fundament für alle weiteren Steuerungsbefehle.

## 🎯 Akzeptanzkriterien (Definition of Done)
- [ ] Der ESP32 wird vom `micro-ros-agent` erfolgreich erkannt.
- [ ] Topic `/mav/status/heartbeat` publiziert mit ~1Hz.
- [ ] Die physische LED am ESP32 lässt sich via `ros2 topic pub /mav/cmd/led` schalten.
- [ ] Der Code ist im Git-Repository unter `firmware/bridge_node/` abgelegt.

## ⚙️ Technische Spezifikationen
- **Hardware:** ESP32 DevKitC
- **Protokoll:** XRCE-DDS über Serial (USB)
- **Baudrate:** 115.200
- **ROS 2 Version:** Humble / Iron (Dockerized)

## 📌 Interfaces
| Topic | Nachrichtentyp | Richtung |
|:---|:---|:---|
| `/mav/cmd/led` | `std_msgs/msg/Bool` | Subscriber (In) |
| `/mav/status/heartbeat` | `std_msgs/msg/Header` | Publisher (Out) |

---
Das ist ein vernünftiger Abschluss. Wir haben jetzt ein funktionierendes Fundament, auf dem du später aufbauen kannst. Hier ist die Zusammenfassung und Dokumentation für dein **Task-002: micro-ROS Bridge**.

---

## 📝 Dokumentation: micro-ROS Bridge (Task-002)
[Offizielle Dokumenation](https://micro.ros.org/)
[Video-Tutorial](https://www.youtube.com/watch?v=Nf7HP9y6Ovo)

### 1. Zielsetzung

Einrichtung einer bidirektionalen Kommunikationsbrücke zwischen einem ESP32 (Microcontroller) und einem ROS 2 System (Docker/Host) über eine serielle USB-Verbindung.

### 2. Technische Komponenten

* **Hardware:** ESP32 DevKit V1
* **Framework:** PlatformIO mit der `micro_ros_platformio` Library.
* **ROS 2 Version:** Humble (im Docker-Container).
* **Transport:** Serial (UART) bei **115200 Baud**.

### 3. Implementierte Funktionen

* **Heartbeat Publisher:** Sendet sekündlich einen inkrementierenden Integer auf `/mav/status/heartbeat`.
* **LED Subscriber:** Empfängt `std_msgs/Bool` auf `/mav/cmd/led` und schaltet die interne LED (Pin 2).
* **Auto-Reconnection:** Der ESP32 erkennt den Verlust der Verbindung zum Agenten und versucht selbstständig eine Neuinitialisierung.

---

### 4. Ausführung (How-To)

#### Schritt A: Hardware vorbereiten

1. ESP32 über USB anschließen.
2. Port identifizieren (meist `/dev/ttyUSB0` unter Linux/WSL).

#### Schritt B: ESP32 Flashen

```bash
# Im Projektverzeichnis
pio run --target upload

```

#### Schritt C: micro-ROS Agent starten

Verwende das offizielle Docker-Image, um die Brücke zu schlagen:

```bash
docker run -it --rm \
  -v /dev:/dev \
  --privileged \
  --net=host \
  microros/micro-ros-agent:humble serial --dev /dev/ttyUSB0 -b 115200

```

#### Schritt D: Kommunikation testen (In einem neuen Terminal)

* **Topics auflisten:** `ros2 topic list`
* **Daten empfangen:** `ros2 topic echo /mav/status/heartbeat`
* **LED schalten:** `ros2 topic pub --once /mav/cmd/led std_msgs/msg/Bool "{data: true}"`

---

### 5. Bekannte Schwierigkeiten & Lösungen

* **Handshake-Verzögerung:** Der ESP32 und der Agent brauchen oft 2-3 Anläufe, um die XRCE-DDS Session zu synchronisieren. **Lösung:** Eine robuste `loop()`, die bei Fehlern `fini`-Funktionen aufruft und neu startet.
* **Speicher-Management:** micro-ROS auf Mikrocontrollern ist empfindlich bei der Speicherreservierung. **Lösung:** Der `rclc_executor` wurde explizit auf 2 Handles limitiert.
* **WSL2/Docker USB-Passthrough:** Unter Windows muss das Gerät per `usbipd` aktiv an die WSL-Instanz "attached" werden, damit der Docker-Container darauf zugreifen kann.

---

### 6. Verbesserungspotenziale für später

* **Baudrate erhöhen:** Wechsel auf `460800` oder `921600` für geringere Latenz.
* **Statische IP/WiFi:** Umstieg auf UDP (WLAN), falls das USB-Kabel im Weg ist.
* **Parameter-Server:** Implementierung von ROS-Parametern, um z.B. Blinkfrequenzen zur Laufzeit zu ändern.