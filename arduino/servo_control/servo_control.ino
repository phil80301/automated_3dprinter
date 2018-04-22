#include <Servo.h>

Servo left_servo;
Servo right_servo;

#define LEFT_SERVO_PIN 5
#define RIGHT_SERVO_PIN 6

#define LEFT_SERVO_OPEN_ANGLE 180
#define RIGHT_SERVO_OPEN_ANGLE 180

#define LEFT_SERVO_CLOSE_ANGLE 85
#define RIGHT_SERVO_CLOSE_ANGLE 95

#define LEFT_SERVO_FLEX_ANGLE 120
#define RIGHT_SERVO_FLEX_ANGLE 60

void closeGripper() {
  left_servo.write(LEFT_SERVO_CLOSE_ANGLE);
  right_servo.write(RIGHT_SERVO_CLOSE_ANGLE);
  delay(1500);
}

void openGripper() {
  left_servo.write(LEFT_SERVO_OPEN_ANGLE);
  right_servo.write(RIGHT_SERVO_OPEN_ANGLE);
  delay(1500);
}

void flexGripper() {
  left_servo.write(LEFT_SERVO_FLEX_ANGLE);
  right_servo.write(RIGHT_SERVO_FLEX_ANGLE);
  delay(1500);
  left_servo.write(LEFT_SERVO_CLOSE_ANGLE);
  right_servo.write(RIGHT_SERVO_CLOSE_ANGLE);
  delay(1500);
}

void setup() {
  Serial.begin(115200);

  left_servo.attach(LEFT_SERVO_PIN);
  right_servo.attach(RIGHT_SERVO_PIN);
  left_servo.write(LEFT_SERVO_OPEN_ANGLE);
  right_servo.write(RIGHT_SERVO_OPEN_ANGLE);

  Serial.println("Ready");
}

void loop() {
  switch(Serial.read()) {
    case 'a':
      left_servo.write(Serial.parseFloat());
      Serial.println("OK");
      break;
    case 'b':
      right_servo.write(Serial.parseFloat());
      Serial.println("OK");
      break;
    case 'c':
      closeGripper();
      Serial.println("OK");
      break;
    case 'o':
      openGripper();
      Serial.println("OK");
      break;
    case 'f':
      flexGripper();
      Serial.println("OK");
      break;
    default:
      break;
  }
}

