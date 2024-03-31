from button import Button
from constants import WIDTH, HEIGHT, GREEN, BROWN, BLACK
import pygame
import pygame_menu

pygame.font.init()


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

player1_image = pygame.image.load('assets/images/player1-btn.png')
player1_image = pygame.transform.scale(player1_image, (250, 100))
player1_button = Button(WIDTH//2 - 125, 30, player1_image)

player2_image = pygame.image.load('assets/images/player2-btn.png')
player2_image = pygame.transform.scale(player2_image, (250, 100))
player2_button = Button(WIDTH//2 - 125, 200, player2_image)

theme = pygame_menu.themes.THEME_BLUE.copy()
theme.widget_font_color = BROWN  
theme.widget_font_shadow = True  
theme.widget_font_shadow_color = BLACK
theme.widget_font_shadow_offset = 2
theme.widget_font_shadow_position = pygame_menu.locals.POSITION_SOUTHEAST
theme.selection_color = GREEN

myimage = pygame_menu.baseimage.BaseImage(
    image_path='assets/images/background.jpg',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
)

font = pygame.font.Font('assets/fonts/default.ttf', 40)
theme.background_color = myimage
theme.widget_font = font
theme.title = False

def draw_main_menu(screen):
    
    pygame.display.set_caption('Main menu')

    screen.blit(bg, (0,0))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    start_button.draw_button(screen)
    options_button.draw_button(screen)
    quit_button.draw_button(screen)

    

def font(size):
    return pygame.font.Font('assets/fonts/default.ttf', size)


def set_difficulty_player1(value, difficulty):
    print(value)
    print(difficulty)

def set_difficulty_player2(value, difficulty):
    print(value)
    print(difficulty)
    
def draw_select_menu(select_menu):
    select_menu.add.image('assets/images/player1-btn.png', angle=0, scale=(0.16, 0.16))
    select_menu.add.selector(' ', [('Human', 0), ('Level 1 Bot', 1), ('Level 2 Bot', 2), ('Level 3 Bot', 3), ('Level 4 Bot', 4)], onchange=set_difficulty_player1)
    select_menu.add.image('assets/images/player2-btn.png', angle=0, scale=(0.16, 0.16))
    select_menu.add.selector(' ', [('Human', 0), ('Level 1 Bot', 1), ('Level 2 Bot', 2), ('Level 3 Bot', 3), ('Level 4 Bot', 4)], onchange=set_difficulty_player2)
    select_menu.add.label('')