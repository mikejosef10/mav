# Dokumentation - ROS 2 MAV-Entwicklungsumgebung (Windows,Docker)
### 1. Architektur-Übersicht

Dein System ist in Schichten aufgebaut. Das Ziel ist es, Windows "sauber" zu halten und die gesamte Robotik-Toolchain in einem isolierten Container zu betreiben.

- **Layer 1 (Hardware):** Dein PC + USB-Anschluss.
    
- **Layer 2 (Host):** Windows 11/10 mit WSL 2 (Ubuntu 22.04).
    
- **Layer 3 (Engine):** Docker Desktop (verknüpft mit WSL 2).
    
- **Layer 4 (Entwicklung):** VS Code mit "Dev Containers".
    
- **Layer 5 (Runtime):** Der Docker-Container mit **ROS 2 Humble** und C++20.
    

---

### 2. Installations-Checkliste (Der Status Quo)

| **Schritt**        | **Status** | **Aktion**                                                                                                  |
| ------------------ | ---------- | ----------------------------------------------------------------------------------------------------------- |
| **WSL 2 & Ubuntu** | ✅ Erledigt | [WSL Installation Guide](wsl_installation_guide.md) .                                                                    |
| **Docker Desktop** | ✅ Erledigt | [Hier herunterladen](https://www.docker.com/products/docker-desktop/). Bei Installation "Use WSL 2" wählen. |
| **VS Code**        | ✅ Erledigt | Installieren und Extension **"Dev Containers"** hinzufügen.                                                 |
| **USBIPD**         | ✅ Erledigt | [Hier laden](https://github.com/dorssel/usbipd-win/releases).          |
---

**### 3. Einrichtung des Projekts**

Um das Dockerfile und die Konfiguration zu nutzen, muss dein Projektordner so aussehen:

```
.
├── docker/                     # Dockerfiles & DevContainer Settings
├── docs/                       # Dokumentation (ADRs, Hardware, etc.)
├── firmware/                   # Alles, was auf den ESP32 geflasht wird
│   └── drive_unit/             # Dein aktuelles ESP32-Projekt
│       ├── include/
│       ├── lib/                # Eigene Libs wie StatusLed
│       ├── src/
│       │   └── main.cpp        # micro-ROS Client Code
│       ├── test/               # Unit Tests für Hardware-Logik
│       └── platformio.ini
├── ros2_ws/                    # Der ROS 2 Workspace für den Raspberry Pi
│   └── src/
│       ├── mav_description/    # URDF-Modelle & Transformationen
│       ├── mav_bringup/        # Launch-Files, um Agent + Nodes zu starten
│       ├── mav_teleop/         # High-Level Steuerung (z.B. Joystick)
│       └── mav_interfaces/     # Eigene Message-Definitionen (falls nötig)
├── scripts/                    # Hilfsskripte (z.B. Flashen, Setup)
└── README.md
```

**Der magische Moment:** Wenn du diesen Ordner in VS Code öffnest, erscheint unten rechts ein Pop-up:

> _"Folder contains a Dev Container configuration file. Reopen to folder to develop in a container."_

Klicke auf **"Reopen in Container"**. VS Code baut nun das Image (dauert beim ersten Mal ca. 5-10 Min) und verbindet sich direkt in das Linux-System des Containers.

---

### 4. Funktionsweise im Alltag (Workflow)

#### A. Programmierung & Kompilierung

Du schreibst Code in VS Code wie gewohnt. Da VS Code "im" Container läuft, erkennt es alle ROS 2 Header und C++20 Features sofort.

Zum Kompilieren öffnest du das Terminal in VS Code (es ist automatisch ein Linux-Terminal im Container) und tippst:

Bash

```
colcon build --symlink-install
source install/setup.bash
```

#### B. Hardware-Integration

Damit der USB-Anschluss im Container ankommt, nutzt du auf **Windows** (PowerShell) diesen Ablauf:

1. Anschluss (mit der ESP32 zum Beispiel) einstecken.
    
2. `usbipd list` (ID des Adapters finden).
    
3. `usbipd bind --busid <ID>` (Einmalig als Admin).
    
4. `usbipd attach --wsl --busid <ID>` (Verbindet ihn mit WSL).
    
    

#### C. Grafische Benutzeroberflächen (Rviz2 / Gazebo)

Dank WSLg musst du nichts konfigurieren. Wenn du im Container-Terminal `rviz2` eingibst, öffnet sich das Fenster direkt auf deinem Windows-Desktop. Die GPU-Beschleunigung wird dabei von Windows an den Container durchgereicht.

---

### 5. Wartung & Tipps

- **Image-Updates:** Wenn du das Dockerfile änderst, drücke in VS Code `F1` -> `Dev Containers: Rebuild Container`.
    
- **Speicherplatz:** Docker-Images fressen Platz. Mit `docker system prune` (in der PowerShell) löschst du alte, ungenutzte Layer.
    
- **Performance:** Achte darauf, dass dein Quellcode im **WSL-Dateisystem** liegt (z.B. `\\wsl$\Ubuntu\home\user\projects`), nicht auf `C:\`. Der Zugriff von Docker auf Windows-Laufwerke (`/mnt/c/`) ist sehr langsam.



