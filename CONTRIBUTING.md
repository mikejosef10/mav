# 🛠 Contributing to MAV - Spec-Driven Development (SDD)

Welcome! This project follows a **Spec-Driven Development** (SDD) approach. The documentation is the single source of truth, and code is an implementation of that truth.

## 🔄 The SDD Cycle

### 1. Identify Requirement
Identify the component (e.g., `firmware/mav-esp-drive/`, `ros2_ws/`, `raspberry_pi/`). Check its local `docs/specs/SPEC.md`. If the feature or fix is not defined, **propose a change to the local spec first**.

### 2. Create or Update Task
Use the `docs/tasks/TASK_TEMPLATE.md` to create a new task. Link it to the specific Requirement IDs (`REQ-[COMPONENT]-[ID]`).

### 3. Implementation Flow
1. **Test-First:** Write a test case in the component's `test/` folder that fails because the requirement is not met.
2. **Code:** Implement the minimal code in the component's `src/` to satisfy the test.
3. **Validate:** Run the component's test suite (e.g., `pytest`, `colcon test`, `pio test`).
4. **Refactor:** Clean up while keeping the tests passing.

## 📏 Platform Standards
- **Firmware (ESP32):** C++20, Arduino Framework, `pio`.
- **ROS 2 / Raspberry Pi:**
    - **C++:** C++20 (GNU++2a), focused on modern STL and zero-cost abstractions.
    - **Python:** Python 3.10+, **strict Type Hinting required**, using `pytest` for validation.
    - **Build System:** `colcon` with `cmake` (C++) or `setuptools` (Python).
- **Documentation:** Markdown in `[component]/docs/` using Mermaid for diagrams.
- **Commits:** Clear messages referencing Task IDs (e.g., `feat(rpi): implement REQ-RPI-01 [TASK-004]`).

## 🤖 AI Collaboration (Gemini CLI)
Gemini CLI is instructed by `.mav-rules.md` (MAV Engineering Protocol) to follow this workflow across all folders. You can ask:
> "Analyze REQ-ESP-01 in mav-esp-drive and verify it against the code."
