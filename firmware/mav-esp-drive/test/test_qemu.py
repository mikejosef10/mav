import os
import subprocess
import time
import pytest

# --- Configuration ---
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

# --- Fixtures ---

@pytest.fixture(scope="session", autouse=True)
def build_and_merge():
    """Builds the firmware once for the entire test session."""
    print("\n[PRE-TEST] Building and merging firmware...")
    
    # 1. Build
    res_build = run_cmd([PIO_CMD, "run"], cwd=PROJECT_DIR)
    if res_build.returncode != 0:
        pytest.fail(f"Build failed: {res_build.stdout}\n{res_build.stderr}")
    
    # 2. Merge
    bootloader = os.path.join(BUILD_DIR, "bootloader.bin")
    partitions = os.path.join(BUILD_DIR, "partitions.bin")
    firmware = os.path.join(BUILD_DIR, "firmware.bin")
    
    cmd_merge = [
        ESP_CMD, "--chip", "esp32", "merge-bin",
        "-o", FLASH_IMAGE,
        "--flash_mode", "dio", "--flash_size", "4MB",
        "--pad-to-size", "4MB",
        "0x1000", bootloader,
        "0x8000", partitions,
        "0x10000", firmware
    ]
    res_merge = run_cmd(cmd_merge)
    if res_merge.returncode != 0:
        pytest.fail(f"Merge failed: {res_merge.stderr}")

@pytest.fixture(scope="session")
def qemu_output():
    """Runs QEMU once and captures a fixed amount of output for analysis."""
    print("\n[PRE-TEST] Starting QEMU capture...")
    
    qemu_cmd = [
        QEMU_BIN,
        "-nographic",
        "-machine", "esp32",
        "-drive", f"file={FLASH_IMAGE},if=mtd,format=raw",
        "-serial", "mon:stdio",
    ]
    
    bios_path = os.path.join(os.path.dirname(QEMU_BIN), "../share/qemu")
    if os.path.exists(bios_path):
        qemu_cmd.extend(["-L", bios_path])

    process = subprocess.Popen(qemu_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    logs = []
    timeout = 30  # Increased timeout
    start_time = time.time()
    
    print("\n--- QEMU LIVE LOGS ---")
    try:
        while time.time() - start_time < timeout:
            line = process.stdout.readline()
            if not line: break
            clean_line = line.strip()
            if clean_line:
                print(f"| {clean_line}")
                logs.append(clean_line)
                # Early exit if we reached the end of setup
                if "[SYS] Setup complete" in clean_line:
                    print("--- SETUP COMPLETE MARKER DETECTED ---")
                    break
    finally:
        process.terminate()
        process.wait()
    print("--- QEMU CAPTURE FINISHED ---\n")
    
    return logs

# --- Test Classes ---

@pytest.mark.order(1)
class TestSystemFoundation:
    """Verifies that the core infrastructure is working."""
    
    def test_flash_image_exists(self):
        assert os.path.exists(FLASH_IMAGE), "Flash image was not generated."
        assert os.path.getsize(FLASH_IMAGE) == 4 * 1024 * 1024, "Flash image size is incorrect (must be 4MB)."

    def test_system_startup(self, qemu_output):
        assert any("[SYS] MAV Drive Unit starting..." in line for line in qemu_output), "System start marker not found."

@pytest.mark.order(2)
class TestFeatureLED:
    """Verifies the StatusLed subsystem."""
    
    def test_led_initialization(self, qemu_output):
        assert any("[LED] Initialized" in line for line in qemu_output), "LED subsystem failed to initialize."

    def test_led_visual_pattern(self, qemu_output):
        assert any("[LED] Test pattern completed" in line for line in qemu_output), "LED startup pattern did not complete."

@pytest.mark.order(3)
class TestFeatureMicroROS:
    """Verifies the micro-ROS subsystem."""
    
    def test_uros_transport(self, qemu_output):
        assert any("[uROS] Transport initialized" in line for line in qemu_output), "micro-ROS transport layer failed."

    def test_setup_finalization(self, qemu_output):
        assert any("[SYS] Setup complete" in line for line in qemu_output), "System failed to reach final setup stage."
