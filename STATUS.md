# 📊 MAV Project Status

## 🚀 Current Focus
- [x] **TASK-001**: [Blinking-LED](docs/tasks/task-001-blinking-led.md) - *Verified via REQ-SYS-04*
- [x] **TASK-002**: [Micro-ROS Bridge](docs/tasks/task-002-micro-ros-bridge.md) - *Verified via REQ-COM-01/02*
- [x] **TASK-003**: [QEMU Simulation](docs/tasks/task-003-qemu-testing.md) - *Validated CI Infrastructure*
- [ ] **TASK-004**: [Motor-Control Spec](docs/tasks/TASK_TEMPLATE.md) - *In Planning*

## 🏁 Milestones (Spec-Driven)
- [x] **Phase 0: Engineering Protocol & SDD Setup** (Status: 100%)
- [ ] **Phase 1: Connectivity & Drive** (Status: 40%)
    - [x] micro-ROS Base Communication
    - [ ] PWM Motor Driver (REQ-MOT-01)
    - [ ] Encoder Feedback (REQ-ENC-01)
- [ ] **Phase 2: Perception & SLAM** (Status: 0%)
- [ ] **Phase 3: Autonomy & Vacuum Logic** (Status: 0%)

## 🛠 Active Tasks (Backlog)
| ID | Task | Req Ref | Status | Priority |
|:---|:---|:---|:---|:---|
| 001 | Micro-ROS Handshake (LED/Heartbeat) | REQ-COM-01 | ✅ Done | High |
| 002 | Docker DevContainer Setup | REQ-HW-01 | ✅ Done | High |
| 003 | QEMU Simulation & CI/CD | - | ✅ Done | High |
| 004 | Motor-Control Firmware (PWM) | REQ-MOT-01 | 📅 Planned | High |
| 005 | Raspberry Pi OS & ROS2 Setup | REQ-RPI-01 | ⏳ Waiting | Medium |

## 🚧 Blockers / Known Issues
- **Requirement Gap:** Motor control specs (REQ-MOT-01) need to be defined in `firmware/mav-esp-drive/docs/specs/SPEC.md`.

---
*Last Updated: 2026-03-08 (SDD Standard v1.0)*
