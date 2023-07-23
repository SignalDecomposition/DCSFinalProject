#include  "../header/halGPIO.h"     // private library - HAL layer
#include  "../header/bsp.h"
#include  "../header/LCD.h"

unsigned int REdge = 0,FEdge = 0;
unsigned int count = 0, index = 0;
unsigned char first = 0x0;
int first_time = 0;
char char_array[4] = {'\0','\0','\0','\0'};
char angle_string[5];
int adcVal[4];
int LIDARarr [2][50];


//--------------------------------------------------------------------
//             System Configuration  
//--------------------------------------------------------------------
void sysConfig(void){ 
	GPIOconfig();
	TIMERconfig();
	//ADCconfig();
	lcd_init();

} 

//---------------------------------------------------------------------
//            Polling based Delay function
//---------------------------------------------------------------------
void delay(unsigned int t){  // t[msec]
	volatile unsigned int i;
	
	for(i=t; i>0; i--);
}
//---------------------------------------------------------------------
//            Enter from LPM0 mode
//---------------------------------------------------------------------
void enterLPM(unsigned char LPM_level){
	if (LPM_level == 0x00) 
	  _BIS_SR(LPM0_bits);     /* Enter Low Power Mode 0 */
        else if(LPM_level == 0x01) 
	  _BIS_SR(LPM1_bits);     /* Enter Low Power Mode 1 */
        else if(LPM_level == 0x02) 
	  _BIS_SR(LPM2_bits);     /* Enter Low Power Mode 2 */
	else if(LPM_level == 0x03) 
	  _BIS_SR(LPM3_bits);     /* Enter Low Power Mode 3 */
        else if(LPM_level == 0x04) 
	  _BIS_SR(LPM4_bits);     /* Enter Low Power Mode 4 */
}
//---------------------------------------------------------------------
//            Enable interrupts
//---------------------------------------------------------------------
void enable_interrupts(){
  _BIS_SR(GIE);
}
//---------------------------------------------------------------------
//            Disable interrupts
//---------------------------------------------------------------------
void disable_interrupts(){
  _BIC_SR(GIE);
}

void Enable_TRIGGER(){

    TA1CCR1 = 50;
    TA1CTL |= MC_1 + TACLR;
}

void Disable_TRIGGER(){

    TA1CCR1 = 0;
    TA1CTL |= MC_0;
}

void Enable_ECHO(){

    REdge = 0;
    FEdge = 0;
    TA1CCTL2 |= CCIE;
}

void Disable_ECHO(){

    TA1CCTL2 &= ~CCIE;
}

void Enable_SERVO(unsigned int t){

    TA0CCR1 = t;
    TA0CTL |= MC_1 + TACLR;
    TA0CCTL0 |= CCIE;

}

void Disable_SERVO(){
    TA0CTL |= MC_0;
    TA0CCTL0 &= ~CCIE;
    TA0CCR1 = 0;


}

void ADC_enable(){
    ADC10CTL1 = INCH_3 + CONSEQ_1;            // A3/A0, single sequence
    //VCC and VSS, 32 x ADC10CLKs,Reference generator, ADC10ON, interrupt enabled, Multiple sample and conversion
    ADC10CTL0 = ADC10SHT_2 + MSC + ADC10ON + ADC10IE;

    ADC10DTC1 = 0x04;    // 2 converstions
    ADC10AE0 |= 0x09;   //BIT3 + BIT0; // input enable A3, A0
}

void transmite_UART(int size_tran){

    while(index < size_tran ){

        while (!(IFG2&UCA0TXIFG));                // USCI_A0 TX buffer ready?
        UCA0TXBUF = char_array[index];
        index++;

    }

       index = 0;

}

void ADC_touch(){
    while (ADC10CTL1 & ADC10BUSY);               // Wait if ADC10 core is active
    ADC10SA = (int)adcVal;
    ADC10CTL0 |= ENC + ADC10SC;      // Enable conversion, Sampling and conversion start
    enterLPM(lpm_mode);             // LPM0, ADC10_ISR will force exit
    ADC10CTL0 &= ~ADC10SC;

}

void to_char(unsigned int t){
    if(t < 256){
        char_array[0] = t & 0xFF;
        char_array[1] = 0x00;
    }else{
        char_array[0] = t & 0xFF;
        char_array[1] = (t >> 8) & 0xFF;
    }
}

#pragma vector=TIMER0_A0_VECTOR
__interrupt void Timer0_A0_ISR (void)
{
    //was: count < 50
    if(count < 30){
        count = count + 1;
    }else{
        count = 0;
        LPM0_EXIT;   // Exit LPM0
    }
}


#pragma vector=TIMER1_A1_VECTOR
__interrupt void Timer1_A1_ISR (void)
{
    switch(__even_in_range(TA1IV,0x0A)){

        case  TA1IV_TACCR2:
            if (TA1CCTL2 & CCI){
                REdge = TA1CCR2;
                first = 0x1;
            }
            else if(first) {
                FEdge = TA1CCR2;
                TA1CCTL2 &= ~CCIE;
                first = 0x0;
                LPM0_EXIT;   // Exit LPM0
            }
            break;

        default :
            break;

    }
}

// ADC10 interrupt service routine
#pragma vector=ADC10_VECTOR
__interrupt void ADC10_ISR(void)

{
    ADC10CTL0 &= ~ENC;
    ADC10CTL0 &= ~ADC10ON;
    LPM0_EXIT;      // Clear CPUOFF bit from 0(SR)
}


//  Echo back RXed character, confirm TX buffer is ready first
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(USCIAB0RX_VECTOR))) USCI0RX_ISR (void)
#else
#error Compiler not supported!
#endif
{
  //while (!(IFG2&UCA0TXIFG));                // USCI_A0 TX buffer ready?
  if (state == state1){
      char_array[index] = UCA0RXBUF;
      index++;
      if (char_array[index-1] == '\n'){
          index = 0;
          LPM0_EXIT;
      }
  }
  else if (state == state3){
      REdge = UCA0RXBUF;
      IE2 |= UCA0TXIE;
  }
  else if (state == state4 && first_time){

        angle_string[index] = UCA0RXBUF;
        index++;
        if (angle_string[index-1] == '\n'){
            first_time = 0;
            index = 0;
            LPM0_EXIT;
        }
    }
  else if (UCA0RXBUF == '0'){
      state = state0;

    }
  else if (UCA0RXBUF == '1'){
      state = state1;
      index = 0;
  }
  else if (UCA0RXBUF == '2'){
      state = state2;
      LPM0_EXIT;
  }
  else if (UCA0RXBUF == '3'){
      state = state3;
      UCA0TXBUF = '3';
      LPM0_EXIT;
  }
  else if (UCA0RXBUF == '4'){
       state = state4;
       first_time = 1;
       LPM0_EXIT;
  }
  else if (UCA0RXBUF == '5'){
         state = state5;
         LPM0_EXIT;
    }


}

#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=USCIAB0TX_VECTOR
__interrupt void USCI0TX_ISR(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(USCIAB0TX_VECTOR))) USCI0TX_ISR (void)
#else
#error Compiler not supported!
#endif
{
    while(char_array[index] != '\0'){
        while (!(IFG2&UCA0TXIFG));                // USCI_A0 TX buffer ready?
        UCA0TXBUF = char_array[index];
        index++;
    }

    index = 0;
    IE2 &= ~UCA0TXIE;                       // Disable USCI_A0 TX interrupt
    LPM0_EXIT;
}

