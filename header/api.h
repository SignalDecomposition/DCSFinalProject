#ifndef _api_H_
#define _api_H_

#include  "../header/halGPIO.h"     // private library - HAL layer

extern void Telemeter(unsigned int angle);
extern void ObjectsDetectorSystem(unsigned int steps);
extern void LIDR();
extern void LIDR_test();
extern void LIDR_Clib();
extern void printIntToLCD(unsigned int temp);
#endif







