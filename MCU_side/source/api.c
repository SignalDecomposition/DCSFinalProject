#include  "../header/api.h"         // private library - API layer
#include  "../header/halGPIO.h"     // private library - HAL layer

struct FileSystem f;
unsigned char d = 0x32;

int conv_str_to_int(char* array){
    int i_arr = 0;
    int value = 0;
    while(array[i_arr] != '\n'){
        value = value*10 + (array[i_arr] - '0');
        i_arr++;
    }

    return value;
}
void Telemeter(int x){

    int cycles_in;
    int angle_in;

    Enable_SERVO(450);
    enterLPM(lpm_mode);
    enterLPM(lpm_mode);
    Disable_SERVO();

    //wait to send index
    if (state == state4){
    enterLPM(lpm_mode);
    angle_in = conv_str_to_int(angle_string);
    }
    else{
        angle_in = x;
    }

    lcd_clear();
    lcd_home();
    printIntToLCD(angle_in);

    Enable_SERVO(QFangle(angle_in) + 450);

    while(state == state4 || state == state6){
        Enable_TRIGGER();
        Enable_ECHO();
        enterLPM(lpm_mode);
        Disable_TRIGGER();

        if(REdge != 0 || FEdge != 0){

           cycles_in = FEdge - REdge;

           if (FEdge < REdge){
               cycles_in = REdge - FEdge;
           }
        }

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

    Enable_TRIGGER();
    Enable_ECHO();
    enterLPM(lpm_mode);

    range_US =0;
    for(i = 0 ;i < 4; i++){
        range_US += FEdge - REdge;
    }
    range_US = range_US >> 2;

    Disable_TRIGGER();

    return range_US;
}

// Qformat angle
unsigned int QFangle(unsigned int angle_in){
    unsigned int timer_out;
    long temp_angle;
    unsigned int mult_QF = 1208;//9.5*2^7//9.39*2^7
    temp_angle = ((long)mult_QF)*((long)angle_in);
    temp_angle = temp_angle >> 7;
    timer_out = (int)temp_angle;
    return timer_out;

}


void ObjectsDetectorSystem(int l, int r){
    unsigned int j = 0, max = 35;//450 original
    unsigned int dist, angle;
    unsigned int true_angle;
    unsigned int steps;

    lcd_clear();
    lcd_home();

    Enable_SERVO(450);
    enterLPM(lpm_mode);
    steps = (r-l)/3;

    if(state == state6){
        to_char(r);
        transmite_UART(2);
    }

    /*
    if (char_array[0] != 0){
        max = (char_array[2]+'0')*100 + (char_array[1]+'0')*10 + (char_array[0]+'0');
        char_array[0] = '\0';
        char_array[1] = '\0';
        char_array[2] = '\0';
        char_array[3] = '\0';
    }
    */
    while(state == state1 || state == state6){
        for (j = 0 ; j <= steps ; j++){
            REdge = 0;
            FEdge = 0;
            true_angle = l + 3*j;
            angle = QFangle(true_angle);

            Enable_SERVO(angle + 450);
            Enable_TRIGGER();
            Enable_ECHO();

            lcd_home();
            printIntToLCD(true_angle);//P1.0 LIDAR1
            enterLPM(lpm_mode);
            Disable_TRIGGER();


            if(REdge != 0 || FEdge != 0){

                dist = FEdge - REdge;

                if (FEdge < REdge){
                    dist = REdge - FEdge;
                }
            }else{

                dist = 450;
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
    long SMA = 0, temp;
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
    int j;
    int mult_step;
    int true_angle;
    int angle;

    Enable_SERVO(450); // 0 degres
    enterLPM(lpm_mode);
    enterLPM(lpm_mode);
    Disable_SERVO();

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
            ADC_enable();
            ADC_touch();

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
    Disable_SERVO();
    state = state0;
    }


}//LIDR_test

void LIDR_Clib(){
    int angle;
    int i = 0;
    angle = QFangle(90);
    Enable_SERVO(angle + 450); // 90 degres
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

void flash(){
    unsigned int i, j;
    int address = infomation_seg_A;
    erase_segment(infomation_seg_A);          // Erase flash Information A and B
    while (state == state5){
        enterLPM(lpm_mode);

        // WRITE FILES TO FLASH MEMORY
        for (i = 0; i < f.FilesCount; i++){
            f.FilesStart[i] = (int *)address;
            while (1){
                enterLPM(lpm_mode);
                for (j = 0; j < index; j++){
                    write_char_flash(address,string1[j]);
                    address++;
                }
                index = 0;
                if (string1[0] == 0x00 && string1[1] == 0x08){
                    break;
                }
            }
            f.FilesSizes[i] = address - (int)f.FilesStart[i];
        }
        state = state0;
    }
}

void Script_Mode(){
    char fileNo, OP;
    int i, x, k;
    d = 50;
    while (state == state6){
        enterLPM(lpm_mode);
        fileNo = char_array[0];
        i = (int)f.FilesStart[fileNo] ;
        while (i < (int)f.FilesStart[fileNo] + f.FilesSizes[fileNo]){
            OP = charsToINT(read_data(i),read_data(i+1));
            i = i+2;
            switch (OP){
                case 0x01:
                    x = charsToINT(read_data(i),read_data(i+1));
                    inc_lcd(x);
                    break;
                case 0x02:
                    x = charsToINT(read_data(i),read_data(i+1));
                    dec_lcd(x);
                    break;
                case 0x03:
                    x = charsToINT(read_data(i),read_data(i+1));
                    rra_lcd(x);
                    break;
                case 0x04:
                    d = charsToINT(read_data(i),read_data(i+1));
                    break;
                case 0x05:
                    lcd_clear();
                    i = i-2;
                    break;
                case 0x06:
                    to_char(OP);
                    transmite_UART(2);
                    x = charsToINT(read_data(i),read_data(i+1));
                    Telemeter(x);
                    state = state6;
                    break;
                case 0x07:
                    to_char(OP);
                    transmite_UART(2);
                    x = charsToINT(read_data(i),read_data(i+1));
                    i += 2;
                    k = charsToINT(read_data(i),read_data(i+1));
                    ObjectsDetectorSystem(x,k);
                    state = state6;
                    break;
                case 0x08:
                    to_char(OP);
                    transmite_UART(2);
                    state = state0;
                    break;
                default :
                    break;
            }
            i += 2;
            lcd_clear();
            lcd_home();
        }
    }
    //char_array[0] = '\0';
}

int charsToINT(char high, char low){

    int x;
    x = low + (high << 4);
    return (x);
}

void inc_lcd(int x){
    unsigned int i;
    Enable_DelayLCD();
    for (i = 0 ; i <= x ; i++){
        printIntToLCD(i);
        enterLPM(lpm_mode);
        lcd_clear();
        lcd_home();
    }
    Disable_DelayLCD();
}

void dec_lcd(int x){
    int i;
    Enable_DelayLCD();
    for (i = x ; i >= 0 ; i--){
        printIntToLCD(i);
        enterLPM(lpm_mode);
        lcd_clear();
        lcd_home();
    }
    Disable_DelayLCD();
}

void rra_lcd(char x){
    unsigned int i,j;
    Enable_DelayLCD();
    for (j = 0; j < 2; j++){
        lcd_data(x + '0');
        for (i = 1 ; i < 16 ; i++){
            enterLPM(lpm_mode);
            lcd_cursor_left();
            lcd_data('\n');
            lcd_data(x + '0');
        }
        lcd_cursor_left();
        lcd_data('\n');
        lcd_new_line;
    }
    Disable_DelayLCD();


}

void Bonus(int l, int r){
    unsigned int j = 0, max = 35;//450 original
    unsigned int dist, angle;
    unsigned int true_angle;
    int steps;

    lcd_clear();
    lcd_home();

    Enable_SERVO(450);
    enterLPM(lpm_mode);
    steps = (r-l)/3;


    while(state == state7){


        for (j = 0 ; j <= steps ; j++){
            adc_V1 = 0;
            adc_V2 = 0;
            REdge = 0;
            FEdge = 0;

            true_angle = l + 3*j;
            angle = QFangle(true_angle);



            Enable_SERVO(angle + 450);
            Enable_TRIGGER();
            Enable_ECHO();
            ADC_enable();
            ADC_touch();

            enterLPM(lpm_mode);
            Disable_TRIGGER();

            adc_V1 = adc_V1 >> 2;
            adc_V2 = adc_V2 >> 2;
            if(REdge != 0 || FEdge != 0){

                dist = FEdge - REdge;

                if (FEdge < REdge){
                    dist = REdge - FEdge;
                }
            }

            to_char(true_angle);
            transmite_UART(2); //send angle

            to_char(adc_V1);//P1.0 LIDAR1
            transmite_UART(2);
            to_char(adc_V2);//P1.3 LIDAR2
            transmite_UART(2);

            to_char(dist);
            transmite_UART(2); //send dist

            lcd_home();
            printIntToLCD(true_angle);//P1.0 LIDAR1
            lcd_new_line;
            printIntToLCD(dist);
        }
        Disable_SERVO();
        state = state0;
    }


}
void test_func(){
    int i;

    for(i = 400; i< 480; i += 30){
        lcd_home();
        printIntToLCD(i);
        Enable_SERVO(i);
        enterLPM(lpm_mode);
        Disable_SERVO();
    }


}

