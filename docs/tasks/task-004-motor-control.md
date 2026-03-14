# TASK-004: Motor Control Implementation (TB6612FNG)

## 🎯 Goal
Implement the motor control logic for two N20 DC motors using the TB6612FNG driver. This includes forward/backward motion, speed control (PWM), and integration with micro-ROS.

## 📋 Requirements (Traceability)
- [ ] **REQ-MOT-01 to REQ-MOT-05**: Hardware Pin Mapping & Logic.
- [ ] **REQ-SYS-05**: Motor initialization sequence.
- [ ] **REQ-COM-03** (New): micro-ROS subscription for motor commands (e.g., `/mav/cmd/velocity`).

## 🛠 Sub-Tasks
1. [ ] **Hardware Abstraction**: Create a `Motor` class to handle individual motor logic (PWM, Direction).
2. [ ] **Driver Integration**: Implement the TB6612FNG standby logic (GPIO 22).
3. [ ] **micro-ROS Integration**: 
    - Add a subscriber for motor control.
    - Implement a callback to translate ROS commands to motor speeds.
4. [ ] **Safety Features**: Add a timeout (e.g., stop motors if no command is received for 500ms).

## 🧪 Validation
- **Unit Test**: Test the `Motor` class logic (mocking PWM).
- **QEMU Test**: Verify the firmware boots and subscribes to the new topic.
- **Hardware Test**: Verify the physical motors rotate correctly (Forward/Backward/Stop).

## 📅 Status
- **Status**: 🚀 Active
- **Assigned to**: Gemini CLI
- **Started**: 2026-03-14
