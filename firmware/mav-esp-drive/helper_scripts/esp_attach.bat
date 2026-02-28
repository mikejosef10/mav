@echo off
:: Replace the VID:PID with your ESP32's (from usbipd list) and run this script on the Windows host to bind the ESP32 to WSL.
set DEVICE_ID=10c4:ea60 
for /f "tokens=1" %%a in ('usbipd list ^| findstr "%DEVICE_ID%"') do set BUSID=%%a
if defined BUSID (
    echo Attaching ESP32 on Bus %BUSID%...
    usbipd attach --wsl --busid %BUSID%
) else (
    echo ESP32 not found. Is the cable secure?
    pause
)