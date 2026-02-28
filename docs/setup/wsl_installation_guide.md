# Installation of WSL 2
- **Download Ubuntu Package:** Enter the following in PowerShell (Admin):
   PowerShell
    
   ```
    curl.exe -L -o ubuntu.appx https://aka.ms/wslubuntu2204
    ```
    
    _(This downloads Ubuntu 22.04, the version that perfectly matches your ROS 2 Humble Docker setup.)_
    
- **Install:**
    
    PowerShell
    
   ```
    Add-AppxPackage .\ubuntu.appx
    ```
   
- **Start:** Now search for **"Ubuntu"** in the Start menu and click on it. A black window will open to complete the installation (where you then assign your username and password).
---

# 📑 Guide: Moving WSL 2 (Ubuntu) from C: to D:

This guide describes how to move your entire Linux development environment, including all Docker data, to another hard drive (e.g., drive **D:**) to save space on the system drive **C:**.

## ⚠️ Important Pre-checks

1. **Distribution Name:** Check in PowerShell with `wsl -l -v` what exactly your instance is named (usually `Ubuntu`).
2. **Backups:** If you have important files outside of Git, make sure they are backed up (although the export command itself is a backup).
3. **Storage Space:** Ensure there is enough space on drive **D:** for the `.tar` file (backup) **and** the subsequent `.vhdx` file (the new virtual hard drive).

---

## 🛠 Step-by-Step Process

### 1. Shutdown WSL

Close all Ubuntu terminals and VS Code windows. Open a **PowerShell (Administrator)** and terminate all instances:

```powershell
wsl --shutdown

```

### 2. Export Current Instance

Create a folder on **D:** for your backup and export the system. This may take several minutes depending on the project size.

```powershell
mkdir D:\wsl_backup
wsl --export Ubuntu D:\wsl_backup\ubuntu_backup.tar

```

### 3. Remove Old Instance from C:

Now delete the instance on C:. This will immediately free up space on your system drive.

```powershell
wsl --unregister Ubuntu

```

### 4. Import to New Hard Drive (D:)

Create the destination folder where Ubuntu should "live" from now on. Then import the backup there:

```powershell
mkdir D:\WSL\Ubuntu
wsl --import Ubuntu D:\WSL\Ubuntu D:\wsl_backup\ubuntu_backup.tar

```

### 5. Restore Default User

By default, WSL logs you in as `root` after an import. To restore your usual user:

```powershell
# Replace 'yourname' with your actual Linux username
ubuntu2204 config --default-user yourname

```

> **Tip:** If the command `ubuntu2204` does not work, you can enter the following in the `/etc/wsl.conf` file within Ubuntu:
> ```ini
> [user]
> default=yourname
> 
> ```
> 
> 

---

## 🔄 Check Docker Connection

Since Docker Desktop is linked with WSL, you must ensure the connection is still active:

1. Start **Docker Desktop**.
2. Go to **Settings > Resources > WSL Integration**.
3. Ensure the switch for **Ubuntu** is enabled.
4. Click **Apply & Restart**.

---

## 📁 Cleanup

If everything works and you can reopen your MAV project in VS Code, you can delete the temporary backup file:

```powershell
rm D:\wsl_backup\ubuntu_backup.tar

```