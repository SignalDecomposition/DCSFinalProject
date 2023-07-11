import serial as ser
import time

menu = """                                   Menu
            1. Blink RGB LED, color by color with delay of X[ms]
            2. Count up onto LCD screen with delay of X[ms]
            3. Circular tone series via Buzzer with delay of X[ms]
            4. Get delay time X[ms]:
            5. LDR 3-digit value [v] onto LCD
            6. Clear LCD screen
            7. I love my Negev
            8. Show menu
            9. Sleep
           """


def main():
    s = ser.Serial('COM6', baudrate=9600, bytesize=ser.EIGHTBITS,
                   parity=ser.PARITY_NONE, stopbits=ser.STOPBITS_ONE,
                   timeout=1)  # timeout of 1 sec where the read and write operations are blocking,
    # after the timeout the program continues
    print(menu)
    arr = [0,0,0]
    i=0
    # clear buffers
    s.reset_input_buffer()
    s.reset_output_buffer()
    while (1):
        while s.out_waiting == 0:
            inChar = input("Enter char: ")
            if inChar == '8':
                print(menu)
            elif inChar == '1' :
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
                x = input("Enter max masking: ")
                bytesChar = bytes(x + '\n', 'ascii')
                s.write(bytesChar)
                time.sleep(0.25)  # delay for accurate read/write operations on both ends
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
            elif inChar == '2' or  inChar == '5' or inChar == '6' or inChar == '9':
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
            elif inChar == '4':
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
                while s.out_waiting != 0:
                    pass
                x = input("Enter new X: ")
                bytesChar = bytes(x + '\n', 'ascii')
                s.write(bytesChar)
                time.sleep(0.25)  # delay for accurate read/write operations on both ends

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
