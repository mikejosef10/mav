# 🛠 Contributing to MAV - Engineering Protocol & SDD

Welcome! This project follows a **Spec-Driven Development** (SDD) approach and strict engineering standards. Documentation is the "Single Source of Truth".

## 🎯 Core Rules (The MAV Protocol)

1. **Spec-First:** Before any implementation or bug fix, you MUST verify requirements in the local component's specification file (e.g., `**/docs/specs/SPEC.md`).
2. **Component Autonomy:** Documentation and specs remain within their respective component folders (e.g., `firmware/mav-esp-drive/`) to keep them portable.
3. **Traceability:** Every code change must be traceable to a Requirement ID (`REQ-[PLATFORM]-[ID]`) and a Task ID in `docs/tasks/`.
4. **No Phantom Features:** Do not implement functionality not defined in a spec. Propose a spec update first if needed.
5. **Validation is Mandatory:** A task is "Done" only when it passes validation (tests/logs) defined in its local `test/` or `docs/specs/` folder.

## 🔄 The SDD Workflow

### 1. Research & Identify Requirement
Identify the affected component and check its local `docs/specs/SPEC.md`. If the feature or fix is not defined, **propose a change to the local spec first**.

### 2. Strategy & Task Management
Use the `docs/tasks/TASK_TEMPLATE.md` to create or update a task. Link it to the specific Requirement IDs (`REQ-[COMPONENT]-[ID]`).

### 3. Implementation Flow (Test-First)
1. **Test-First:** Write a test case in the component's `test/` folder that fails because the requirement is not met.
2. **Code:** Implement the minimal code in the component's `src/` to satisfy the test.
3. **Validate:** Run the component's test suite (e.g., `pytest`, `colcon test`, `pio test`).
4. **Refactor:** Clean up while keeping the tests passing.

## 📏 Platform Standards

- **Firmware (ESP32):** C++20, Arduino Framework, PlatformIO (`pio`).
- **ROS 2 / Raspberry Pi:**
    - **C++:** C++20 (GNU++2a), focused on modern STL and zero-cost abstractions.
    - **Python:** Python 3.10+, **strict Type Hinting required**, using `pytest`.
    - **Build System:** `colcon` with `cmake` (C++) or `setuptools` (Python).
- **Documentation:** Markdown in `[component]/docs/` using Mermaid for diagrams.
- **Commits:** Clear messages referencing Task IDs (e.g., `feat(rpi): implement REQ-RPI-01 [TASK-004]`).

## 📁 Project Structure Convention
Every major component should follow this layout:
- `[component]/docs/specs/SPEC.md`: Technical interfaces and requirements.
- `[component]/docs/adr/`: Local architectural decisions.
- `[component]/src/`: Implementation code.
- `[component]/test/`: Validation suite.

## 🤖 AI Collaboration (Gemini CLI)
Gemini CLI is instructed to follow this protocol across all folders. You can ask:
> "Analyze REQ-ESP-01 in mav-esp-drive and verify it against the code."
