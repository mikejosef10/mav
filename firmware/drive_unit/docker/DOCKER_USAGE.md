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
docker build --target development -f docker/Dockerfile.qemu -t drive-unit-dev .

# Run and mount your current code as a volume for live updates
docker run --rm -it -v $(pwd):/app drive-unit-dev
```

### 2. For CI/CD (Automated Test)
Build and run the CI stage. This copies the current code into the image and runs the test script as the entrypoint.
```bash
# Build the CI stage
docker build --target ci -f docker/Dockerfile.qemu -t drive-unit-qemu-test .

# Run the test
docker run --rm drive-unit-qemu-test
```

## Why Multi-Stage?
- **Intent Separation**: Clear distinction between an interactive environment and a standalone test environment.
- **Workflow Flexibility**: Developers can mount their code into the `development` stage for fast iteration without rebuilding the image.
- **CI/CD Reliability**: The `ci` stage produces a self-contained image that includes exactly the code state at build time.
