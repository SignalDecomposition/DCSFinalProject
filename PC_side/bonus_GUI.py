import pygame
import math
import sys
import serial as ser
import time
import numpy as np

from utilities import receive_bytes,max_difference_between_columns
from button import Button 
from position_estimation import estimate_pos

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 600

#define coloures 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GRAY69 = (176,176,176)
BG_COLOER = (52, 78, 91)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
PURPLE = (128,0,128)

radar_circle_center_x = WINDOW_WIDTH/2
radar_circle_center_y = 550
radar_sweep_length = 500


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
def draw_pointes(window,scaned_points_LDR,dist_points_LDR,scaned_points_US,dist_points_US):
    dist_font = get_font(10)
    for i in range(len(scaned_points_LDR)-1):

        pygame.draw.circle(window,YELLOW,scaned_points_LDR[i],3,2)
        #dist_text = dist_font.render(str(dist_points_LDR[i]), False, BLACK)
        
        if i%2:
            dist_text = dist_font.render(str(dist_points_LDR[i]), False, BLACK)
        else:
            dist_text = dist_font.render(str(dist_points_LDR[i]), False, WHITE)
        window.blit(dist_text, scaned_points_LDR[i])

    for j in range(len(scaned_points_US)-1):
        pygame.draw.circle(window,BLUE,scaned_points_US[j],3,2)
        #dist_text = dist_font.render(str(dist_points_US[j]), False, BLACK)
        if j%2:
            dist_text = dist_font.render(str(dist_points_US[j]), False, BLACK)
        else:
            dist_text = dist_font.render(str(dist_points_US[j]), False, WHITE)
        window.blit(dist_text, scaned_points_US[j])
def print_estmation(window,est_pointes):
    dist_font = get_font(20)
    for point in est_pointes:
        print(point)
        (x,y) = creat_point(point[1],point[0])
        print(x,y)
        pygame.draw.circle(window,GREEN,(x,y),4,2)
        dist_text = dist_font.render("(%d,%d)"%point, False, PURPLE)
        window.blit(dist_text, (x,y))

def bonus_scan(window,s,state,max_dist):
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
    
    
    radar_clock = pygame.time.Clock()
    pygame.display.set_caption("LDR Scan")
    max_angle = 180
    if state == 7:
        inChar = '7'        
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
    
    scaned_points_LDR = []
    dist_points_LDR = []
    scaned_points_US = []
    dist_points_US = []
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
               
                
            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_RETURN:    
            #        update()
        if(radar_sweep_angle < 180): 

            angle_in = receive_bytes(s,2)
            angle = int.from_bytes(angle_in,"little")

            a_in = receive_bytes(s, 2)
            a = int.from_bytes(a_in, "little")
            b_in = receive_bytes(s, 2)
            b = int.from_bytes(b_in, "little")

            dist_in =  receive_bytes(s,2)
            dist = round(int.from_bytes(dist_in ,"little")*0.13216,2)


            # Print the received integer
            print("Angle is: ", angle)
            # Print the received integer
            print("a is: ", a)
            print("b is: ", b)
            print("dist: ",dist)
        if(radar_sweep_angle < 180 and angle >=0 ):
            if (abs(a - b) <= max_difference and a < loaded_array[0][9] and b < loaded_array[1][9]):
                idx_a = (np.abs(new_matrix[0] - a)).argmin()
                idx_b = (np.abs(new_matrix[1] - b)).argmin()
                if (abs(idx_a - idx_b) <= 1):
                    # Calculate the mean between the two values and convert to integer
                    mean_value = int(np.mean([idx_a, idx_a]))
                    print(mean_value)
                    (x,y) = creat_point(mean_value,angle)
                    scaned_points_LDR.append((x,y))
                    dist_points_LDR.append(mean_value)
                elif(dist < max_dist):
                    print("difference to big LDR")
                    data.append((angle,dist))
                    (x,y) = creat_point(dist,angle)
                    scaned_points_US.append((x,y))
                    dist_points_US.append(dist)
            elif(dist < max_dist):
                print("no dist LDR")
                data.append((angle,dist))
                (x,y) = creat_point(dist,angle)
                scaned_points_US.append((x,y))
                dist_points_US.append(dist)
            
            
        radar_sweep_angle = angle
        draw_radar_sweep(window)
        draw_pointes(window,scaned_points_LDR,dist_points_LDR,scaned_points_US,dist_points_US)

        if angle == 180 and first:
            first = False
            est_pointes = estimate_pos(data)
        
        if angle == 180:
            print_estmation(window,est_pointes)
        pygame.display.update()

        #if first:
        #    pygame.image.save(window, "radar_screenshot.png")
        
       