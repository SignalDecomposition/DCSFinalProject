import serial as ser
import time

def ScriptToHEX():
    with open("Script0.txt", 'r') as script:
        commands = script.readlines()

    """
        convert each command to be a list
    """
    for i in range(len(commands)):
        commands[i] = commands[i].split()
        for j in commands[i]:
            if ',' in j:
                temp = j.split(',')
                commands[i].remove(j)
                for k in temp:
                    commands[i].append(k)

    """ 
        Convert each command to HEX
    """
    HEXlist = []
    OPcode = {"inc_lcd": 1, "dec_lcd": 2, "rra_lcd": 3, "set_delay": 4, "clear_lcd": 5,
              "servo_deg": 6, "servo_scan": 7, "sleep": 8}

    for command in commands:
        temp = '\\x' +  format(OPcode[command[0]], '02x')
        for param in command[1:]:
            temp = ''.join([temp, format(int(param), '02x')])

        HEXlist.append(temp)

    return HEXlist


def main():
    """ Establish communication """
    while (1):
        try :
            s = ser.Serial('COM1', baudrate=9600, bytesize=ser.EIGHTBITS,
                           parity=ser.PARITY_NONE, stopbits=ser.STOPBITS_ONE,
                           timeout=1)
                            # timeout of 1 sec so that the read and write operations are blocking,
                            # when the timeout expires the program will continue
            # clear buffers
            s.reset_input_buffer()
            s.reset_output_buffer()

        except ser.SerialTimeoutException:
            print("TRYING AGAIN")
        finally:
            print(s.read())
            break

    while(1):
        x = input("NO FEAR")
        x = ScriptToHEX()
        for i in x:
            print(i)
            bytetxMsg = bytes(i[2:]+'\n','ascii')
            s.write(bytetxMsg)
            time.sleep(0.25)  # delay for accurate read/write operations on both ends
            while (s.out_waiting > 0 ):
                pass
            while (s.in_waiting == 0 ):
                pass
            print(s.read())



if __name__ == '__main__':
    main()
