#ifndef _api_H_
#define _api_H_

#include  "../header/halGPIO.h"     // private library - HAL layer

extern struct FileSystem f;
extern unsigned char d;

extern void Telemeter(int x);
extern void ObjectsDetectorSystem(int l, int r);
extern void LIDR();
extern void LDR_Scan(unsigned int steps);
extern void LIDR_Clib();
extern void printIntToLCD(unsigned int temp);
extern unsigned int  QFangle(unsigned int angle_in);
extern void Script_Mode();
extern void flash();
extern void inc_lcd(int x);
extern void dec_lcd(int x);
extern void rra_lcd(char x);
extern void Bonus(int l, int r);
extern int charsToINT(char high, char low);
#endif






