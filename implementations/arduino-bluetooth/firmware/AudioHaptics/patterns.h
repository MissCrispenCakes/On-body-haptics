/**
 * On-Body Haptics - Pattern Definitions
 *
 * Pre-programmed haptic patterns for the wearable system.
 * Add your custom patterns here.
 */

#ifndef PATTERNS_H
#define PATTERNS_H

#include "config.h"

// Array of motor pins for easy iteration
const int motorPins[NUM_MOTORS] = {
  MOTOR_1_PIN,
  MOTOR_2_PIN,
  MOTOR_3_PIN,
  MOTOR_4_PIN,
  MOTOR_5_PIN
};

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Turn all motors off
 */
void allMotorsOff() {
  for (int i = 0; i < NUM_MOTORS; i++) {
    digitalWrite(motorPins[i], LOW);
  }
}

/**
 * Turn all motors on at specified intensity
 */
void allMotorsOn(int intensity = MOTOR_INTENSITY_HIGH) {
  for (int i = 0; i < NUM_MOTORS; i++) {
    analogWrite(motorPins[i], intensity);
  }
}

/**
 * Activate a single motor
 */
void activateMotor(int motorIndex, int intensity = MOTOR_INTENSITY_HIGH) {
  if (motorIndex >= 0 && motorIndex < NUM_MOTORS) {
    analogWrite(motorPins[motorIndex], intensity);
  }
}

// ============================================
// PATTERN FUNCTIONS
// ============================================

/**
 * Clockwise rotation pattern
 */
void patternClockwise() {
  allMotorsOff();
  for (int i = 0; i < NUM_MOTORS; i++) {
    activateMotor(i, MOTOR_INTENSITY_HIGH);
    delay(ROTATION_SPEED);
    allMotorsOff();
  }
}

/**
 * Counter-clockwise rotation pattern
 */
void patternCounterClockwise() {
  allMotorsOff();
  for (int i = NUM_MOTORS - 1; i >= 0; i--) {
    activateMotor(i, MOTOR_INTENSITY_HIGH);
    delay(ROTATION_SPEED);
    allMotorsOff();
  }
}

/**
 * Pulse all motors simultaneously
 */
void patternPulse() {
  allMotorsOn(MOTOR_INTENSITY_HIGH);
  delay(PULSE_DURATION);
  allMotorsOff();
  delay(PULSE_DURATION);
  allMotorsOn(MOTOR_INTENSITY_HIGH);
  delay(PULSE_DURATION);
  allMotorsOff();
}

/**
 * Wave pattern (low to high intensity)
 */
void patternWave() {
  for (int intensity = MOTOR_INTENSITY_LOW; intensity <= MOTOR_INTENSITY_HIGH; intensity += 20) {
    allMotorsOn(intensity);
    delay(50);
  }
  for (int intensity = MOTOR_INTENSITY_HIGH; intensity >= MOTOR_INTENSITY_LOW; intensity -= 20) {
    allMotorsOn(intensity);
    delay(50);
  }
  allMotorsOff();
}

// ============================================
// CUSTOM PATTERN SLOTS
// ============================================
// Add your custom patterns below

void customPattern1() {
  // Example: Alternating motors
  for (int i = 0; i < NUM_MOTORS; i += 2) {
    activateMotor(i, MOTOR_INTENSITY_HIGH);
  }
  delay(PATTERN_STEP_DELAY);
  allMotorsOff();

  for (int i = 1; i < NUM_MOTORS; i += 2) {
    activateMotor(i, MOTOR_INTENSITY_HIGH);
  }
  delay(PATTERN_STEP_DELAY);
  allMotorsOff();
}

void customPattern2() {
  // Add your pattern here
  // Example: Double pulse
  patternPulse();
  delay(200);
  patternPulse();
}

void customPattern3() {
  // Add your pattern here
  allMotorsOff();
}

void customPattern4() {
  // Add your pattern here
  allMotorsOff();
}

void customPattern5() {
  // Add your pattern here
  allMotorsOff();
}

void customPattern6() {
  // Add your pattern here
  allMotorsOff();
}

void customPattern7() {
  // Add your pattern here
  allMotorsOff();
}

/**
 * Execute pattern by name (called from main sketch)
 */
void executePattern(String patternName) {
  patternName.trim();
  patternName.toUpperCase();

  if (DEBUG_PRINT_PATTERNS) {
    Serial.print("Executing pattern: ");
    Serial.println(patternName);
  }

  if (patternName == "CW") {
    patternClockwise();
  }
  else if (patternName == "CCW") {
    patternCounterClockwise();
  }
  else if (patternName == "PULSE") {
    patternPulse();
  }
  else if (patternName == "WAVE") {
    patternWave();
  }
  else if (patternName == "CUSTOM1") {
    customPattern1();
  }
  else if (patternName == "CUSTOM2") {
    customPattern2();
  }
  else if (patternName == "CUSTOM3") {
    customPattern3();
  }
  else if (patternName == "CUSTOM4") {
    customPattern4();
  }
  else if (patternName == "CUSTOM5") {
    customPattern5();
  }
  else if (patternName == "CUSTOM6") {
    customPattern6();
  }
  else if (patternName == "CUSTOM7") {
    customPattern7();
  }
  else if (patternName == "OFF") {
    allMotorsOff();
  }
  else {
    if (DEBUG_MODE) {
      Serial.print("Unknown pattern: ");
      Serial.println(patternName);
    }
  }
}

#endif // PATTERNS_H
