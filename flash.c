/**************************************************************************/
/*       Flash memory programming with the CPU executing the      */
/*               code in the flash memory                                 */
/*                                                                        */
/*                                                                        */
/* MSP430 Teaching ROM                                                    */
/* Produced by: MSP430@UBI Group - www.msp430.ubi.pt                      */
/*                                                                        */
/* Exercise: Using the MSP-EXP430FG4618 Development Tool implement        */
/*           a flash memory programming with the CPU executing the        */
/*           code in the flash memory.                                    */
/*                                                                        */
/* Instructions:                                                          */
/*                                                                        */
/* This lab requires to configure:                                        */
/*  - Flash memory controller                                             */
/*  - Segment erase routine                                               */
/*  - Flash write routine                                                 */
/*                                                                        */
/* The execution time of the different operations can be obtained with    */
/* an oscilloscope connected on pin 2 of the Header 4 or analyzing the    */
/* state of the LED (digital output P2.1)                                 */
/*                                                                        */
/*                                                                        */
/*                                        Copyright by Texas Instruments  */
/**************************************************************************/


#include <msp430xG46x.h>

#define infomation_seg_A 0x1000
#define infomation_seg_B 0x1080
#define seg_length 0x0032

unsigned char i = 0x00, bla;

struct FileSystem{
    int  FilesCount;
    char *FilesNames[3];
    char *FilesStart[3];
    int  FilesSizes[3];
};

//*************************************************************************
// TEST READING FROM FLASH
//*************************************************************************
void read_data(int adress)
{
  char *Flash_ptr;                          // Flash pointer

  Flash_ptr = (char *)adress;               // Initialize Flash pointer

  if (*Flash_ptr == 1)                       // test value in adress
      P2OUT |= BIT1;

}
//*************************************************************************
// Erase segment  
//*************************************************************************
void erase_segment(int adress)
{
  int *Flash_ptr;                           // Flash pointer

  Flash_ptr = (int *)adress;                // Initialize Flash pointer
  FCTL1 = FWKEY + ERASE;                    // Set Erase bit
  FCTL3 = FWKEY;                            // Clear Lock bit
  
  *Flash_ptr = 0;                           // Dummy write to erase Flash segment
  
  FCTL3 = FWKEY + LOCK;                     // Set LOCK bit
}
//************************************************************************
// Write char in flash
//************************************************************************
void write_char_flash(int adress, char value)
{
  char *Flash_ptr;                          // Flash pointer

  Flash_ptr = (char *)adress;               // Initialize Flash pointer
  FCTL3 = FWKEY;                            // Clear Lock bit
  FCTL1 = FWKEY + WRT;                      // Set WRT bit for write operation
  
  *Flash_ptr = value;                       // Write value to flash
  
  FCTL1 = FWKEY;                            // Clear WRT bit
  FCTL3 = FWKEY + LOCK;                     // Set LOCK bit
}
//************************************************************************
// Write integer in flash
//************************************************************************
void write_int_flash(int adress, int value)
{
  int *Flash_ptr;                           // Flash pointer

  Flash_ptr = (int *)adress;                // Initialize Flash pointer
  FCTL3 = FWKEY;                            // Clear Lock bit
  FCTL1 = FWKEY + WRT;                      // Set WRT bit for write operation
  
  *Flash_ptr = value;                       // Write value to flash
  
  FCTL1 = FWKEY;                            // Clear WRT bit
  FCTL3 = FWKEY + LOCK;                     // Set LOCK bit
}
//************************************************************************
// Copy data from one segment to another
//************************************************************************
void copy_seg_flash(int adress_source, int adress_destiny)
{
  int *Flash_ptr_A;                         // Segment Information A pointer
  int *Flash_ptr_B;                         // Segment D pointer
  unsigned char i;

  Flash_ptr_A = (int *)adress_source;       // Initialize Flash segment C pointer
  Flash_ptr_B = (int *)adress_destiny;      // Initialize Flash segment D pointer
  FCTL1 = FWKEY + ERASE;                    // Set Erase bit
  FCTL3 = FWKEY;                            // Clear Lock bit
  *Flash_ptr_B = 0;                         // Dummy write to erase Flash segment D
  FCTL1 = FWKEY + WRT;                      // Set WRT bit for write operation

  for (i=0; i<seg_length; i = i + 2)
  {
    *Flash_ptr_B++ = *Flash_ptr_A++;        // copy value segment C to segment D
  }

  FCTL1 = FWKEY;                            // Clear WRT bit
  FCTL3 = FWKEY + LOCK;                     // Set LOCK bit
}
//***********************************************************************
// Main
//***********************************************************************
void main(void)
{
  WDTCTL = WDTPW + WDTHOLD;                 // Stop watchdog timer
  
  P2DIR |= 0x02;                            // P2.1 output 
  P2OUT &= ~0x02;

  FCTL2 = FWKEY + FSSEL0 + FN1;             // MCLK/3 for Flash Timing Generator
  
  P4SEL |= 0x03;                            // P4.1,0 = USART1 TXD/RXD
  ME2 |= UTXE1 + URXE1;                     // Enable USART1 TXD/RXD
  U1CTL |= CHAR;                            // 8-bit character
  U1TCTL |= SSEL0;                          // UCLK = ACLK
  U1BR0 = 0x03;                             // 32k/9600 - 3.41
  U1BR1 = 0x00;                             //
  U1MCTL = 0x4A;                            // Modulation
  U1CTL &= ~SWRST;                          // Initialize USART state machine
  IE2 |= URXIE1;                            // Enable USART1 RX interrupt

  erase_segment(infomation_seg_A);          // Erase flash Information A and B
  while(1){
      _BIS_SR(LPM0_bits + GIE);                 // Enter LPM3 w/ interrupt
      write_char_flash(infomation_seg_A + i,bla);
      i++;
      if (i == 5)
          break;
  }

  while(1){
      _NOP();
  }


 /*
  erase_segment(infomation_seg_B);

  i = 1;
  write_char_flash(infomation_seg_A,i);

  for(i = 0; i< seg_length; i++)            // write information A with byte data
  {
  	write_char_flash(infomation_seg_A + i,i);
  }
  

  for(i = 0; i< seg_length; i = i + 2)      // write information B with word data
  {
  	write_int_flash(infomation_seg_B + i,i);
  }


  P2OUT ^= 0x02;                                        // Toogle P2.1
  erase_segment(infomation_seg_B);                      // Erase again Information B
  copy_seg_flash(infomation_seg_A, infomation_seg_B);	// copy contents from Information A to Information B
  P2OUT ^= 0x02;                                        // Toogle P2.1


  struct FileSystem f;
  f.FilesCount = 1;
  f.FilesStart[0] = (char *)infomation_seg_A;
  if (*f.FilesStart[0] == 0)
      P2OUT ^= 0x02;
*/

}

#pragma vector=USART1RX_VECTOR
__interrupt void USART1_rx (void)
{
  TXBUF1 = RXBUF1;                          // RXBUF1 to TXBUF1
  bla = RXBUF1;
  P2OUT ^= 0x02;
  _BIC_SR_IRQ(LPM0_bits);                   // Clear LPM3 bits from 0(SR)
}

