#ifndef _bsp_H_
#define _bsp_H_

#include  <msp430g2553.h>          // MSP430x2xx


#define   debounceVal      1000     //500     //250
#define   LEDs_SHOW_RATE   0xFFFF  // 62_5ms

#define LCD_port2_Sel      P2SEL

// LEDs abstraction
#define RGBsArrPort        P2OUT
#define RGBsArrPortDir     P2DIR
#define RGBsArrPortSel     P2SEL

#define LDROUT             P1OUT
#define LDRDIR             P1DIR
#define LDRSEL             P1SEL

// SERVO Abstraction
#define SERVODIR           P2DIR
#define SERVOSEL           P2SEL
#define SERVOSEL2          P2SEL2


// Echo Abstraction
#define ECHODIR            P2DIR
#define ECHOSEL            P2SEL
#define ECHOSEL2           P2SEL2


// Trigger Abstraction
#define TRIGGERDIR         P2DIR
#define TRIGGERSEL         P2SEL
#define TRIGGERSEL2        P2SEL2



// LCDs abstraction
#define LCDsArrPort        P1OUT
#define LCDsArrPortDir     P1DIR
#define LCDsArrPortSel     P1SEL
#define LCD_port2_Sel      P2SEL

// PushButtons abstraction
#define PBsArrPort         P2IN
#define PBsArrIntPend      P2IFG
#define PBsArrIntEn        P2IE
#define PBsArrIntEdgeSel   P2IES
#define PBsArrPortSel      P2SEL
#define PBsArrPortDir      P2DIR
#define PB0                0x01
#define PB1                0x02
#define PB2                0x04

extern void GPIOconfig(void);
extern void TIMERconfig(void);
extern void ADCconfig(void);

#endif



