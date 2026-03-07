# Dockerized QEMU Testing for ESP32

This directory contains the Docker configuration to run ESP32 firmware tests in a completely isolated environment using the Espressif QEMU fork.

## Prerequisites
- Docker installed on your host machine.
- WSL 2 integration enabled (if using Windows).

## Files
- `Dockerfile.qemu`: Defines the environment (Ubuntu 24.04, PlatformIO, Espressif QEMU v9.2.2).
- `qemu_test_runner.py`: The test script (located in `../scripts/`) which is called as the entrypoint.

## Usage

### 1. Build the Image
Run this command from the `firmware/drive_unit` directory:
```bash
docker build -f docker/Dockerfile.qemu -t drive-unit-qemu-test .
```

### 2. Run the Test
```bash
docker run --rm drive-unit-qemu-test
```

## Why use Docker for QEMU?
1. **Zero Setup:** No need to manually download binaries or install system libraries on your host.
2. **Consistency:** Ensures the test environment is identical to the one used in CI/CD (GitHub Actions).
3. **Isolation:** Keeps your main development environment clean from specific emulator dependencies.

## Customization
If you want to run a different command or explore the container:
```bash
docker run --rm -it drive-unit-qemu-test bash
```
