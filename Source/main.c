#include  "../header/api.h"    		// private library - API layer
#include  "../header/app.h"    		// private library - APP layer

enum FSMstate state;
enum SYSmode lpm_mode;



void main(void){
  

  state = state0;  // start in idle state on RESET
  lpm_mode = mode0;     // start in idle state on RESET
  sysConfig();
  int j;
  int steps = 30;
  int cycles_in;
  Enable_SERVO(450);
  enterLPM(lpm_mode);
  enterLPM(lpm_mode);
  Disable_SERVO();

  while(1){
	switch(state){
	    case state0:
            enterLPM(lpm_mode);
            break;
	    case state1:
            // 0 degrees is 450 and 180 degrees is 2140
            ObjectsDetectorSystem(60);
            break;
	    case state2:
	        LDR_Scan(60);
            break;
        case state3:
            LIDR_Clib();
            break;
        case state4:
            Telemeter();
            break;
        case state5:
            Script_Mode();
            break;
        case state6:
            //TBD bounes
            break;
	}
  }
}
  
  
  
  
  
  
