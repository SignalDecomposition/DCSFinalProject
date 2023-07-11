#include  "../header/api.h"    		// private library - API layer
#include  "../header/app.h"    		// private library - APP layer

enum FSMstate state;
enum SYSmode lpm_mode;


void main(void){
  
  state = state0;  // start in idle state on RESET
  lpm_mode = mode0;     // start in idle state on RESET
  sysConfig();
  
  while(1){
	switch(state){
	case state0:
	    enterLPM(lpm_mode);
	    break;
	  case state1:
	      ObjectsDetectorSystem(20);
          P2OUT |= BIT7;
	      break;
      case state2:
            LIDR_test();
            break;
        case state3:
            LIDR_Clib();
            break;
        case state4:
            Telemeter(0);
            break;
	}
  }
}
  
  
  
  
  
  
