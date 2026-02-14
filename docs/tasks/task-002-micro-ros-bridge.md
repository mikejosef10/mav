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