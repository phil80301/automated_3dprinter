#include <AccelStepper.h>

#define STEPPER_STEP 2
#define STEPPER_DIR 3
#define STEPPER_ENABLE 4
#define LIMIT_SWITCH 10

#define NUM_INDEXES 4
#define HOMING_TIMEOUT 5000
#define TOP_POS 3500
#define DEBOUNCE_TIMEOUT 50
#define DEFAULT_SPEED 250
#define PRECISE_POSITIONING_SPEED 100
#define OFFSET_SPEED 100

AccelStepper stepper(1, STEPPER_STEP, STEPPER_DIR);

/* We assume the carriage starts at the home position (index 0) */
int current_index = 0;
int last_move_direction = 0;
int current_offset = 0;

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
 * Offset the carriage
 */
void offset(int steps) {
  stepper.setMaxSpeed(OFFSET_SPEED);
  digitalWrite(STEPPER_ENABLE, LOW);

  stepper.move(steps);

  while (stepper.run());

  current_offset += steps;
}

/**
 * Undo the offset
 */
void undoOffset() {
  if (current_offset != 0) {
    stepper.setMaxSpeed(OFFSET_SPEED);
    digitalWrite(STEPPER_ENABLE, LOW);

    stepper.move(-current_offset);

    while (stepper.run());

    current_offset = 0;
  }
}

/**
 * Moves the limit switch to just above the screw at the current index
 */
void doPrecisePositioning() {
  undoOffset();
  
  stepper.setMaxSpeed(PRECISE_POSITIONING_SPEED);
  digitalWrite(STEPPER_ENABLE, LOW);
  
  if (digitalRead(LIMIT_SWITCH) == HIGH) {
    /* Need to move into the screw first */

    if (last_move_direction == 1) {
      /* Need to move down */

      stepper.moveTo(0);

      while (digitalRead(LIMIT_SWITCH) != LOW) {
        stepper.run();
      }

      stepper.stop();

      while (stepper.run());
    } else {
      /* Need to move up */

      stepper.moveTo(TOP_POS);

      while (digitalRead(LIMIT_SWITCH) != LOW) {
        stepper.run();
      }

      stepper.stop();

      while (stepper.run());
    }
  }

  /* Now we are inside the screw, move up */

  stepper.moveTo(TOP_POS);

  while (digitalRead(LIMIT_SWITCH) != HIGH) {
    stepper.run();
  }

  stepper.stop();

  while (stepper.run());
}

/**
 * Moves to the desired index
 */
void moveToIndex(int index) {
  long start_time;

  undoOffset();
  
  stepper.setMaxSpeed(DEFAULT_SPEED);
  digitalWrite(STEPPER_ENABLE, LOW);

  if (index > current_index) {
    /* Need to move up */
    stepper.moveTo(TOP_POS);

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

    last_move_direction = 1;
    doPrecisePositioning();
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

      last_move_direction = -1;
      doPrecisePositioning();
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

void handleOffsetCommand() {
  int offset_steps = Serial.parseInt();
  if (offset_steps >= 0) {
    offset(offset_steps);
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

  stepper.setMaxSpeed(DEFAULT_SPEED);
  stepper.setAcceleration(1500.0);

  home();

  Serial.println("Ready");
}

void loop() {
  switch(Serial.read()) {
    case 'i':
      handleIndexCommand();
      break;
    case 'o':
      handleOffsetCommand();
      break;
    case 'h':
      handleHomeCommand();
      break;
    default:
      break;
  }
}
