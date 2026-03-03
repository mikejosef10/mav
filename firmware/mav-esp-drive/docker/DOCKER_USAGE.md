# Dockerized QEMU Testing for ESP32

This Dockerfile uses a **Multi-Stage Build** to provide optimized environments for both development and CI/CD testing.

## Stages
1. **`base`**: Contains only the OS and the Espressif QEMU binaries.
2. **`builder`**: Adds Python, PlatformIO, and esptool.
3. **`development`**: A workspace for interactive development and debugging.
4. **`ci`**: A standalone stage that copies the code and runs the tests automatically.

## Usage

### 1. For Development (Interactive Shell)
Build and run the development stage. This is useful for manual debugging inside the container.
```bash
# Build the development stage
docker build --target development -f docker/Dockerfile.qemu -t mav-esp-drive-dev .

# Run and mount your current code as a volume for live updates
docker run --rm -it -v $(pwd):/app mav-esp-drive-dev
```

### 2. For CI/CD (Automated Pytest)
Build and run the CI stage. This runs the `pytest` suite which checks:
- Firmware build (`pio run`)
- Flash image creation (`esptool merge-bin`)
- QEMU execution and runtime milestones (Startup + Setup Completion)

```bash
# Build the CI stage
docker build --target ci -f docker/Dockerfile.qemu -t mav-esp-drive-qemu-test .

# Run the test and export the report to your host
docker run --rm -v $(pwd):/reports mav-esp-drive-qemu-test bash -c "pytest -v -s --junitxml=/reports/report.xml test/test_qemu.py"
```

## Why Multi-Stage & Pytest?
- **Modular Testing**: Individual test cases for build, merge, and run.
- **Enhanced Reporting**: Generates `report.xml` (JUnit format) for visualization in CI/CD (GitHub Actions) or local tools.
- **GitHub Integration**: Inline annotations for test failures in the GitHub Actions UI.
- **Intent Separation**: Clear distinction between an interactive development environment and a standalone test environment.
