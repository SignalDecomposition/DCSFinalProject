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
from script_GUI import script_mode
from bonus_GUI import bonus_scan



# Initialize
pygame.init()


#Window size 
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 600

# Create Window/Display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("DCS Final")

#define fonts 
font = pygame.font.SysFont("arialblack", 40)# font size = 40

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("arialblack", size)
#Define button
radar_img = pygame.image.load("assets/Play Rect.png").convert_alpha()
light_detetector_button =  pygame.image.load("assets/Play Rect.png").convert_alpha()


#define coloures 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GRAY69 = (176,176,176)
BG_COLOER = (52, 78, 91)


# Initialize Clock for FPS
#fps = 30
#clock = pygame.time.Clock()

def text_box(str):
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
    

    return user_input 

def main():
    while (1):
        try :
            s = ser.Serial('COM4', baudrate=9600, bytesize=ser.EIGHTBITS,
                        parity=ser.PARITY_NONE, stopbits=ser.STOPBITS_ONE,
                        timeout=1, write_timeout=1)  # timeout of 1 sec where the read and write operations are blocking,
            
            # after the timeout the program continues
            # clear buffers
            s.reset_input_buffer()
            s.reset_output_buffer()
        except s.SerialTimeoutException:
            print("BLA")
        finally:
            break
    pygame.display.set_caption("Menu")
    MENU_TEXT = get_font(80).render("DCS Final Project", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 80))
        
    RADAR_BUTTON = Button(image=None, pos=(640, 160), 
                            text_input="Radar Scan", font=get_font(45), base_color=BLACK, hovering_color="White")
    LDR_BUTTON = Button(image=None, pos=(640, 220), 
                            text_input="LDR Scan", font=get_font(45), base_color=BLACK, hovering_color="White")
    CALIB_BUTTON = Button(image=None, pos=(640,290), 
                            text_input="LDR Calibration", font=get_font(45), base_color=BLACK, hovering_color="White")
    TELEMETER_BUTTON = Button(image=None, pos=(640,360), 
                            text_input="Telemeter", font=get_font(45), base_color=BLACK, hovering_color="White")
    SCRIPT_BUTTON = Button(image=None, pos=(640, 430), 
                            text_input="Script Mode", font=get_font(45), base_color=BLACK, hovering_color="White")
    BONUS_BUTTON = Button(image=None, pos=(640, 500), 
                            text_input="BONUS", font=get_font(45), base_color=BLACK, hovering_color="White")
    QUIT_BUTTON = Button(image=None, pos=(640, 560), 
                            text_input="Quit", font=get_font(45), base_color=BLACK, hovering_color="White")
    # Main loop
    start = True
    while start:
        window.fill(BG_COLOER)
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [RADAR_BUTTON, LDR_BUTTON,CALIB_BUTTON,TELEMETER_BUTTON,SCRIPT_BUTTON,BONUS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RADAR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    max_dist = int(text_box("Max dist [cm]: ")) 
                    radar(window,s,1,max_dist)
                    pygame.display.set_caption("Menu")
                    #back to state = 0 
                    inChar = '0'  
                    bytesChar = bytes(inChar, 'ascii')
                    s.write(bytesChar)
                    
                if LDR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    LDR_scan(window,s,2)
                    print("LDR")
                if TELEMETER_BUTTON.checkForInput(MENU_MOUSE_POS):   
                    Telemeter(window,s,4)
                    #back to state = 0
                    inChar = '0'
                    bytesChar = bytes(inChar, 'ascii')
                    s.write(bytesChar)                   
                if CALIB_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Calibration(window,s)
                    #back to state = 0
                    inChar = '0'
                    bytesChar = bytes(inChar, 'ascii')
                    s.write(bytesChar)
                if SCRIPT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    script_mode(window,s)
                    print("Scirpt Mode")
                if BONUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    max_dist = int(text_box("Max dist [cm]: "))
                    bonus_scan(window,s,7,max_dist) 

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        
       
        # Update Display
        pygame.display.update()
       
    pygame.quit()


if __name__ == '__main__':
    main()