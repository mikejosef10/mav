# TASK-003: QEMU-based Test Environment for ESP32 Firmware

## 📝 Description
Introduction of a hardware-independent test environment using Espressif's QEMU fork. This allows testing firmware logic (without physical ESP32) and integration into CI/CD pipelines (GitHub Actions).

## 🎯 Acceptance Criteria (Definition of Done)
- [x] QEMU configuration is operational for the `firmware/drive_unit` project.
- [x] Documentation for local QEMU usage is available (`docs/explanations/qemu_simulation_guide.md`).
- [x] Test runner script automates Build, Merge, and Run.
- [ ] CI/CD pipeline (GitHub Actions) runs tests in QEMU successfully (Waiting for repo sync).

## ⚙️ Technical Specifications
- **Emulator:** [Espressif QEMU Fork](https://github.com/espressif/qemu)
- **Architecture:** Xtensa (ESP32)
- **CI Tool:** GitHub Actions
- **Integration Method:** Scripting or PlatformIO hooks

## 📌 Documentation
- `docs/adr/0002-qemu-simulation-for-testing.md`
- `docs/explanations/qemu_simulation_guide.md`
