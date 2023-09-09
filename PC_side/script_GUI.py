import pygame
import time
import sys
import serial as ser
import math
import numpy as np

from button import Button
from radar_GUI import radar
from telemeter_GUI import Telemeter
from calib_GUI import Calibration
from LDR_GUI import LDR_scan
from utilities import Send_cahr,receive_bytes
from utilities import ScriptToHEX




#define coloures 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GRAY69 = (176,176,176)
BG_COLOER = (52, 78, 91)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("arialblack", size)

def text_box(str,window):
    user_input = ""
    input_rect = pygame.Rect(200,200,800,80)
    Color_input= pygame.Color("lightskyblue3")
    count = 0 
    while (1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:    
                    return user_input 
                elif event.key == pygame.K_BACKSPACE and count > 0:
                    user_input = user_input[0:-1]
                    count -= 1  
                elif count < 3:   
                    count += 1  
                    user_input += event.unicode
               
        pygame.draw.rect(window,Color_input,input_rect)            
        text_surfce = get_font(60).render(str + user_input, False, BLACK)
        window.blit(text_surfce, input_rect)
        # Update Display
        #pygame.display.update()
        pygame.display.flip()


def script_mode(window,s):
   
    pygame.display.set_caption("Script Mode")
    BACK_BUTTON = Button(image=None, pos=(80, 30), 
                            text_input="back", font=get_font(60), base_color=BLACK, hovering_color="White")

    MENU_TEXT = get_font(80).render("Script Mode", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 80))
    FLASH_BUTTON = Button(image=None, pos=(640, 160), 
                            text_input="Flash", font=get_font(45), base_color=BLACK, hovering_color="White")
    SCRIPT_BUTTON = Button(image=None, pos=(640, 220), 
                            text_input="Script Select", font=get_font(45), base_color=BLACK, hovering_color="White")

    
    wait_text = get_font(45).render("In Process ", True, "#b68f40")
    text_rect = wait_text.get_rect(center=(200, 200))
    # Main loop
    start_script = True
    while start_script:
        window.fill(BG_COLOER)

        SCRIPT_MOUSE_POS = pygame.mouse.get_pos()
        window.blit(MENU_TEXT, MENU_RECT)

        for button in [BACK_BUTTON, FLASH_BUTTON,FLASH_BUTTON,SCRIPT_BUTTON]:
            button.changeColor(SCRIPT_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(SCRIPT_MOUSE_POS):
                    return
                elif FLASH_BUTTON.checkForInput(SCRIPT_MOUSE_POS):
                    inChar = '5'      
                    time.sleep(0.25) 
                    while s.in_waiting > 0 :
                        lox = s.read_until(expected='\n')
                    time.sleep(0.25)     
                    bytesChar = bytes(inChar, 'ascii')
                    s.write(bytesChar)
                   
                    while (s.out_waiting > 0):
                        pass
                    while (s.in_waiting == 0):
                        pass
                    print(s.read())
                    #inChar = input("Enter NO. of files ")

                    inChar = str(text_box("Enter NO. of files ",window))
                    bytetxMsg = bytes(inChar, 'ascii')
                    s.write(bytetxMsg)
                    num_files = int(inChar)
                    for i in range(num_files):
                        filename = "Script%d.txt"%i
                        print(filename)
                        script = ScriptToHEX(filename)
                        for command in script:
                            bytetxMsg = bytes(command[2:] + '\n', 'ascii')
                            s.write(bytetxMsg)
                            time.sleep(0.25)  # delay for accurate read/write operations on both ends
                            while (s.out_waiting > 0):
                                pass
                            while (s.in_waiting == 0):
                                pass
                            print(s.read())
                elif SCRIPT_BUTTON.checkForInput(SCRIPT_MOUSE_POS):
                    

                    #time.sleep(0.25) 
                    #while s.in_waiting > 0 :
                    #    lox = s.read_until(expected='\n')
                    #time.sleep(0.25)
                    inChar = '6'    
                    bytetxMsg = bytes(inChar, 'ascii')
                    s.write(bytetxMsg)
                    while (s.out_waiting > 0):
                        pass
                    
                    print(s.read())
                    #inChar = input("Select Script (0,1,2) ")
                    inChar = str(text_box("Select Script (0,1,2) ",window))
                    bytetxMsg = bytes(inChar, 'ascii')
                    s.write(bytetxMsg)
                    while (s.out_waiting > 0):
                        pass

                    flag_script = True
                    while flag_script:
                        #while (s.in_waiting == 0):
                        #    pass
                        bytes_in = s.read(2)
                        state = int.from_bytes(bytes_in, "little")
                        if state == 6 :
                            Telemeter(window,s,6)
                            #back to state = 0
                            inChar = '0'
                            bytesChar = bytes(inChar, 'ascii')
                            s.write(bytesChar)
                            
                        elif state == 7:
                            radar(window,s,6,450)
                        elif state == 8:               
                            flag_script = False
                        else:
                            window.fill(BG_COLOER)
                            window.blit(wait_text, text_rect)
                            # Update Display
                            pygame.display.update()
                    
        

        # Update Display
        pygame.display.update()
    return 