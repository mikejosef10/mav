@echo off
:: Ersetze die VID:PID durch die deines ESP32 (aus usbipd list) und führe dieses Skript auf dem Windows-Host aus, um den ESP32 an WSL zu binden.
set DEVICE_ID=10c4:ea60 
for /f "tokens=1" %%a in ('usbipd list ^| findstr "%DEVICE_ID%"') do set BUSID=%%a
if defined BUSID (
    echo Attach ESP32 on Bus %BUSID%...
    usbipd attach --wsl --busid %BUSID%
) else (
    echo ESP32 nicht gefunden. Kabel fest?
    pause
)