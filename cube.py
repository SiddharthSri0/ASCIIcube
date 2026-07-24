import math 
import sys
import pygame

#these are macros defined for optimization 

WIDTH, HEIGHT = 160 , 44    #size of the ascii grid 
CUBE_WIDTH =20              #predetermined width of the cube
DISTANCE_FROM_CAM = 100     #
K1 = 40                     #projection scale vector
INCREMENT_SPEED = 0.6
BACKGROUND_CHAR=" "         #background for the cube display

ROT_SPEED_A = 0.10
ROT_SPEED_B = 0.10
ROT_SPEED_C = 0.03

FONT_SIZE = 10
FPS = 60


#intial rotation states 
A=0.0
B=0.0
C=0.0

#function to calculate the rotated x coordinates
def calculate_x(i , j , k):
    return (j*math.sin(A)*math.sin(B)*math.cos(C) 
    - k*math.cos(A)*math.sin(B)*math.cos(C) 
    + j*math.cos(A)*math.sin(C) 
    + k*math.sin(A)*math.sin(C) 
    + i*math.cos(B)*math.cos(C) )
#the above calculation is done by multiplying the current x coordinate with the roatational matrix and returning the new x coordinate


#we will repeat the same steps for the y and z coordinates as well
def calculate_y(i , j , k):
    return (j*math.cos(A)*math.cos(C) 
    + k*math.sin(A)*math.cos(C) 
    - j*math.sin(A)*math.sin(B)*math.sin(C) 
    + k*math.cos(A)*math.sin(B)*math.sin(C) 
    - i*math.cos(B)*math.sin(C) )

def calculate_z(i , j , k):
    return k*math.cos(A)*math.cos(B) - j*math.sin(A)*math.cos(B) + i*math.sin(B)
    

def render_fram(horizontal_offset=0.0):
        #z buffer implementation to keep track of the depth of each pixel

        buffer=[BACKGROUND_CHAR] * (WIDTH * HEIGHT) # this is the buffer that will hold the characters to be displayed on the screen
        z_buffer = [0] * (WIDTH * HEIGHT) #this decides which pixel is in front of the other based on the z coordinate of the pixel

        def calculate_for_surface(cube_x, cube_y, cube_z, ch):
            #sending each of these coordinates to the rotation functions to get the new coordinates after rotation
            x=calculate_x(cube_x, cube_y, cube_z)
            y=calculate_y(cube_x, cube_y, cube_z)
            z=calculate_z(cube_x, cube_y, cube_z) + DISTANCE_FROM_CAM

            ooz =1.0/z #z^-1 for the projection formula

            #this is the projection formula to convert 3D coordinates to 2D coordinates
            xp=int(WIDTH/2 +horizontal_offset + K1*ooz*x*2)
            yp=int(HEIGHT/2 + K1*ooz*y)

            idx = xp+yp*WIDTH

            #the purpose of the z buffer is to keep track of the depth of each pixel and only display the pixel that is closest to the camera.
            if 0<=idx<WIDTH*HEIGHT:
                if ooz>z_buffer[idx]:
                    z_buffer[idx]=ooz
                    buffer[idx]=ch

        cube_x= -CUBE_WIDTH
        while cube_x< CUBE_WIDTH:
            cube_y= -CUBE_WIDTH
            while cube_y< CUBE_WIDTH:
                calculate_for_surface(cube_x, cube_y, -CUBE_WIDTH, "@")
                calculate_for_surface(cube_x, cube_y, CUBE_WIDTH, "$")
                calculate_for_surface(-CUBE_WIDTH, cube_y, cube_x, "#")
                calculate_for_surface(CUBE_WIDTH, cube_y, cube_x, "~")
                calculate_for_surface(cube_x, -CUBE_WIDTH, cube_y, ";")
                calculate_for_surface(cube_x, CUBE_WIDTH, cube_y, "+")
                cube_y+=INCREMENT_SPEED
            cube_x+=INCREMENT_SPEED
        return buffer
def main():
    global A, B, C

    pygame.init()
    font=pygame.font.SysFont("consolas", FONT_SIZE)
    char_w, char_h = font.size("@")

    #display size is calculated based on the number of characters in the grid and the size of each character
    screen_w= char_w * WIDTH
    screen_h= char_h * HEIGHT
    screen=pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Rotating ASCII Cube")

    clock=pygame.time.Clock()

    #prerender each character to a surface to optimize the rendering process
    glyph_cache={}

    def get_glyph(ch):
        if ch not in glyph_cache:
            #this is the color of the cube, you can change it to any color you want
            glyph_cache[ch]=font.render(ch, False, (0,255,70))
        return glyph_cache[ch]

    running=True
    while running:
        for event in pygame.event.get():
            #this if else tree is used to check if the user has closed the window or pressed the escape key to exit the program
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                running=False

        buffer = render_fram()

        screen.fill((0,0,0))  #fill the screen with black color
        for row in range(HEIGHT):
            for col in range(WIDTH):
                ch = buffer[row * WIDTH + col]
                if ch == BACKGROUND_CHAR:
                    continue
                glyph = get_glyph(ch)
                screen.blit(glyph, (col * char_w, row * char_h))

        pygame.display.flip()

        A+= ROT_SPEED_A
        B+= ROT_SPEED_B
        C+= ROT_SPEED_C

        #limit the frame rate to the specified FPS to ensure smooth animation
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()
        



    