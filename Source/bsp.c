#include  "../header/bsp.h"    // private library - BSP layer

//-----------------------------------------------------------------------------  
//           GPIO congiguration
//-----------------------------------------------------------------------------
void GPIOconfig(void){

    WDTCTL = WDTHOLD | WDTPW;       // Stop WDT

    PBsArrPortSel &= ~0x01;
    PBsArrPortDir &= ~0x01;
    PBsArrIntEdgeSel |= 0x01;  //pull-up mode
    PBsArrIntEn |= 0x01;
    PBsArrIntPend &= ~0x01;

    // TEST BIT
    P2SEL &= ~BIT0;
    P2DIR |= BIT0;
    P2OUT &= ~BIT0;


    //TRRIGER setup
    TRIGGERSEL |= BIT1;
    TRIGGERSEL2 &= ~BIT1;
    TRIGGERDIR |= BIT1;

    //ECHO setup
    ECHOSEL |= BIT5;
    ECHOSEL2 &= ~BIT5;
    ECHODIR &= ~BIT5;

    //SERVO SetUp
    SERVODIR |= BIT6;
    SERVOSEL |= BIT6;
    SERVOSEL &= ~BIT7;
    SERVOSEL2 &= ~BIT6 + ~BIT7;

    //UART SetUp
    P1SEL = BIT1 + BIT2 ;                     // P1.1 = RXD, P1.2=TXD
    P1SEL2 = BIT1 + BIT2 ;                     // P1.1 = RXD, P1.2=TXD
    P1OUT &= 0x00;
    UCA0CTL1 |= UCSSEL_3;                     // CLK = SMCLK
    UCA0BR0 = 109;                            // 2^20 / 9600 = 109.23
    UCA0BR1 = 0x00;
    UCA0MCTL = UCBRS0;                        //
    UCA0CTL1 &= ~UCSWRST;                     // **Initialize USCI state machine**
    IE2 |= UCA0RXIE;                          // Enable USCI_A0 RX interrupt

    //FLASH SetUp
    FCTL2 = FWKEY + FSSEL0 + FN1;             // MCLK/3 for Flash Timing Generator

  _BIS_SR(GIE);                     // enable interrupts globally
}                             
//------------------------------------------------------------------------------------- 
//            Timers congiguration 
//-------------------------------------------------------------------------------------

void TIMERconfig(void){

    // SERVO TIMER

    TA0CTL |= TASSEL_2 + MC_0 + ID_0;//SMCLK, UP MODE, DIV 1
    TA0CCR0 = 26500;
    TA0CCTL1 |= OUTMOD_7; // Reset-Set mode


    // ULTRA-SONIC TIMER

    // TRIGGER Config
    TA1CTL |= TASSEL_2 + MC_0 + ID_3; //SMCLK, UP MODE, DIV 8
    TA1CCR0 = 8650;
    TA1CCTL1 |= OUTMOD_7; // Reset-Set mode


    // ECHO Config
    TA1CCTL2 |= CAP + CM_3 + SCS + CCIS_1;




} 

//------------------------------------------------------------------------------------- 
//            ADC congiguration 
//-------------------------------------------------------------------------------------
void ADCconfig(void){
	
	//write here ADC congiguration code
}              

           
             

 
             
             
            
  

