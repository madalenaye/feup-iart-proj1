from button import Button
from constants import WIDTH, HEIGHT
import pygame

bg = pygame.image.load('assets/images/background.jpg')
title = pygame.image.load('assets/images/fanorona.png')
start_image = pygame.image.load('assets/images/start-btn.png')
start_image = pygame.transform.scale(start_image, (250, 100))
start_button = Button(WIDTH//2 - 125, HEIGHT//2 - 90, start_image)

options_image = pygame.image.load('assets/images/options-btn.png')
options_image = pygame.transform.scale(options_image, (250, 100))
options_button = Button(WIDTH//2 - 125, HEIGHT//2, options_image)

quit_image = pygame.image.load('assets/images/quit-btn.png')
quit_image = pygame.transform.scale(quit_image, (250, 100))
quit_button = Button(WIDTH//2 - 125, HEIGHT//2 + 90, quit_image)

home_image = pygame.image.load('assets/images/home-btn.png')
home_image = pygame.transform.scale(home_image, (65, 65))
home_button = Button(WIDTH//2 - 70, HEIGHT - 25, home_image)

retry_image = pygame.image.load('assets/images/retry-btn.png')
retry_image = pygame.transform.scale(retry_image, (65, 65))
retry_button = Button(WIDTH//2 + 5, HEIGHT - 25, retry_image)

def draw_main_menu(screen):
    
    pygame.display.set_caption('Main menu')

    screen.blit(bg, (0,0))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    start_button.draw_button(screen)
    options_button.draw_button(screen)
    quit_button.draw_button(screen)

    

def font(size):
    return pygame.font.Font('assets/fonts/default.ttf', size)