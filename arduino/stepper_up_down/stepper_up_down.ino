// ConstantSpeed.pde
// -*- mode: C++ -*-
//
// Shows how to run AccelStepper in the simplest,
// fixed speed mode with no accelerations
/// \author  Mike McCauley (mikem@airspayce.com)
// Copyright (C) 2009 Mike McCauley
// $Id: ConstantSpeed.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

#include <AccelStepper.h>

AccelStepper stepper(1, 3, 4); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5


void setup()
{  
  stepper.setMaxSpeed(1000000);
  stepper.setSpeed(-1000000);	
  
}

void switch_up(){
   stepper.setSpeed(-100000);
}

void switch_down(){
   stepper.setSpeed(100000);
}

void loop()
{  
  unsigned long start_time = millis();
  unsigned int length_time = 5000;
  switch_up();
  while(millis() - start_time < length_time){
    stepper.runSpeed();    
  }
  switch_down();
  while(millis() - start_time < 2 * length_time){
    stepper.runSpeed();    
  }
  
}
