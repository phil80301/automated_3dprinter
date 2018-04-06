#include <Servo.h>

Servo left_servo;
Servo right_servo;

#define LEFT_SERVO_PIN 9
#define RIGHT_SERVO_PIN 10

#define LEFT_SERVO_DEFAULT_US 1500
#define RIGHT_SERVO_DEFAULT_US 1500

void setup() {
  Serial.begin(115200);
  left_servo.attach(LEFT_SERVO_PIN);
  right_servo.attach(RIGHT_SERVO_PIN);
  left_servo.writeMicroseconds(LEFT_SERVO_DEFAULT_US);
  right_servo.writeMicroseconds(RIGHT_SERVO_DEFAULT_US);

  Serial.println("Ready");
}

void loop() {
  switch(Serial.read()) {
    case 'a':
      left_servo.writeMicroseconds(Serial.parseInt());
      break;
    case 'b':
      right_servo.writeMicroseconds(Serial.parseInt());
      break;
  }
}

