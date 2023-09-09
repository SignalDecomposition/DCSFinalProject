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
    

def Telemeter(window,s,state):
    BACK_BUTTON = Button(image=None, pos=(80, 30), 
                            text_input="back", font=get_font(60), base_color=BLACK, hovering_color="White")
    if state == 4:
        inChar = '4'        
        time.sleep(0.25) 
        while s.in_waiting > 0 :
            lox = s.read_until(expected='\n')
        time.sleep(0.25)     
        bytesChar = bytes(inChar, 'ascii')
        s.write(bytesChar)
        enableTX = True
        # TX
        while (s.out_waiting > 0 or enableTX):  # while the output buffer isn't empty
            if state == 6 :
                txMsg = "LCD"
                break
            txMsg = text_box("Enter angle 0-180: ",window)
            if(txMsg == ''): break
            bytetxMsg = bytes(txMsg + '\n', 'ascii')
            s.write(bytetxMsg)
            time.sleep(0.25)  # delay for accurate read/write operations on both ends
            if s.out_waiting == 0:
                enableTX = False 
    
    Telemeter_clock = pygame.time.Clock()  
    telemeter_start = True    
    while telemeter_start:
        
        while s.in_waiting == 0 :
                pass
        #while s.in_waiting != 0 :
            #bytes_in = s.read(2)
        bytes_in = s.read(2)
        #time.sleep(0.25)
        dist = round(int.from_bytes(bytes_in,"little")*0.132160, 2)
        if state == 4:
            text_surfce = get_font(60).render("Angle "+ txMsg +" Dist [cm]"+ str(dist), False, BLACK)
        else:
            text_surfce = get_font(60).render("Dist [cm]"+ str(dist), False, BLACK)
        window.fill(BLUE)
        RADAR_MOUSE_POS= pygame.mouse.get_pos()
        

        for button in [BACK_BUTTON]:
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
       
        window.blit(text_surfce, (200,200)) 
        # Update Display       
        pygame.display.update()
        Telemeter_clock.tick(30)
    #state = 0 
    #inChar = '0'
    #bytesChar = bytes(inChar, 'ascii')
    #while s.in_waiting == 0 :
    #        pass
    #s.write(bytesChar)
    return