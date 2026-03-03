# ADR 0002: Introducing QEMU Simulation for ESP32 Firmware Tests

**Status:** Accepted  
**Date:** 2026-03-02  
**Stakeholders:** Developer (Gemini CLI)

## Context
Developing firmware for the ESP32 typically requires physical hardware for testing. This slows down the development cycle, complicates CI/CD automation, and makes testing dependent on hardware availability.

## Decision
We use the **Espressif QEMU Fork** (Xtensa support) to run ESP32 binaries in a simulated environment. Since standard QEMU (apt) does not support the `esp32` machine type, the binary was stored locally under `tools/qemu/`.

## Rationale
- **Hardware Independence:** Developers can validate code changes locally without connecting an ESP32.
- **CI/CD Integration:** Enables automated regression testing on every push/pull request in GitHub Actions.
- **Specific Support:** Only the Espressif fork provides the necessary emulation for ESP32-specific ROMs and machine types.

## Implementation
- **Flash Images:** Images must be created with `esptool merge-bin --pad-to-size 4MB`.
- **Test Runner:** A Python script (`firmware/drive_unit/scripts/qemu_test_runner.py`) automates the build, image creation, and simulation.
