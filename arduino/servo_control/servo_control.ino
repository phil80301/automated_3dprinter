#include <Servo.h>

Servo left_servo;
Servo right_servo;

#define LEFT_SERVO_PIN 9
#define RIGHT_SERVO_PIN 10

#define LEFT_SERVO_OPEN_US 400
#define RIGHT_SERVO_OPEN_US 300

#define LEFT_SERVO_CLAMP_US 1300
#define RIGHT_SERVO_CLAMP_US 1200

#define LEFT_SERVO_FLEX_US 900
#define RIGHT_SERVO_FLEX_US 1700

void eject() {
  left_servo.writeMicroseconds(LEFT_SERVO_OPEN_US);
  right_servo.writeMicroseconds(RIGHT_SERVO_OPEN_US);
  delay(2000);
  left_servo.writeMicroseconds(LEFT_SERVO_CLAMP_US);
  right_servo.writeMicroseconds(RIGHT_SERVO_CLAMP_US);
  delay(5000);
  left_servo.writeMicroseconds(LEFT_SERVO_FLEX_US);
  right_servo.writeMicroseconds(RIGHT_SERVO_FLEX_US);
  delay(2000);
  left_servo.writeMicroseconds(LEFT_SERVO_CLAMP_US);
  right_servo.writeMicroseconds(RIGHT_SERVO_CLAMP_US);
  delay(2000);
  left_servo.writeMicroseconds(LEFT_SERVO_OPEN_US);
  right_servo.writeMicroseconds(RIGHT_SERVO_OPEN_US);
}

void setup() {
  Serial.begin(115200);
  left_servo.attach(LEFT_SERVO_PIN);
  right_servo.attach(RIGHT_SERVO_PIN);
  left_servo.writeMicroseconds(LEFT_SERVO_OPEN_US);
  right_servo.writeMicroseconds(RIGHT_SERVO_OPEN_US);

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
    case 'e':
      eject();
      break;
  }
}

