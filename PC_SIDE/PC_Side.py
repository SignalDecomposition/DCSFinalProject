import serial as ser
import time
import numpy as np
from utilities import Telemeter, Send_cahr, receive_bytes, ScriptToHEX
from utilities import max_difference_between_columns, ObjectsDetectorSystem

menu = """                                   Menu
            1. Objects Detector System
            2. Light Sources Detector System
            3. Light Detector calibration
            4. Telemeter
            5. Script Mode
            6. Light Sources and Objects Detector System
            9. Sleep
           """


# Function to estimate distances based on LDR readings using linear regression model
def estimate_distance(ldr_readings, coefficients):
    slope, intercept = coefficients
    return (ldr_readings - intercept) / slope


def main():
    loaded_array = []
    try:
        # Load the 2D array from the file
        with open('array_data.txt', 'r') as f:
            for line in f:
                row = [int(elem) for elem in line.strip().split()]
                loaded_array.append(row)
        print("Array Loaded!")
    except:
        print("No defulte values for light detector array")


    s = ser.Serial('COM13', baudrate=9600, bytesize=ser.EIGHTBITS,
                   parity=ser.PARITY_NONE, stopbits=ser.STOPBITS_ONE,
                   timeout=1)  # timeout of 1 sec where the read and write operations are blocking,
    # after the timeout the program continues
    # clear buffers
    s.reset_input_buffer()
    s.reset_output_buffer()



    print(menu)
    arr = [0, 0, 0]
    i = 0
    while (1):
        while s.out_waiting == 0:
            inChar = input("Enter char: ")
            if inChar == '8':
                print(menu)
            elif inChar == '1':
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
                ObjectsDetectorSystem(s,1)


            elif inChar == '3':
                # Create an empty 2x9 array
                empty_array = [[0 for _ in range(10)] for _ in range(2)]
                # clear garbge values
                time.sleep(0.25)
                while s.in_waiting > 0:
                    lox = s.read_until(expected='\n')
                time.sleep(0.25)

                # Send state
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
                # wait to finshe sending
                while s.out_waiting > 0:
                    pass

                i = 5
                j = 0
                while (i < 55 and j < 10):
                    inChar = input("Put light source in [cm] %d Enter char to continue: " % i)
                    bytesChar = bytes(inChar, 'ascii')
                    s.write(bytesChar)
                    # wait to finshe sending
                    while s.out_waiting > 0:
                        pass

                    # wait for response
                    while (s.in_waiting == 0):
                        pass
                    LDR1_bytes = receive_bytes(s, 2)
                    LDR1 = int.from_bytes(LDR1_bytes, "little")  # LDR1
                    LDR2_bytes = receive_bytes(s, 2)
                    LDR2 = int.from_bytes(LDR2_bytes, "little")  # LDR 2
                    # Print the received integer
                    print("LDR1 is: ", LDR1)
                    print("LDR2 is: ", LDR2)
                    empty_array[0][j] = LDR1
                    empty_array[1][j] = LDR2
                    i = i + 5
                    j = j + 1

                    # Save the 2D array to a text file
                with open('array_data.txt', 'w') as f:
                    for row in empty_array:
                        f.write(' '.join(str(elem) for elem in row) + '\n')

                # BACK TO ZERO state
                inChar = '0'
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
            elif inChar == '4':
                Send_cahr(s, inChar)
                Telemeter(s,4)
            elif inChar == '2':
                loaded_array = []
                try:
                    # Load the 2D array from the file
                    with open('array_data.txt', 'r') as f:
                        for line in f:
                            row = [int(elem) for elem in line.strip().split()]
                            loaded_array.append(row)
                        print("Array Loaded!")
                except:
                    print("No defulte values for light detector array")

                # Find the maximum difference between columns
                max_difference = max_difference_between_columns(loaded_array)

                # Sample 2x10 matrix representing LDR readings for distances 5 cm to 50 cm in jumps of 5 cm
                original_matrix = np.array(loaded_array)

                # Create a new array representing distances from 0 cm to 50 cm with 1 cm increment
                new_distances = np.arange(0, 51, 1)

                # Create a new 2x51 matrix using linear interpolation
                new_matrix = np.zeros((2, 51))
                for i in range(2):
                    new_matrix[i] = np.interp(new_distances, np.arange(5, 51, 5), original_matrix[i])
                # fix last culms of matrix
                for i in range(2):
                    new_matrix[i][0:4] = original_matrix[i][0] - (
                                original_matrix[i][1] - original_matrix[i][0]) / 5 * np.arange(4, 0, -1)

                print("Old mat: ")
                print(loaded_array)
                print("New Matrix:")
                print(new_matrix)

                print("max difference = ", max_difference)

                # send state2
                time.sleep(0.25)
                while s.in_waiting > 0:
                    lox = s.read()
                Send_cahr(s, inChar)

                try:
                    angle = 0
                    while (1):
                        angle_in = receive_bytes(s, 2)
                        angle = int.from_bytes(angle_in, "little")

                        bytes_in = receive_bytes(s, 2)
                        a = int.from_bytes(bytes_in, "little")
                        b = receive_bytes(s, 2)
                        b = int.from_bytes(b, "little")
                        # Print the received integer
                        print("Angle is: ", angle)
                        # Print the received integer
                        print("a is: ", a)
                        print("b is: ", b)
                        if (abs(a - b) <= max_difference and a < loaded_array[0][9] and b < loaded_array[1][9]):
                            idx_a = (np.abs(new_matrix[0] - a)).argmin()
                            idx_b = (np.abs(new_matrix[1] - b)).argmin()
                            if (abs(idx_a - idx_b) <= 1):
                                # Calculate the mean between the two values and convert to integer
                                mean_value = int(np.mean([idx_a, idx_a]))
                                print(mean_value)
                            else:
                                print("difference to big")
                        else:
                            print("no dist")
                        if angle >= 180 :
                            break
                except KeyboardInterrupt:
                    s.reset_input_buffer()
                    pass
                print('Done!')

                # BACK TO ZERO state
                inChar = '0'
                bytesChar = bytes(inChar, 'ascii')
                s.write(bytesChar)
            elif inChar == '5':
                bytetxMsg = bytes(inChar, 'ascii')
                s.write(bytetxMsg)
                while (s.out_waiting > 0):
                    pass
                while (s.in_waiting == 0):
                    pass
                print(s.read())
                inChar = input("Enter NO. of files ")
                bytetxMsg = bytes(inChar, 'ascii')
                s.write(bytetxMsg)
                script = ScriptToHEX()
                for command in script:
                    bytetxMsg = bytes(command[2:] + '\n', 'ascii')
                    s.write(bytetxMsg)
                    time.sleep(0.25)  # delay for accurate read/write operations on both ends
                    while (s.out_waiting > 0):
                        pass
                    while (s.in_waiting == 0):
                        pass
                    print(s.read())

            elif inChar == '6' or inChar == '9' or inChar == '4':
                bytetxMsg = bytes(inChar, 'ascii')
                s.write(bytetxMsg)
                while (s.out_waiting > 0):
                    pass
                while (s.in_waiting == 0):
                    pass
                print(s.read())
                inChar = input("Select Script (0,1,2) ")
                bytetxMsg = bytes(inChar, 'ascii')
                s.write(bytetxMsg)

                while True:
                    while (s.in_waiting == 0):
                        pass
                    bytes_in = s.read(2)
                    state = int.from_bytes(bytes_in, "little")
                    if state == 6 :
                        Telemeter(s,6)
                    elif state == 7:
                        ObjectsDetectorSystem(s,6)
                    elif state == 0:
                        break


                bytetxMsg = s.read()

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