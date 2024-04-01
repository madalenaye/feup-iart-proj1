from button import Button
from constants import WIDTH, HEIGHT, GREEN, BROWN, BLACK
import pygame
import pygame_menu

pygame.font.init()

'''0 - Human, 1 - Level 1 Bot, 2 - Level 2 Bot, 3 - Level 3 Bot, 4 - Level 4 Bot'''
player1 = 0
player2 = 0

'''1 - player 1, -1 - player 2'''
curr_player = 1

# Load images
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
home_button = Button(WIDTH//2 - 33, HEIGHT - 25, home_image)

# Theme for the menus
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

# Auxiliar functions to draw the menus
def draw_main_menu(screen):
    
    pygame.display.set_caption('Main menu')

    screen.blit(bg, (0,0))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    start_button.draw_button(screen)
    options_button.draw_button(screen)
    quit_button.draw_button(screen)


def font(size):
    return pygame.font.Font('assets/fonts/default.ttf', size)

# Auxiliar functions to set the options
def set_difficulty_player1(value, difficulty):
    global player1
    player1 = difficulty

def set_difficulty_player2(value, difficulty):
    global player2
    player2 = difficulty

def set_pieces_color(value, color):
    global curr_player 
    curr_player = color

    
def draw_options_menu(options_menu):
    options_menu.add.image('assets/images/player1-btn.png', angle=0, scale=(0.16, 0.16))
    options_menu.add.selector(' ', [('Human', 0), ('Level 1 Bot', 1), ('Level 2 Bot', 2), ('Level 3 Bot', 3), ('Level 4 Bot', 4), ('Level 5 Bot', 5)], onchange=set_difficulty_player1)
    options_menu.add.image('assets/images/player2-btn.png', angle=0, scale=(0.16, 0.16))
    options_menu.add.selector(' ', [('Human', 0), ('Level 1 Bot', 1), ('Level 2 Bot', 2), ('Level 3 Bot', 3), ('Level 4 Bot', 4), ('Level 5 Bot', 5)], onchange=set_difficulty_player2)
    options_menu.add.label('')
    
def draw_choose_pieces_menu(choose_pieces_menu):
    choose_pieces_menu.add.image('assets/images/player1-btn.png', angle=0, scale=(0.16, 0.16))
    choose_pieces_menu.add.selector(' ', [('White', 1), ('Black', -1)], onchange=set_pieces_color)

# Auxiliar function to get the current player level
def players_level(curr_player):
    if curr_player == 1:
        return player1
    else:
        return player2

# Auxiliar function to draw the game over menu

def draw_game_over_menu(game_over, winner):
    if (winner == 1):
        game_over.add.label('Player 1' + ' wins!', font_size=40)
    else:
        game_over.add.label('Player 2' + ' wins!', font_size=40)
        
def get_curr_player():
    return curr_player
