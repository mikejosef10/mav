#include <Arduino.h>
#include <micro_ros_platformio.h>

#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <std_msgs/msg/int32.h>
#include <std_msgs/msg/bool.h>

#include "StatusLed.hpp"

// --- Configuration ---
#define LED_PIN 2 // Builtin LED for ESP32 DevKit V1
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){ return false; }}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

// --- Global Objects ---
StatusLed statusLed(LED_PIN);

rcl_publisher_t publisher;
rcl_subscription_t subscriber;
std_msgs__msg__Int32 msg_heartbeat;
std_msgs__msg__Bool msg_led_cmd;

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

// --- Callbacks ---

// Error handling: Blinks frantically if micro-ROS fails
void error_loop(){
  while(1){
    statusLed.on(); delay(100);
    statusLed.off(); delay(100);
  }
}

// Timer Callback: Heartbeat (1 Hz)
void timer_callback(rcl_timer_t * timer, int64_t last_call_time) {
  (void) last_call_time;
  if (timer != NULL) {
    msg_heartbeat.data++;
    RCSOFTCHECK(rcl_publish(&publisher, &msg_heartbeat, NULL));
  }
}

// Subscription Callback: LED Control
void subscription_callback(const void * msgin) {
  const std_msgs__msg__Bool * msg = (const std_msgs__msg__Bool *)msgin;
  if (msg->data) {
    statusLed.on();
  } else {
    statusLed.off();
  }
}

// --- Main Setup ---

bool init_microros() {
    allocator = rcl_get_default_allocator();

    // 1. Support
    RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

    // 2. Node
    RCCHECK(rclc_node_init_default(&node, "mav_drive_unit", "", &support));

    // 3. Publisher
    RCCHECK(rclc_publisher_init_default(
        &publisher, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
        "/mav/status/heartbeat"));

    // 4. Subscriber
    RCCHECK(rclc_subscription_init_default(
        &subscriber, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
        "/mav/cmd/led"));

    // 5. Timer
    RCCHECK(rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(1000), timer_callback));

    // 6. Executor
    executor = rclc_executor_get_zero_initialized_executor();
    RCCHECK(rclc_executor_init(&executor, &support.context, 2, &allocator));
    RCCHECK(rclc_executor_add_timer(&executor, &timer));
    RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg_led_cmd, &subscription_callback, ON_NEW_DATA));

    return true;
}

void setup() {
    // Delay serial initialization to wait for boot logs
    delay(1000); 
    Serial.begin(115200);
    
    Serial.println("[SYS] MAV Drive Unit starting...");
    
    // Feature: LED
    statusLed.begin();
    Serial.println("[LED] Initialized");
    
    // Signaling: "I am ready to connect"
    statusLed.on(); delay(500); statusLed.off(); 
    Serial.println("[LED] Test pattern completed");
    
    // Feature: micro-ROS
    set_microros_serial_transports(Serial);
    Serial.println("[uROS] Transport initialized");
    
    Serial.println("[SYS] Setup complete");
}

void loop() {
    static bool micro_ros_init_successful = false;

    if (!micro_ros_init_successful) {
        if (init_microros()) {
            micro_ros_init_successful = true;
            statusLed.off(); 
        } else {
            // Full cleanup on error
            rclc_executor_fini(&executor);
            rcl_publisher_fini(&publisher, &node);
            rcl_subscription_fini(&subscriber, &node);
            rcl_node_fini(&node);
            rclc_support_fini(&support);
            
            // Blink code for error: Slower to reduce CPU load
            statusLed.on(); delay(500); statusLed.off(); delay(500);
        }
    } else {
        rcl_ret_t ret = rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
        if (ret != RCL_RET_OK) {
            micro_ros_init_successful = false;
        }
    }
}