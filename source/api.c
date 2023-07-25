#include  "../header/api.h"    		// private library - API layer
#include  "../header/halGPIO.h"     // private library - HAL layer



int conv_str_to_int(char* array){
    int i_arr = 0;
    int value = 0;
    while(array[i_arr] != '\n'){
        value = value*10 + (array[i_arr] - '0');
        i_arr++;
    }

    return value;
}
void Telemeter(){

    unsigned int angle;
    int cycles_in;
    int angle_in;
    int angle_true;
    //white to send index
    enterLPM(lpm_mode);

    lcd_clear();
    lcd_home();
    angle_in = conv_str_to_int(angle_string);
    printIntToLCD(angle_in);

    Enable_SERVO(QFangle(angle_in) + 460);





    while(state == state4){
        Enable_TRIGGER();
        Enable_ECHO();
        enterLPM(lpm_mode);
        //Disable_ECHO();
        Disable_TRIGGER();

        if(REdge != 0 || FEdge != 0){

           cycles_in = FEdge - REdge;

           if (FEdge < REdge){
               cycles_in = REdge - FEdge;
               //dist = (FEdge - REdge) << 3;
           }
        }
        //cycles_in = get_sonic_range();
        to_char(cycles_in);
        transmite_UART(2);


        lcd_home();
        lcd_new_line;
        printIntToLCD(cycles_in);

    }
    Disable_SERVO();
    lcd_clear();
    lcd_home();

}



int get_sonic_range(){
    //range from 2cm to 450cm
    unsigned int range_US;
    int i;
    // for 25 C room temputre
    unsigned int speed_sound = 34645;

    Enable_TRIGGER();
    Enable_ECHO();
    enterLPM(lpm_mode);

    range_US =0;
    for(i = 0 ;i < 4; i++){
        range_US += FEdge - REdge;
    }
    range_US = range_US >> 2;
    Disable_ECHO();
    Disable_TRIGGER();

    return range_US;
}

// Qformat angle
unsigned int QFangle(unsigned int angle_in){
    unsigned int timer_out;
    long temp_angle;
    unsigned int mult_QF = 1200;//9.5*2^7
    temp_angle = ((long)mult_QF)*((long)angle_in);
    temp_angle = temp_angle >> 7;
    timer_out = (int)temp_angle;
    return timer_out;

}


void ObjectsDetectorSystem(unsigned int steps){
    unsigned int j = 0, max = 35;//450 original
    unsigned int dist, angle;
    unsigned char char_angle;
    unsigned int true_angle;
    int mult_step;

    lcd_clear();
    lcd_home();

    Enable_SERVO(450);
    enterLPM(lpm_mode);
    enterLPM(lpm_mode);
    mult_step = 180/steps;
    /*
    if (char_array[0] != 0){
        max = (char_array[2]+'0')*100 + (char_array[1]+'0')*10 + (char_array[0]+'0');
        char_array[0] = '\0';
        char_array[1] = '\0';
        char_array[2] = '\0';
        char_array[3] = '\0';
    }
    */
    while(state == state1){

        for (j = 0 ; j <= steps ; j++){
            REdge = 0;
            FEdge = 0;
            true_angle = j*mult_step;
            angle = QFangle(true_angle);

            Enable_SERVO(angle + 450);
            Enable_TRIGGER();
            Enable_ECHO();

            lcd_home();
            printIntToLCD(true_angle);//P1.0 LIDAR1
            enterLPM(lpm_mode);
            //Disable_ECHO();
            Disable_TRIGGER();

            if(REdge != 0 || FEdge != 0){

                dist = FEdge - REdge;

                if (FEdge < REdge){
                    dist = REdge - FEdge;
                    //dist = (FEdge - REdge) << 3;
                }
            }
            to_char(true_angle);
            transmite_UART(2);

            to_char(dist);
            transmite_UART(2);

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

void LDR_Scan(unsigned int steps){
    //int adc_V1 ,adc_V2 ;
    int ii;
    int j;
    int mult_step;
    int true_angle;
    int angle;
    Enable_SERVO(450); // 90 degres
    enterLPM(lpm_mode);
    Disable_SERVO();

    Enable_SERVO(450);
    enterLPM(lpm_mode);
    enterLPM(lpm_mode);
    mult_step = 180/steps;

    while(state == state2){
        adc_V1 = 0;
        adc_V2 = 0;

        for (j = 0 ; j <= steps ; j++){
            adc_V1 = 0;
            adc_V2 = 0;

            true_angle = j*mult_step;
            angle = QFangle(true_angle);

            Enable_SERVO(angle + 450);
            //Enable_SERVO(1315);
            //for(ii = 0; ii< 4; ii++){
            ADC_enable();
            ADC_touch();
            //adc_V1 +=adcVal[3];//P1.0 LIDAR1
            //adc_V2 +=adcVal[0];//P1.3 LIDAR2
            //}
            enterLPM(lpm_mode);
            adc_V1 = adc_V1 >> 2;
            adc_V2 = adc_V2  >> 2;

            lcd_home();
            printIntToLCD(count_LDR);//P1.0 LIDAR1
            lcd_new_line;
            printIntToLCD(adc_V2);//P1.3 LIDAR2

            to_char(true_angle);
            transmite_UART(2);

            to_char(adc_V1);
            transmite_UART(2);
            to_char(adc_V2);
            transmite_UART(2);

    }

    adc_V1 = 0;
    adc_V2 = 0;
    state = state0;
    }


}//LIDR_test

void LIDR_Clib(){

    int i = 0;
    int ii;

    Enable_SERVO(1315); // 90 degres
    enterLPM(lpm_mode);
    Disable_SERVO();


    //get 9 values
    for(i=0;i<10;i++ ){
        adc_V1 = 0;
        adc_V2 = 0;

        ADC_enable();
        ADC_touch();
        //wait for servo button
        enterLPM(lpm_mode);

        // get values from LDR
        /*for(ii = 0; ii< 4; ii++){
            ADC_enable();
            ADC_touch();
            adc_V1 +=adcVal[3];//P1.0 LIDAR1
            adc_V2 +=adcVal[0];//P1.3 LIDAR2
        }*/
        adc_V1 = adc_V1 >> 2;
        adc_V2 = adc_V2 >> 2;

        lcd_home();
        printIntToLCD(adc_V1);//P1.0 LIDAR1
        lcd_new_line;
        printIntToLCD(adc_V2);//P1.3 LIDAR2

        to_char(adc_V1);
        transmite_UART(2);
        to_char(adc_V2);
        transmite_UART(2);


    }

    adc_V1 = 0;
    adc_V2 = 0;

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

void test_fun(){
    int a = 0;
    int b = 1000;
    Enable_SERVO(450); // 90 degres
    enterLPM(lpm_mode);
    Disable_SERVO();

    Enable_SERVO(1315); // 90 degres
    enterLPM(lpm_mode);
    Disable_SERVO();
    Enable_SERVO(2140); // 90 degres
    enterLPM(lpm_mode);
    Disable_SERVO();






}



