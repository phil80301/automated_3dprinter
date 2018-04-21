#include <AccelStepper.h>

#define STEPPER_STEP 2
#define STEPPER_DIR 3
#define STEPPER_ENABLE 4
#define LIMIT_SWITCH 10

#define NUM_INDEXES 4
#define HOMING_TIMEOUT 3000
#define FAR_POS 1000000
#define DEBOUNCE_TIMEOUT 50

AccelStepper stepper(1, STEPPER_STEP, STEPPER_DIR);

/* We assume the carriage starts at the home position (index 0) */
int current_index = 0;

/**
 * Finds the home position by letting the carriage fall
 * Homing is complete when the limit switch is released for more than HOMING_TIMEOUT milliseconds
 */
void home() {
  digitalWrite(STEPPER_ENABLE, HIGH);

  unsigned long start_time = millis();
  unsigned long current_time;

  do {
    current_time = millis();

    if (digitalRead(LIMIT_SWITCH) == LOW) {
      start_time = current_time; // Reset timeout
    }
  } while (current_time - start_time < HOMING_TIMEOUT);

  stepper.setCurrentPosition(0);
  current_index = 0;
}

/**
 * Moves to the desired index
 */
void moveToIndex(int index) {
  long start_time;

  digitalWrite(STEPPER_ENABLE, LOW);

  if (index > current_index) {
    /* Need to move up */
    stepper.moveTo(FAR_POS);

    while (current_index != index) {
      start_time = millis();
      while (millis() - start_time < DEBOUNCE_TIMEOUT) {
        stepper.run();
      }
  
      while (digitalRead(LIMIT_SWITCH) != HIGH) {
        stepper.run();
      }

      start_time = millis();
      while (millis() - start_time < DEBOUNCE_TIMEOUT) {
        stepper.run();
      }
      
      while (digitalRead(LIMIT_SWITCH) != LOW) {
        stepper.run();
      }

      current_index++;
    }

    stepper.stop();

    while (stepper.run());
  } else if (index < current_index) {
    /* Need to move down */
    stepper.moveTo(0);

    if (index == 0) {
      /* Special case: index == 0, simply run to completion */
      while (stepper.run());
      current_index = 0;
    } else {
      while (digitalRead(LIMIT_SWITCH) != LOW) {
        stepper.run();
      }
      
      while (current_index != index) {
        start_time = millis();
        while (millis() - start_time < DEBOUNCE_TIMEOUT) {
          stepper.run();
        }
    
        while (digitalRead(LIMIT_SWITCH) != HIGH) {
          stepper.run();
        }
  
        start_time = millis();
        while (millis() - start_time < DEBOUNCE_TIMEOUT) {
          stepper.run();
        }
        
        while (digitalRead(LIMIT_SWITCH) != LOW) {
          stepper.run();
        }
  
        current_index--;
      }
  
      stepper.stop();
  
      while (stepper.run());
    }
  } else {
    /* Already at the right index, don't do anything */
  }
}

void handleIndexCommand() {
  int target_index = Serial.parseInt();
  if (target_index >= 0 && target_index <= NUM_INDEXES) {
    moveToIndex(target_index);
    Serial.println("OK");
  } else {
    Serial.println("Error");
  }
}

void handleHomeCommand() {
  home();
  Serial.println("OK");
}

void setup() {
  Serial.begin(115200);

  pinMode(STEPPER_ENABLE, OUTPUT);
  digitalWrite(STEPPER_ENABLE, HIGH); // Make sure stepper is not enabled
  pinMode(LIMIT_SWITCH, INPUT_PULLUP);

  stepper.setMaxSpeed(250);
  stepper.setAcceleration(1500.0);

  home();

  Serial.println("Ready");
}

void loop() {
  switch(Serial.read()) {
    case 'i':
      handleIndexCommand();
      break;
    case 'h':
      handleHomeCommand();
      break;
    default:
      break;
  }
}
