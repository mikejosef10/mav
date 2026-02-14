# Projekt: "Mini-Auto" Vakuum-Plattform (MAV)

## 📝 Projektübersicht

Das Ziel dieses Projekts ist die Entwicklung eines modularen, autonomen Roboterstaubsaugers, der nach den Software-Standards moderner autonomer Fahrzeuge (AV) entwickelt wird. Anstatt eines monolithischen Systems wird eine **verteilte Architektur** genutzt, die Skalierbarkeit für spätere Erweiterungen (Lidar, SLAM, Compute-Offloading) bietet.

### Kernphilosophie

- **Hardware-Abstraktion:** Software läuft isoliert von der Hardware durch definierte Interfaces.
    
- **Native ROS 2 Integration:** Durchgängige Kommunikation vom High-Level-Algorithmus bis zum Motor-Register mittels **micro-ROS**.
    
- **Modularität:** Jede Komponente (Antrieb, Sensorik, Logik) ist ein eigenständiger Service.
    

---

## 🛠 Technologie-Stack & Standards

|**Bereich**|**Technologie / Standard**|**Begründung**|
|---|---|---|
|**Sprachen**|C++20 / C|Performance und moderne Sprachfeatures (Smart Pointers, Ranges).|
|**Middleware**|**ROS 2 (Humble/Iron)**|Industriestandard für Robotik; nutzt DDS für zuverlässige Kommunikation.|
|**Kommunikation**|**micro-ROS (USB/Serial)**|Native ROS 2 Nodes auf MCUs; nutzt XRCE-DDS für ressourceneffiziente Pub/Sub-Kommunikation.|
|**Containerisierung**|**Docker & DevContainers**|Reproduzierbare Build-Umgebungen; Trennung von Host- und Target-System.|
|**Build-System**|CMake / Colcon|Standard für C++ und ROS 2 Projekte.|
|**Qualitätssicherung**|GTest / GMock / Linter|Sicherstellung der Code-Qualität durch Unit-Tests und statische Analyse.|

---

## 🏗 Systemarchitektur

Die Architektur folgt dem Muster eines modernen Fahrzeug-E/E-Systems, nutzt jedoch eine direkte serielle Verbindung:

1. **Low-Level Layer (Firmware):**
    
    - **Basis:** ESP32 oder STM32.
        
    - **Aufgabe:** Motoransteuerung (PWM), Encoder-Auslesung, Not-Aus-Logik.
        
    - **Schnittstelle:** **micro-ROS Client** (publiziert native ROS 2 Topics wie `/odom`).
        
2. **Middle Layer (Middleware):**
    
    - **Basis:** Raspberry Pi oder Jetson Nano (Dockerized ROS 2).
        
    - **Aufgabe:** Betrieb des **micro-ROS Agent**, der die Verbindung zwischen MCU und dem restlichen ROS-Graph herstellt.
        
3. **High-Level Layer (Applikation):**
    
    - **Aufgabe:** Mapping, Pfadplanung (Nav2), Hinderniserkennung.
        

> Die zugehörige Ordnerstruktur findest du in der [Ordnerstruktur](docs/setup/setup_windows.md#3-einrichtung-des-projekts) der Setup-Anleitung.
---

## 🔄 Entwicklungsprozess

Um Professionalität zu wahren, nutzen wir einen **Git-basierten Workflow**:

### 1. Dokumentation (Markdown-First)

- **ADRs (Architecture Decision Records):** Jede große Entscheidung (z. B. Wechsel von CAN zu USB/micro-ROS) wird in einer `.md`-Datei im Ordner `/docs/adr` begründet.
    
- **API-Docs:** Inline-Dokumentation via Doxygen.
    

### 2. Modularer Build-Prozess

Jedes Modul ist ein eigener ROS-Package oder eine eigenständige C++ Library.

- **Entwicklung im Container:** Die gesamte Toolchain (micro-ROS Build-System, Compiler) liegt im Docker-Image.
    
- **CI/CD (Geplant):** Automatisierte Builds und Tests bei jedem Push via GitHub Actions.
    

### 3. micro-ROS Integration

Anstatt manueller Byte-Protokolle nutzen wir das **XRCE-DDS** Protokoll:

- Der Mikrocontroller wird als vollwertiger Teilnehmer im ROS-Netzwerk behandelt.
    
- Kommunikation erfolgt über Standard-Messages (`geometry_msgs/Twist`, `nav_msgs/Odometry`).
    
- Kein manuelles Parsen von seriellen Datenströmen nötig; micro-ROS übernimmt die Serialisierung.
    

---

## 🚀 Roadmap: Phase 1 (The "Basics")
> Siehe dazu den [Projektstatus](STATUS.md) für den aktuellen Stand.

Fokus auf Hardware-naher C++ Entwicklung und Konnektivität.

- [ ] **Setup Dev-Environment:** Docker-Container mit ROS 2 und micro-ROS Komponenten.
    
- [ ] **Firmware "Drive-Unit":** micro-ROS Node auf dem MCU zur Steuerung der Motoren.
    
- [ ] **Topic-Definition:** Implementierung der Subscriber für `/cmd_vel` und Publisher für `/battery_state`.
    
- [ ] **ROS 2 Integration:** Validierung der Kommunikation zwischen Pi und MCU über den micro-ROS Agent.