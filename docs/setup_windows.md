# Dokumentation - ROS 2 MAV-Entwicklungsumgebung (Windows,Docker)
### 1. Architektur-Übersicht

Dein System ist in Schichten aufgebaut. Das Ziel ist es, Windows "sauber" zu halten und die gesamte Robotik-Toolchain in einem isolierten Container zu betreiben.

- **Layer 1 (Hardware):** Dein PC + USB-CAN Adapter.
    
- **Layer 2 (Host):** Windows 11/10 mit WSL 2 (Ubuntu 22.04).
    
- **Layer 3 (Engine):** Docker Desktop (verknüpft mit WSL 2).
    
- **Layer 4 (Entwicklung):** VS Code mit "Dev Containers".
    
- **Layer 5 (Runtime):** Der Docker-Container mit **ROS 2 Humble**, C++20 und CAN-Tools.
    

---

### 2. Installations-Checkliste (Der Status Quo)

| **Schritt**        | **Status** | **Aktion**                                                                                                  |
| ------------------ | ---------- | ----------------------------------------------------------------------------------------------------------- |
| **WSL 2 & Ubuntu** | ✅ Erledigt | Ubuntu ist installiert und eingerichtet.                                                                    |
| **Docker Desktop** | ✅ Erledigt | [Hier herunterladen](https://www.docker.com/products/docker-desktop/). Bei Installation "Use WSL 2" wählen. |
| **VS Code**        | ✅ Erledigt | Installieren und Extension **"Dev Containers"** hinzufügen.                                                 |
| **USBIPD**         | ✅ Erledigt | [Hier laden](https://github.com/dorssel/usbipd-win/releases). Wichtig für den CAN-Adapter-Zugriff.          |

>[!hint]- WSL 2 Installation
>- **Ubuntu-Paket ziehen:** Gib in der PowerShell (Admin) folgendes ein:
 >   PowerShell
>    
 >   ```
>    curl.exe -L -o ubuntu.appx https://aka.ms/wslubuntu2204
>    ```
>    
>    _(Das lädt Ubuntu 22.04 herunter, genau die Version, die perfekt zu deinem ROS 2 Humble Docker-Setup passt.)_
>    
>- **Installieren:**
>    
>    PowerShell
>    
 >   ```
>    Add-AppxPackage .\ubuntu.appx
>    ```
 >   
>- **Starten:** Suche jetzt im Startmenü nach **"Ubuntu"** und klicke darauf. Es öffnet sich ein schwarzes Fenster, das die Installation abschließt (hier vergibst du dann deinen Benutzernamen und Passwort).
---

### 3. Einrichtung des Projekts

Um das Dockerfile und die Konfiguration zu nutzen, muss dein Projektordner so aussehen:

```
mav_project/
├── .devcontainer/         # Docker- & VS Code-Konfiguration
├── .vscode/               # Editor-spezifische Einstellungen (Launch-Configs)
├── docs/                  # Zentrale Dokumentation (Markdown, Diagramme)
│   ├── architecture/      # Diagramme, Layer-Beschreibungen
│   ├── hardware/          # Pinbelegung, CAN-Adapter-Specs
│   └── setup_guide.md     # Deine Checkliste von oben
├── src/                   # Der ROS 2 Workspace
│   ├── module_a/          # Softwaremodul 1 (z.B. Motor-Treiber)
│   │   ├── include/
│   │   ├── src/
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   ├── module_b/          # Softwaremodul 2 (z.B. Sensor-Processing)
│   └── interfaces/        # Eigene ROS 2 Msgs/Srvs (wichtig für Modularität)
├── scripts/               # Hilfsskripte (z.B. usbipd-attach.ps1)
├── README.md              # Der "Einstiegspunkt" für Menschen
└── .gitignore             # Schließt build/, install/, log/ aus
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

#### B. Hardware-Integration (CAN-Bus)

Damit der CAN-Adapter im Container ankommt, nutzt du auf **Windows** (PowerShell) diesen Ablauf:

1. Adapter einstecken.
    
2. `usbipd list` (ID des Adapters finden).
    
3. `usbipd bind --busid <ID>` (Einmalig als Admin).
    
4. `usbipd attach --wsl --busid <ID>` (Verbindet ihn mit WSL).
    
    Im Container erscheint er dann als `can0` und kann mit `candump can0` getestet werden.
    

#### C. Grafische Benutzeroberflächen (Rviz2 / Gazebo)

Dank WSLg musst du nichts konfigurieren. Wenn du im Container-Terminal `rviz2` eingibst, öffnet sich das Fenster direkt auf deinem Windows-Desktop. Die GPU-Beschleunigung wird dabei von Windows an den Container durchgereicht.

---

### 5. Wartung & Tipps

- **Image-Updates:** Wenn du das Dockerfile änderst, drücke in VS Code `F1` -> `Dev Containers: Rebuild Container`.
    
- **Speicherplatz:** Docker-Images fressen Platz. Mit `docker system prune` (in der PowerShell) löschst du alte, ungenutzte Layer.
    
- **Performance:** Achte darauf, dass dein Quellcode im **WSL-Dateisystem** liegt (z.B. `\\wsl$\Ubuntu\home\user\projects`), nicht auf `C:\`. Der Zugriff von Docker auf Windows-Laufwerke (`/mnt/c/`) ist sehr langsam.


---

# Umsiedlung von C:/ auf D:/
Hier ist die vollständige Anleitung im sauberen Markdown-Format. Du kannst dir diesen Text einfach kopieren und als `wsl_migration_guide.md` in deinem Projekt speichern.

---

# 📑 Anleitung: WSL 2 (Ubuntu) von C: nach D: umziehen

Diese Anleitung beschreibt, wie du deine gesamte Linux-Entwicklungsumgebung inklusive aller Docker-Daten auf eine andere Festplatte (z. B. Laufwerk **D:**) verschiebst, um Platz auf der Systemplatte **C:** zu sparen.

## ⚠️ Wichtige Vorab-Checks

1. **Name der Distribution:** Prüfe in der PowerShell mit `wsl -l -v`, wie deine Instanz genau heißt (meist `Ubuntu`).
2. **Backups:** Falls du wichtige Dateien außerhalb von Git hast, stelle sicher, dass sie gesichert sind (obwohl der Export-Befehl ein Backup ist).
3. **Speicherplatz:** Stelle sicher, dass auf Laufwerk **D:** genug Platz für die `.tar`-Datei (Backup) **und** die spätere `.vhdx`-Datei (die neue virtuelle Festplatte) vorhanden ist.

---

## 🛠 Schritt-für-Schritt-Prozess

### 1. WSL beenden

Schließe alle Ubuntu-Terminals und VS Code Fenster. Öffne eine **PowerShell (Administrator)** und beende alle Instanzen:

```powershell
wsl --shutdown

```

### 2. Export der aktuellen Instanz

Erstelle einen Ordner auf **D:** für dein Backup und exportiere das System. Dies kann je nach Größe des Projekts einige Minuten dauern.

```powershell
mkdir D:\wsl_backup
wsl --export Ubuntu D:\wsl_backup\ubuntu_backup.tar

```

### 3. Alte Instanz von C: entfernen

Jetzt wird die Instanz auf C: gelöscht. Dies gibt den Speicherplatz auf deiner Systemplatte sofort frei.

```powershell
wsl --unregister Ubuntu

```

### 4. Import auf die neue Festplatte (D:)

Erstelle den Zielordner, in dem Ubuntu ab jetzt "leben" soll. Dann importiere das Backup dorthin:

```powershell
mkdir D:\WSL\Ubuntu
wsl --import Ubuntu D:\WSL\Ubuntu D:\wsl_backup\ubuntu_backup.tar

```

### 5. Standard-Benutzer wiederherstellen

Standardmäßig loggt dich WSL nach einem Import als `root` ein. Um deinen gewohnten User wieder einzustellen:

```powershell
# Ersetze 'deinname' durch deinen echten Linux-Benutzernamen
ubuntu2204 config --default-user deinname

```

> **Tipp:** Falls der Befehl `ubuntu2204` nicht funktioniert, kannst du in der Datei `/etc/wsl.conf` innerhalb von Ubuntu folgendes eintragen:
> ```ini
> [user]
> default=deinname
> 
> ```
> 
> 

---

## 🔄 Docker-Anbindung prüfen

Da Docker Desktop mit WSL verknüpft ist, musst du sicherstellen, dass die Verbindung noch steht:

1. Starte **Docker Desktop**.
2. Gehe zu **Settings > Resources > WSL Integration**.
3. Stelle sicher, dass der Schalter bei **Ubuntu** aktiviert ist.
4. Klicke auf **Apply & Restart**.

---

## 📁 Aufräumen

Wenn alles funktioniert und du dein MAV-Projekt in VS Code wieder öffnen kannst, kannst du die temporäre Backup-Datei löschen:

```powershell
rm D:\wsl_backup\ubuntu_backup.tar

```
