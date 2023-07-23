import serial as ser
import time
import sys
from utilities import Telemeter, Send_cahr,receive_bytes

menu = """                                   Menu
            1. Objects Detector System
            2. Light Sources Detector System
            3. Light Detector calibration
            4. Telemeter
            5. Script Mode
            6. Light Sources and Objects Detector System
            9. Sleep
           """


def main():
    s = ser.Serial('COM4', baudrate=9600, bytesize=ser.EIGHTBITS,
                   parity=ser.PARITY_NONE, stopbits=ser.STOPBITS_ONE,
                   timeout=1)  # timeout of 1 sec where the read and write operations are blocking,
    # after the timeout the program continues
    # clear buffers
    s.reset_input_buffer()
    s.reset_output_buffer()

    print(menu)
    arr = [0,0,0]
    i=0
    while (1):
        while s.out_waiting == 0:
            inChar = input("Enter char: ")
            if inChar == '8':
                print(menu)
            elif inChar == '1' :
                time.sleep(0.25) 
                while s.in_waiting > 0 :
                    lox = s.read_until(expected='\n')
                time.sleep(0.25)     
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
                
                #while s.out_waiting != 0:
                    #pass                
                    #print("hello")
                #x = input("Enter max masking: ")
                #bytesChar = bytes(x + '\n', 'ascii')
                #s.write(bytesChar)
                #time.sleep(0.25)  # delay for accurate read/write operations on both ends
                try:
                   angle = 0
                   while(1):
                        angle_in = receive_bytes(s,2)
                        angle = int.from_bytes(angle_in,"little")
                        b = receive_bytes(s,2)
                        range = int.from_bytes(b ,"little")*0.13216
                        # Print the received integer
                        print("Angle is: ", angle)
                        print("Range is [cm]:: ", range)
                except KeyboardInterrupt:
                    s.reset_input_buffer()
                    pass
                print('Done!')


            elif inChar == '3' :
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)

                dist = 5
                while s.out_waiting != 0:
                    pass
                while s.in_waiting == 0:
                    pass
                while s.in_waiting != 0:
                    bytes_in = s.read(1)
                print(str(bytes_in))
                while dist <= 50:
                    print("press any key to contiue")
                    inChar = input()
                    bytesChar = bytes(inChar, 'ascii')
                    s.write(bytesChar)
                    while s.out_waiting != 0 :
                        pass
                    while s.in_waiting == 0 :
                        pass
                    while s.in_waiting != 0 :
                        bytes_in = s.read(2)
                    print(int.from_bytes(bytes_in,"little"))
                    print("Calibration at "+str(dist)+" cm")
                    if dist == 50 :
                        break
            elif inChar == '4':
                Send_cahr(s,inChar)
                Telemeter(s)
            elif inChar == '5' or inChar == '2':
                Send_cahr(s,inChar)
                try:
                   while(1):
                        bytes_in = receive_bytes(s,2)
                        a = int.from_bytes(bytes_in,"little")
                        b = receive_bytes(s,2)
                        b = int.from_bytes(b,"little")
                        # Print the received integer
                        print("a is: ", a)
                        print("b is: ", b)
                except KeyboardInterrupt:
                    pass
                inChar = '0'
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
                
            elif inChar == '6' or inChar == '9' or inChar == '4':
                Send_cahr(s,inChar)
           
            elif inChar == '7':
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
                time.sleep(0.25)  # delay for accurate read/write operations on both ends
                while (s.in_waiting > 0):  # while the input buffer isn't empty
                    line = s.read()
                    # readline() can also be used if the terminator is '\n'
                    print(line.decode("ascii"))
            else:
                print("WRONG INPUT, TRY AGAIN")


if __name__ == '__main__':
    main()
