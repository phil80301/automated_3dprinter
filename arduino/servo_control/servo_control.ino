#include <Servo.h>

Servo left_servo;
Servo right_servo;

#define LEFT_SERVO_PIN 5
#define RIGHT_SERVO_PIN 6

#define LEFT_SERVO_DEFAULT_US 1500
#define RIGHT_SERVO_DEFAULT_US 1500
#define LIMIT_SWITCH 12


int switch_val;
void setup() {
  Serial.begin(115200);
  // Setting Up Servos
  left_servo.attach(LEFT_SERVO_PIN);
  right_servo.attach(RIGHT_SERVO_PIN);
  //left_servo.writeMicroseconds(LEFT_SERVO_DEFAULT_US);
  //right_servo.writeMicroseconds(RIGHT_SERVO_DEFAULT_US);

  // Setting up LimitSwitch
  pinMode(LIMIT_SWITCH, INPUT);
  switch_val = 0;
  Serial.println("Ready");
}

int mode = -1;

void open90(){
  right_servo.write(180);
  delay(10);
  left_servo.write(180);
  delay(10);  
}


void close90(){
  right_servo.write(92);
  delay(10);
  left_servo.write(92);
  delay(10);  
}


void flexup(){
  right_servo.write(92-45);
  left_servo.write(92+45);
}



void flexdown(){
  right_servo.write(0);
  left_servo.write(0);
}


void flat(){
  right_servo.write(0);
  left_servo.write(0);
}
int count = 0;
void loop() {
    count = count + 1;
    if(digitalRead(LIMIT_SWITCH) == HIGH){
      switch_val = 0;
    } else {
      switch_val = 1;
    }

    if (count%1000 == 1) {
      //Serial.println(switch_val);
    }

    if (Serial.available() > 0) {
      int read_value = Serial.read();
      mode = read_value - 48;
      switch(mode) {
        case 0:
          open90();
          Serial.println("done");
          break;
        case 1:
          close90();
          Serial.println("done");
          break;
        case 2:
          flexup();
          Serial.println("done");
          break;
        case 3:
          flexdown();
          Serial.println("done");
          break;
        case 4:
          flat();
          Serial.println("done");
          break;
      }
      delay(1000);  
    }

}

