#include  "../header/api.h"    		// private library - API layer
#include  "../header/app.h"    		// private library - APP layer

enum FSMstate state;
enum SYSmode lpm_mode;


void main(void){
  
  state = state1;  // start in idle state on RESET
  lpm_mode = mode0;     // start in idle state on RESET
  sysConfig();
  int j;
  int steps = 30;
  int cycles_in;

  while(1){
	switch(state){
	    case state0:
            enterLPM(lpm_mode);
            break;
	    case state1:
            // 0 degrees is 460 and 180 degrees is 2170
            ObjectsDetectorSystem(30);
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
        case state5:
            //TBD script
            break;
	}
  }
}
  
  
  
  
  
  
