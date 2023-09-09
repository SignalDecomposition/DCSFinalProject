import pygame
import time
import sys

from button import Button 
from utilities import Send_cahr,receive_bytes

#define coloures 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GRAY69 = (176,176,176)
BG_COLOER = (52, 78, 91)
BLUE = (0,238,238)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("arialblack", size)

    

def Calibration(window,s):
    BACK_BUTTON = Button(image=None, pos=(80, 30), 
                            text_input="back", font=get_font(60), base_color=BLACK, hovering_color="White")
    CONTINUE_BUTTON  = Button(image=None, pos=(640, 400), 
                            text_input="Continue", font=get_font(60), base_color=BLACK, hovering_color="White")
    # Create an empty 2x9 array
    empty_array = [[0 for _ in range(10)] for _ in range(2)]
    # clear garbge values
    time.sleep(0.25)
    while s.in_waiting > 0:
        lox = s.read_until(expected='\n')
    time.sleep(0.25)
    inChar = '3'
    # Send state
    bytesChar = bytes(inChar, 'ascii')
    s.write(bytesChar)
    # wait to finshe sending
    while s.out_waiting > 0:
        pass
    
    telemeter_start = True    
    i = 5
    j = 0
    while telemeter_start:
        
        if (i < 55 and j < 10):
            str_output = "Put light source in [cm] %d and press continue" % i
            text_surfce = get_font(40).render(str_output, False, BLACK)
       
        window.fill(BLUE)
        RADAR_MOUSE_POS= pygame.mouse.get_pos()
        

        for button in [BACK_BUTTON, CONTINUE_BUTTON]:
            button.changeColor(RADAR_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(RADAR_MOUSE_POS):
                    return
                    #telemeter_start = False
                if CONTINUE_BUTTON.checkForInput(RADAR_MOUSE_POS):
                    inChar = 'U'
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
                    if (i == 55):
                        # Save the 2D array to a text file
                        with open('array_data.txt', 'w') as f:
                            for row in empty_array:
                                f.write(' '.join(str(elem) for elem in row) + '\n')
                        text_surfce = get_font(40).render("End press back", False, BLACK)

       
        window.blit(text_surfce, (200-text_surfce.get_width()/8,200)) 
        # Update Display       
        pygame.display.update()

    
    return