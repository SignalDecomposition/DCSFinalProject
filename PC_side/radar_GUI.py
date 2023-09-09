import pygame
import math
import sys
import serial as ser
import time

from utilities import receive_bytes
from button import Button 
from position_estimation import estimate_pos


#from PC_side_GUI import get_font

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 600

#define coloures 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GRAY69 = (176,176,176)
BG_COLOER = (52, 78, 91)
BLUE = (0,0,255)
GREEN = (0,255,0)
PURPLE = (128,0,128)

def radar_BG(window):
    # Calculate the x,y for the end point of our 'sweep' based on
    # the current angle
    window.fill(GRAY69)
    angle = 90
    x = 450 * math.cos(angle)  - WINDOW_WIDTH/2
    y = 450 * math.sin(angle) - 550   
    radar_circle_center_x = WINDOW_WIDTH/2
    radar_circle_center_y = 550
    radar_sweep_length = 500
    text_font = pygame.font.SysFont("arialblack", 20)
    for i in range(9):
        x = radar_circle_center_x + radar_sweep_length *math.sin(math.radians(angle))
        y = radar_circle_center_y + radar_sweep_length *math.cos(math.radians(angle))
        if(i < 5):
            x_txt = radar_circle_center_x + (radar_sweep_length + 20)*math.sin(math.radians(angle))
            y_txt = radar_circle_center_y + (radar_sweep_length + 30)*math.cos(math.radians(angle))
        elif i >= 5 and i <= 8:
            x_txt = radar_circle_center_x + (radar_sweep_length + 70)*math.sin(math.radians(angle))
            y_txt = radar_circle_center_y + (radar_sweep_length + 40)*math.cos(math.radians(angle))
        else:
            x_txt = radar_circle_center_x + (radar_sweep_length + 80)*math.sin(math.radians(angle))
            y_txt = radar_circle_center_y + (radar_sweep_length + 20)*math.cos(math.radians(angle))
        pygame.draw.line(window, BLACK, (radar_circle_center_x,radar_circle_center_y), (x, y), 3)
        text_radar = text_font.render(str(i*22.5), False, BLACK)
        window.blit(text_radar, (x_txt,y_txt))
        angle = angle + 22.5
    
    pygame.draw.circle(window,BLACK,[radar_circle_center_x,radar_circle_center_y],radar_sweep_length,3,True,True)
    pygame.draw.circle(window,BLACK,[radar_circle_center_x,radar_circle_center_y],375,3,True,True)
    pygame.draw.circle(window,BLACK,[radar_circle_center_x,radar_circle_center_y],radar_sweep_length/2,3,True,True)
    pygame.draw.circle(window,BLACK,[radar_circle_center_x,radar_circle_center_y],radar_sweep_length/4,3,True,True)

radar_circle_center_x = WINDOW_WIDTH/2
radar_circle_center_y = 550
radar_sweep_length = 500
# Function to convert angle and distance to Cartesian coordinates (x, y)




def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("arialblack", size)

def circle(window):
    pygame.draw.circle(window,(1,84,10),[400,400],400)
def move_line(window):
    pygame.draw.line(window,WHITE,[400,400],[116,116])

def draw_radar_sweep(window): 
    
    global radar_sweep_angle
    x = radar_circle_center_x + radar_sweep_length *math.sin(math.radians(90 + radar_sweep_angle))
    y = radar_circle_center_y + radar_sweep_length *math.cos(math.radians(90 + radar_sweep_angle))
    pygame.draw.line(window, RED, (radar_circle_center_x,radar_circle_center_y), (x, y), 3)
    

def creat_point(dist,angle):
    x = radar_circle_center_x + (dist*3) *math.sin(math.radians(90 + angle))
    y = radar_circle_center_y + (dist*3) *math.cos(math.radians(90 + angle))
    return x,y


  

def update():
   # Increment the angle in each frame
   global radar_sweep_angle
   radar_sweep_angle += 1
def draw_pointes(window,scaned_points,dist_points):
     dist_font = get_font(10)
     for i in range(len(scaned_points)-1):
        pygame.draw.circle(window,BLUE,scaned_points[i],3,2)
        if i%2:
            dist_text = dist_font.render(str(dist_points[i]), False, BLACK)
        else:
            dist_text = dist_font.render(str(dist_points[i]), False, WHITE)
        window.blit(dist_text, scaned_points[i])
        
def print_estmation(window,est_pointes):
    dist_font = get_font(20)
    for point in est_pointes:
        print(point)
        (x,y) = creat_point(point[1],point[0])
        print(x,y)
        pygame.draw.circle(window,GREEN,(x,y),4)
        dist_text = dist_font.render("(%d,%d)"%point, False, PURPLE)
        window.blit(dist_text, (x,y))
   

def radar(window,s,state,max_dist):
    radar_clock = pygame.time.Clock()
    pygame.display.set_caption("Radar Scan")
    max_angle = 180
    if state == 1:
        inChar = '1'        
        time.sleep(0.25) 
        while s.in_waiting > 0 :
            lox = s.read_until(expected='\n')
        time.sleep(0.25)     
        bytesChar = bytes(inChar, 'ascii')
        s.write(bytesChar)
    else: #state is 6 
        max_angle = int.from_bytes(s.read(2), "little")
    
    
    start_radar = True
    global radar_sweep_angle 
    radar_sweep_angle =0
    
    scaned_points = []
    dist_points = []
    data = []
    first = True
    while start_radar:
        BACK_BUTTON = Button(image=None, pos=(80, 30), 
                            text_input="back", font=get_font(60), base_color=BLACK, hovering_color="White")
        #radar_BG(window)
        bg = pygame.image.load("assets/radar_screenshot.png")

        #INSIDE OF THE GAME LOOP
        window.blit(bg, (0, 0))
        RADAR_MOUSE_POS= pygame.mouse.get_pos()
        # Update Display
        
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
                scaned_points.append(RADAR_MOUSE_POS)
                update()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:    
                    update()
        if(radar_sweep_angle < 180):        
            angle_in = receive_bytes(s,2)
            angle = int.from_bytes(angle_in,"little")
            b = receive_bytes(s,2)
            dist = round(int.from_bytes(b ,"little")*0.13216,2)
        if(radar_sweep_angle < 180 and angle >=0 and dist < max_dist):
            (x,y) = creat_point(dist,angle)
            scaned_points.append((x,y))
            dist_points.append(dist)
            data.append((angle,dist))
        radar_sweep_angle = angle
        draw_radar_sweep(window)
        draw_pointes(window,scaned_points,dist_points)
       
        

        if angle == 180 and first:
            first = False
            est_pointes = estimate_pos(data)
        
        if angle == 180:
            print_estmation(window,est_pointes)
        pygame.display.update()
        #if first:
        #    pygame.image.save(window, "radar_screenshot.png")
        
        #radar_clock.tick(30)
        if angle == max_angle -(max_angle-angle)%3 and state == 6:
             return