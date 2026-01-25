/**
 * On-Body Haptics - Arduino Configuration
 *
 * Hardware configuration for haptic motors and serial communication.
 * Modify these values to match your hardware setup.
 */

#ifndef CONFIG_H
#define CONFIG_H

// ============================================
// SERIAL COMMUNICATION
// ============================================
#define SERIAL_BAUD 57600      // Must match server configuration
#define SERIAL_TIMEOUT 100     // milliseconds

// ============================================
// HAPTIC MOTOR PINS (PWM capable)
// ============================================
// Arduino Uno/Nano PWM pins: 3, 5, 6, 9, 10, 11
#define MOTOR_1_PIN 3
#define MOTOR_2_PIN 5
#define MOTOR_3_PIN 6
#define MOTOR_4_PIN 9
#define MOTOR_5_PIN 10

#define NUM_MOTORS 5

// ============================================
// PATTERN TIMING
// ============================================
#define PATTERN_STEP_DELAY 100   // milliseconds between pattern steps
#define PULSE_DURATION 200       // milliseconds for pulse pattern
#define ROTATION_SPEED 100       // milliseconds per motor in rotation

// ============================================
// PWM SETTINGS
// ============================================
#define MOTOR_INTENSITY_HIGH 255  // Full intensity
#define MOTOR_INTENSITY_MED 180   // Medium intensity
#define MOTOR_INTENSITY_LOW 100   // Low intensity
#define MOTOR_INTENSITY_OFF 0     // Off

// ============================================
// DEBUG
// ============================================
#define DEBUG_MODE false          // Set to true for serial debugging
#define DEBUG_PRINT_PATTERNS true // Print pattern names when triggered

// ============================================
// BLUETOOTH MODULE (HC-05/HC-06)
// ============================================
// HC-05/HC-06 uses hardware serial on Arduino Uno (pins 0, 1)
// or software serial on other pins
#define USE_HARDWARE_SERIAL true

// If using SoftwareSerial, define pins:
// #define BT_RX_PIN 10
// #define BT_TX_PIN 11

#endif // CONFIG_H
