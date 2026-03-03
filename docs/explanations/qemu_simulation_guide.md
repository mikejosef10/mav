# QEMU Simulation Guide for ESP32 Firmware

This document describes how firmware tests can be performed in a simulated environment without physical hardware.

## Why QEMU?
ESP32 firmware development is often slowed down by hardware dependencies. QEMU (Quick Emulator) allows emulating the XTENSA processor behavior and running firmware binaries directly on a development machine (or in CI/CD pipelines).

### Advantages:
*   **Fast Iteration:** Test logic changes in seconds.
*   **Automation:** Integration into GitHub Actions.
*   **No Hardware Needed:** Ideal for distributed teams or development without constant access to the drive module.

## Setup (IMPORTANT)
Standard QEMU (`apt install qemu-system-xtensa`) usually does **NOT** support the `esp32` machine. Therefore, we use the special **Espressif QEMU Fork**.

### Local Installation of the Espressif Fork
The binaries are manually downloaded into the project directory to avoid global dependencies:

1.  **Download & Extraction:**
    The binaries are located in the `tools/qemu/` folder.
    ```bash
    mkdir -p tools/qemu && cd tools/qemu
    wget https://github.com/espressif/qemu/releases/download/esp-develop-9.2.2-20250817/qemu-xtensa-softmmu-esp_develop_9.2.2_20250817-x86_64-linux-gnu.tar.xz
    tar -xvf qemu-xtensa-softmmu-esp-*.tar.xz
    ```

2.  **System Dependencies (Ubuntu):**
    ```bash
    sudo apt-get install -y libgcrypt20 libglib2.0-0 libpixman-1-0 libsdl2-2.0-0 libslirp0
    ```

## Testing with Pytest

The project uses **pytest** to automate the build, merge, and simulation process. This is the recommended way to run integration tests.

1.  **Build:** Compiles the firmware with PlatformIO (`pio run`).
2.  **Merge & Pad:** Combines bootloader, partition table, and app into a `flash_image.bin` and pads it to exactly **4MB** (required for QEMU).
3.  **Run:** Starts the local Espressif QEMU and verifies specific milestones (Startup + Setup Completion).

### Option A: Local Run (Requires local QEMU and python dependencies)
```bash
export PATH=$PATH:$(pwd)/.venv/bin
cd firmware/mav-esp-drive
pytest -v -s test/test_qemu.py
```

### Option B: Docker Run (Recommended for CI/CD consistency)
For detailed instructions, see [Docker Usage Guide](../../firmware/mav-esp-drive/docker/DOCKER_USAGE.md).
```bash
cd firmware/mav-esp-drive
docker build --target ci -f docker/Dockerfile.qemu -t mav-esp-drive-qemu-test .
docker run --rm mav-esp-drive-qemu-test
```

## CI/CD Integration & Reporting

The project is configured with an enhanced reporting pipeline in GitHub Actions:

- **JUnit XML Reports:** The simulation generates a `report.xml` file containing detailed test results.
- **GitHub Actions Summary:** We use the `test-summary/action` to visualize these results directly in the GitHub Actions "Summary" tab.
- **Inline Annotations:** The `pytest-github-actions-annotate-failures` plugin provides direct annotations in the workflow logs for failed tests.

## Technical Details (What was fixed?)
*   **Flash Image:** QEMU only accepts flash sizes of 2, 4, 8, or 16 MB. The script now uses `esptool merge-bin --pad-to-size 4MB`.
*   **Machine Type:** The command uses `-machine esp32` (only available in the Espressif fork).
*   **BIOS Path:** The `-L tools/qemu/qemu/share/qemu` flag loads the necessary ROM files for the ESP32 boot process.

## Limitations
*   **Hardware Peripherals:** Complex hardware interactions (e.g., WiFi, Bluetooth, specific PWM modes) are not or only partially supported by QEMU.
*   **Timing:** The emulation is not hard real-time capable.
