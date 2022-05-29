import pygame, sys, geometry
import numpy as np
from pygame.locals import *

pygame.init()

screen_size = (1500, 768)
center_pos = np.array(screen_size) / 2
display_surf = pygame.display.set_mode(screen_size)

title = 'tesseract'
pygame.display.set_caption(title)

#colors
c_background = (255, 255, 255)
c_colors = [(255,255,255), (255,255,000), (255,000,255), (000,255,000), (000,000,255), (204,204,204), (255,204,255), (255,204,000), (51, 000, 255), (153,102,255), (255,204,204), (000,255,255), (255,000,000), (153,204,255), (255,000,153), (51,102,255), (153,51,204), (255,153,000), (51,255,204), (000,102,51), (102, 204, 000) , (255, 51,102), (000,102,204), (153,153,204), (51,153,51), (102,000,102), (102,51,204),(51,204,204), (000,51,255), (102,255,000), (000,51,51), (102,153,102)]
c_skyblue = (135, 206, 235)
c_black = (0, 0, 0)
c_red = (255, 0, 0)

c_random = np.array([0, 0, 0])

c_real = np.array([0.0, 0.0, 0.0])

fps_clock = pygame.time.Clock()
fps = 60

Tesseract = geometry.tesseract(0, 0, 1000, 0, 500)
theta = [0, 0, 0, 0, 0, 0] #xy, xz, xw, yz, yw, zw
theta_name = ['xy', 'xz', 'xw', 'yz', 'yw', 'zw']
theta_key = [K_0, K_1, K_2, K_3, K_4, K_5]
theta_index = 0

timer = 0
t = 1
change = False
minus = -1
auto = True


mouse_down = False

while True:
    if auto:
        if timer <= 0:
            timer = (np.random.randint(5) + 1) * fps
            t = timer
            change = True
        else:
            timer -= 1
            if change:
                theta_index = np.random.randint(6)
                print(theta_name[theta_index])
                c_random = np.random.randint(256, size = 3)
                change = False
                minus = np.random.randint(2) * 2 - 1

            c_real += (c_random - c_real) / t
            theta[theta_index] += minus * 0.01
            if theta[theta_index] > 2 * np.pi:
                theta[theta_index] = 0.0
        
        
    display_surf.fill(c_background)
    proj_points = geometry.proj(1, geometry.rot(Tesseract, *theta), 600)

    for i in range(0, len(Tesseract.lines)):
        j, k = Tesseract.lines[i]
        pygame.draw.aaline(display_surf, c_real, proj_points[j] + center_pos, proj_points[k] + center_pos)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            mouse_button = pygame.mouse.get_pressed()
        
        if event.type == MOUSEBUTTONUP:
            mouse_down = False
        
        if event.type == KEYDOWN:
            for i in range(0, 6):
                if theta_key[i] == event.key:
                    theta_index = i
                    print(theta_name[i])
                    break
            if event.key == K_SPACE:
                theta = [0, 0, 0, 0, 0, 0] #xy, xz, xw, yz, yw, zw
            if event.key == K_7:
                if auto:
                    auto = False
                else:
                    auto = True

    if mouse_down:
        print(theta[theta_index])
        if mouse_button[0]:
            theta[theta_index] -= 0.01
        if mouse_button[2]:
            theta[theta_index] += 0.01

    pygame.display.update()
    fps_clock.tick(fps)
