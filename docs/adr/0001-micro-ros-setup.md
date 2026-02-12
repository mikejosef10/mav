# ADR 0001: Einsatz von Micro-ROS

**Status:** Akzeptiert  
**Datum:** 2026-02-12  
**Beteiligte:** Developer (Du)

## Kontext
Wir benötigen eine robuste Schnittstelle zwischen dem Mikrocontroller (Echtzeit-Hardware-Ebene) und dem Einplatinencomputer (High-Level Logik). Standard-Serial-Protokolle erfordern manuelles Parsing und sind fehleranfällig bei Erweiterungen.

## Entscheidung
Wir nutzen **micro-ROS** über eine serielle USB-Verbindung. 

## Begründung
- **Native Integration:** Der ESP32 erscheint als vollwertiger Node im ROS 2 Graphen.
- **Typensicherheit:** Nutzung standardisierter ROS 2 Messages.
- **Skalierbarkeit:** Einfache Integration weiterer Sensoren/Aktoren ohne Protokolländerung.

## Konsequenzen
- Erhöhter Speicherbedarf auf dem ESP32.
- Komplexeres Build-System (Colcon/Micro-ROS Build Tool) im Vergleich zur Arduino-IDE.