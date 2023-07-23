import serial as ser
import time 

def Telemeter(s): 
    
    enableTX = True
    # TX
    while (s.out_waiting > 0 or enableTX):  # while the output buffer isn't empty
        txMsg = input("Enter angle 0-180: ")
        if(txMsg == ''): break
        bytetxMsg = bytes(txMsg + '\n', 'ascii')
        s.write(bytetxMsg)
        time.sleep(0.25)  # delay for accurate read/write operations on both ends
        if s.out_waiting == 0:
            enableTX = False             
    try:
        while True:
            
        
            while s.in_waiting == 0 :
                pass
            while s.in_waiting != 0 :
                bytes_in = s.read(2)
            time.sleep(0.25)
            range = int.from_bytes(bytes_in,"little")*0.132160
            # Print the received integer
            print("range is [cm]: %.2f" % range)
    except KeyboardInterrupt:
        s.reset_input_buffer()
        pass
    #state = 0 
    inChar = '0'
    bytesChar = bytes(inChar, 'ascii')
    while s.in_waiting == 0 :
            pass
    s.write(bytesChar)
    return

def Send_cahr(s,inChar):
    """send a 1 character to MCU (MSP430) 
    Parameters
    ----------
    s : serial
        seiral object from pyserial lib
    inChar :string inChar
        shoulde be the number of state we want to send 

    Returns
    -------
    None 
    """
    bytesChar = bytes(inChar, 'ascii')
    s.write(bytesChar)
    # delay for accurate read/write operations on both ends
    time.sleep(0.25)  

    return 

def receive_bytes(s, num_bytes):
    """recives the number of bytes you send it from MSP430 
    ----------
    s : serial
        seiral object from pyserial lib
    num_bytes :int
        number of bytes we expect 

    Returns
    -------
    bytes from MSP430
    """

    while s.out_waiting != 0 :
        pass
    bytes_in = s.read(num_bytes)
    #time.sleep(0.25)

    return bytes_in