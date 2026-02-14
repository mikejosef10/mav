# Installation von WSL 2
- **Ubuntu-Paket ziehen:** Gib in der PowerShell (Admin) folgendes ein:
   PowerShell
    
   ```
    curl.exe -L -o ubuntu.appx https://aka.ms/wslubuntu2204
    ```
    
    _(Das lädt Ubuntu 22.04 herunter, genau die Version, die perfekt zu deinem ROS 2 Humble Docker-Setup passt.)_
    
- **Installieren:**
    
    PowerShell
    
   ```
    Add-AppxPackage .\ubuntu.appx
    ```
   
- **Starten:** Suche jetzt im Startmenü nach **"Ubuntu"** und klicke darauf. Es öffnet sich ein schwarzes Fenster, das die Installation abschließt (hier vergibst du dann deinen Benutzernamen und Passwort).
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