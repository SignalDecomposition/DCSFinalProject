#ifndef _halGPIO_H_
#define _halGPIO_H_

#include  "../header/bsp.h"    		// private library - BSP layer
#include  "../header/app.h"    		// private library - APP layer
#include  "../header/LCD.h"

extern enum FSMstate state;   // global variable
extern enum SYSmode lpm_mode; // global variable

extern unsigned int REdge, FEdge;
extern unsigned int count, index;
extern unsigned char first;
extern char char_array[4];
extern int adcVal[4];
extern int LIDARarr [2][50];


extern void sysConfig(void);
extern void delay(unsigned int);
extern void enterLPM(unsigned char);
extern void enable_interrupts();
extern void disable_interrupts();
extern void Enable_TRIGGER();
extern void Disable_TRIGGER();
extern void Enable_SERVO(unsigned int t);
extern void Disable_SERVO();
extern void Enable_ECHO();
extern void Disable_ECHO();
extern void ADC_enable();
extern void ADC_touch();
extern void to_char(unsigned int t);

extern __interrupt void Timer0_A0_ISR (void);
extern __interrupt void Timer1_A1_ISR (void);
extern __interrupt void ADC10_ISR(void);
extern __interrupt void USCI0RX_ISR(void);
extern __interrupt void USCI0TX_ISR(void);
extern __interrupt void PBs_handler(void);




#endif







