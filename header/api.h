#ifndef _api_H_
#define _api_H_

#include  "../header/halGPIO.h"     // private library - HAL layer

extern void Telemeter();
extern void ObjectsDetectorSystem(unsigned int steps);
extern void LIDR();
extern void LDR_Scan(unsigned int steps);
extern void LIDR_Clib();
extern void printIntToLCD(unsigned int temp);
extern unsigned int  QFangle(unsigned int angle_in);
#endif







