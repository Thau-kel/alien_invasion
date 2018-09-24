import sys
import pygame

def launch_screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Events Detecting...')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
      
        pygame.display.flip()

launch_screen()