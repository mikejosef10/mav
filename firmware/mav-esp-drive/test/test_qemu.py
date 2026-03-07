import os
import subprocess
import time
import pytest

# Configuration
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Use the workspace root's .venv/bin for pio and esptool
VENV_BIN = os.path.join(os.path.dirname(os.path.dirname(PROJECT_DIR)), ".venv/bin")

PIO_CMD = os.path.join(VENV_BIN, "pio")
ESP_CMD = os.path.join(VENV_BIN, "esptool")

BUILD_DIR = os.path.join(PROJECT_DIR, ".pio/build/esp32dev")
FLASH_IMAGE = os.path.join(PROJECT_DIR, "flash_image.bin")

# QEMU Discovery
workspace_root = os.path.dirname(os.path.dirname(PROJECT_DIR))
LOCAL_QEMU = os.path.join(workspace_root, "tools/qemu/qemu/bin/qemu-system-xtensa")

if "QEMU_BIN" in os.environ:
    QEMU_BIN = os.environ["QEMU_BIN"]
elif os.path.exists(LOCAL_QEMU):
    QEMU_BIN = LOCAL_QEMU
else:
    QEMU_BIN = "qemu-system-xtensa"

def run_cmd(cmd, cwd=None):
    """Helper to run shell commands."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

@pytest.mark.order(1)
def test_pio_build():
    """Step 1: Verify that PlatformIO can build the firmware."""
    print("\nBuilding firmware...")
    result = run_cmd([PIO_CMD, "run"], cwd=PROJECT_DIR)
    assert result.returncode == 0, f"Build failed: {result.stdout}\n{result.stderr}"

    assert os.path.exists(os.path.join(BUILD_DIR, "bootloader.bin"))
    assert os.path.exists(os.path.join(BUILD_DIR, "partitions.bin"))
    assert os.path.exists(os.path.join(BUILD_DIR, "firmware.bin"))

@pytest.mark.order(2)
def test_create_flash_image():
    """Step 2: Verify that esptool can create a padded flash image for QEMU."""
    bootloader = os.path.join(BUILD_DIR, "bootloader.bin")
    partitions = os.path.join(BUILD_DIR, "partitions.bin")
    firmware = os.path.join(BUILD_DIR, "firmware.bin")

    cmd = [
        ESP_CMD, "--chip", "esp32", "merge-bin",
        "-o", FLASH_IMAGE,
        "--flash_mode", "dio", "--flash_size", "4MB",
        "--pad-to-size", "4MB",
        "0x1000", bootloader,
        "0x8000", partitions,
        "0x10000", firmware
    ]

    
    result = run_cmd(cmd)
    assert result.returncode == 0, f"Flash image creation failed: {result.stderr}"
    assert os.path.exists(FLASH_IMAGE)
    assert os.path.getsize(FLASH_IMAGE) == 4 * 1024 * 1024  # Must be exactly 4MB

@pytest.mark.order(3)
def test_qemu_firmware_execution():
    """Step 3: Run QEMU and verify firmware milestones."""
    qemu_cmd = [
        QEMU_BIN,
        "-nographic",
        "-machine", "esp32",
        "-drive", f"file={FLASH_IMAGE},if=mtd,format=raw",
        "-serial", "mon:stdio",
    ]
    
    # Add BIOS path if it's the local Espressif fork
    bios_path = os.path.join(os.path.dirname(QEMU_BIN), "../share/qemu")
    if os.path.exists(bios_path):
        qemu_cmd.extend(["-L", bios_path])

    # Start QEMU
    process = subprocess.Popen(qemu_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    milestones = {
        "MAV Drive Unit started...": False,
        "SETUP_COMPLETE": False
    }
    
    timeout = 30
    start_time = time.time()
    
    try:
        for line in iter(process.stdout.readline, ""):
            if time.time() - start_time > timeout:
                break
                
            line_str = line.strip()
            if not line_str:
                continue
                
            print(f"[QEMU] {line_str}")
            
            for key in milestones:
                if key in line_str:
                    milestones[key] = True
            
            # If all milestones are reached, we can stop
            if all(milestones.values()):
                break
    finally:
        process.terminate()
        process.wait()

    # Assertions
    assert milestones["MAV Drive Unit started..."], "Firmware failed to reach startup milestone."
    assert milestones["SETUP_COMPLETE"], "Firmware failed to reach setup completion milestone."
