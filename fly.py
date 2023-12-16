import pygame
from pygame.locals import *

pygame.init()


screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# This defines game variables
ground_scroll = 0
scroll_speed = 4

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

run = True
while run:

    #Draw the background
    screen.blit(bg, (0,0))

    #Draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, 768))
    ground_scroll = scroll_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

