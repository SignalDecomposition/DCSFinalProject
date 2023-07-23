#include  "../header/api.h"    		// private library - API layer
#include  "../header/halGPIO.h"     // private library - HAL layer

//T_on = 2^17 * (1.55m + 0.6m * arctan(10k*2.5m*angle/180 -2*pi))
unsigned int arr[21] = {79,80,82,84,86,90,94,102,113,133,168,214,248,268,283,294,301,306,309,311,313};

void Telemeter(unsigned int angle){
    unsigned int steps;
    steps = (angle >> 3) -1;
    ObjectsDetectorSystem(steps);
}
// Qformat angle
int QFangle(int angle_in){
    int timer_out;
    long temp_angle;
    long mult_QF = 1216;//9.5*2^7
    temp_angle = mult_QF*((long)angle_in);
    temp_angle = temp_angle >> 7;
    timer_out = (int)temp_angle;
    return timer_out;

}


void ObjectsDetectorSystem(unsigned int steps){
    unsigned int j = 0, max = 35;//450 original
    unsigned int dist, angle;
    unsigned char char_angle;
    int true_angle;
    int mult_step;
    Enable_SERVO(460);
    enterLPM(lpm_mode);
    mult_step = 180/steps;
    if (char_array[0] != 0){
        max = (char_array[2]+'0')*100 + (char_array[1]+'0')*10 + (char_array[0]+'0');
        char_array[0] = '\0';
        char_array[1] = '\0';
        char_array[2] = '\0';
        char_array[3] = '\0';
    }
    while(state == state1){

        for (j = 0 ; j <= steps ; j++){
            true_angle = j*mult_step;
            angle = QFangle(true_angle);
            lcd_home();


            Enable_SERVO(angle + 460);
            Enable_TRIGGER();
            Enable_ECHO();

            printIntToLCD(true_angle);//P1.0 LIDAR1
            enterLPM(lpm_mode);
            Disable_ECHO();
            Disable_TRIGGER();

            if(REdge != 0 || FEdge != 0){
                if (FEdge > REdge){
                    dist = (FEdge - REdge) << 3;
                }
                else{
                    dist = (REdge - FEdge) << 3;
                }
                dist = dist >> 6;
                if (17 < dist && dist < max)
                    char_angle = dist;
            }

            lcd_new_line;
            printIntToLCD(dist);//P1.3 LIDAR2

        }
        Disable_SERVO();
        state = state0;
    }
}

void LIDR(){

    char prevADC[6] = {'\0'}, ADC[6];
    long values[32];
    int i, flag = 0;
    int Q_fromat = 7; //2^7
    long SMA = 0, temp, mult = 32 ;
    int count_ADC = 0;
    long Qformat_val;
    long B;
    int int_temp;
    ADC_enable();
    while(state == state2){

        while (flag == 0){
            ADC_touch();
            Qformat_val = (long)(adcVal) ;
            Qformat_val = Qformat_val << 6; //2^6
            values[count_ADC] = Qformat_val;
            count_ADC++;
            SMA = SMA + Qformat_val;

            if (count_ADC == 32 ){
                flag = 1;
                count_ADC = 0;
                // the value here is avarge_ADC * 2^6
                SMA = (SMA >> 5); //divide by 32

            }
        }

        ADC_touch();
        Qformat_val = (long)(adcVal) ;
        Qformat_val = Qformat_val << 6; //2^6
        // this value can be nigative
        B = (Qformat_val - values[count_ADC]) >> 5; //divide by 32
        SMA = SMA +  B;
        values[count_ADC] = Qformat_val;
        count_ADC = (count_ADC +1)%32;


        //(3.25*10^4)/1023 = 32=2^5 = mult and divide by 2^6
        temp = SMA >> 1;
        //now it is avargeADC
        //temp = (SMA >> 6);

        temp = temp/10;
        // this will give me 4 digit number max
        int_temp = (int)(temp);
        FloatToString(ADC, int_temp);
        lcd_home();
        for(i = 0; i < 6; i++){
            if(prevADC[i] != ADC[i]){
                prevADC[i] = ADC[i];
                lcd_data(prevADC[i]);
            }
            else
                lcd_cursor_right();
        }
    }
}

void LIDR_test(){
    while(state == state2){
        ADC_enable();
        ADC_touch();
        lcd_home();
        printIntToLCD(adcVal[3]);//P1.0 LIDAR1
        lcd_new_line;
        printIntToLCD(adcVal[0]);//P1.3 LIDAR2
    }

}//LIDR_test

void LIDR_Clib(){

    int i = 0;
    while(i < 50 ){
        i = i + 1000;
        lcd_home();
        printIntToLCD(i);
        to_char(i);
        enterLPM(lpm_mode);
        ADC_enable();
        ADC_touch();

        //LIDARarr[0][i-1] = adcVal[3];//P1.0 LIDAR1
        //LIDARarr[1][i-1] = adcVal[0];//P1.3 LIDAR2
    }
    i = 0;
    //Send_Clib();
    //enterLPM(lpm_mode);
    state = state0;
    lcd_home();
    lcd_clear();

}

void printIntToLCD(unsigned int temp){

    unsigned int i;
    char s[5];
    s[4] = '\0';

    for(i=4; i>0 ;i--){
        s[i-1] = temp%10 + '0';
        temp = temp/10;
    }
    //lcd_clear();
    //lcd_home();
    lcd_puts(s);
}
