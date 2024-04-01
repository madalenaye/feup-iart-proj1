from board import Board
import pygame
import pygame_menu
from constants import * 
from icecream import ic
from menu import *
import sys
from montecarlo import MonteCarloNode, CustomPolicyMonteCarloNode
from gameTree import greedy


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 2 * PADDING))

current_player = get_curr_player()

# Options menu
def options(screen):
    
    pygame.display.set_caption('Options')
    options_menu = pygame_menu.Menu('Select mode',WIDTH, HEIGHT + 2 * PADDING, theme=theme)
    draw_options_menu(options_menu)
    options_menu.add.button('Save', main)
    
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        if options_menu.is_enabled():
            options_menu.update(events)
            options_menu.draw(screen)
        pygame.display.update()
    

# Menu to select the color of the pieces     
def choose_pieces(screen):
    pygame.display.set_caption('Choose pieces')
    choose_pieces_menu = pygame_menu.Menu('Which Player Starts First', WIDTH, HEIGHT + 2 * PADDING, theme=theme)
    draw_choose_pieces_menu(choose_pieces_menu)
    choose_pieces_menu.add.button('Play', play, screen)
    choose_pieces_menu.add.button('Back', main)
    
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        if choose_pieces_menu.is_enabled():
            choose_pieces_menu.update(events)
            choose_pieces_menu.draw(screen)

        pygame.display.update()

# Game mode: Huma
def human_play(board, screen):
    run = True
    while run:
        board.draw_board(screen)
        board.draw_pieces(screen)
        home_button.draw_button(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and home_button.selected(pygame.mouse.get_pos()):
                if home_button.selected(pygame.mouse.get_pos()):
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN and not board.selected_piece:
                pos = pygame.mouse.get_pos()
                row, col = board.get_row_col_from_mouse(pos)
                board.selected_piece = (col, row)
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN and board.selected_piece:
                row, col = board.get_row_col_from_mouse(pygame.mouse.get_pos())
                player = board.state.player
                board.draw_move(screen, board.selected_piece, (col,row))
                board.selected_piece = None
                if board.state.player != player:
                    run = False
                    break
            
        if board.selected_piece:
            board.draw_valid_moves(screen, row, col)
        
        if board.state.check_win_condition() != -1:
            break
        
        home_button.update(pygame.mouse.get_pos())
        pygame.display.update()
    pygame.display.update()

# Game mode: Level 1 Bot
def greedy_play(board, screen):
    pygame.display.update()
    pygame.time.wait(1000)
    moves = greedy(board.state)
    for move in moves:
        board.state = board.state.apply_move(move[0], move[1])
        board.draw_board(screen)
        board.draw_pieces(screen)
        pygame.display.update()
        pygame.time.wait(1000)
    if(board.state.check_win_condition() != -1):
        return -1

# Game mode: Level 2 Bot
def monte_carlo_play(board, screen):
    monte_carlo = MonteCarloNode(board.state.clone_board())
    node = monte_carlo.run_simulation(5)
    pygame.display.update()
    for move in node.moves:
        board.state = board.state.apply_move(move[0], move[1])
        board.draw_board(screen)
        board.draw_pieces(screen)
        pygame.display.update()
        pygame.time.wait(1000)
    if(board.state.check_win_condition() != -1):
        return -1

def custom_monte_carlo_play(board, screen):
    monte_carlo = CustomPolicyMonteCarloNode(board.state.clone_board())
    node = monte_carlo.run_simulation(5)
    pygame.display.update()
    for move in node.moves:
        board.state = board.state.apply_move(move[0], move[1])
        board.draw_board(screen)
        board.draw_pieces(screen)
        pygame.display.update()
        pygame.time.wait(1000)
    if(board.state.check_win_condition() != -1):
        return -1
    
# Game mode: Level 4 Bot   
def minimax_play(board, screen):
    pygame.display.update()
    pygame.time.wait(1000)
    moves = board.execute_best_move_minimax()
    for move in moves:
        board.state = board.state.apply_move(move[0], move[1])
        board.draw_board(screen)
        board.draw_pieces(screen)
        pygame.display.update()
        pygame.time.wait(1000)
    if(board.state.check_win_condition() != -1):
        return -1

# Game mode: Level 5 Bot
def alpha_beta_play(board, screen):
    pygame.display.update()
    pygame.time.wait(1000)
    moves = board.execute_best_move_alpha_beta()
    for move in moves:
        board.state = board.state.apply_move(move[0], move[1])
        board.draw_board(screen)
        board.draw_pieces(screen)
        pygame.display.update()
        pygame.time.wait(1000)
    if(board.state.check_win_condition() != -1):
        return -1
#Game mode: Level 6 Bot
def alpha_beta_heuristic_play(board, screen):
    pygame.display.update()
    pygame.time.wait(1000)
    moves = board.execute_best_move_alpha_beta_heuristic()
    for move in moves:
        board.state = board.state.apply_move(move[0], move[1])
        board.draw_board(screen)
        board.draw_pieces(screen)
        pygame.display.update()
        pygame.time.wait(1000)
    if(board.state.check_win_condition() != -1):
        return -1

# Main game loop
def play(screen):
    pygame.display.set_caption('Fanorona')
    board = Board()
    run = True
    global current_player
    current_player = get_curr_player()
    while run:
        board.draw_board(screen)
        board.draw_pieces(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        if (players_level(current_player) == 0):
            human_play(board, screen)
            
        elif (players_level(current_player) == 1):
            if (greedy_play(board, screen) == -1):
                game_over(screen, current_player)
                break
            
        elif (players_level(current_player) == 2):
            if (monte_carlo_play(board, screen) == -1):
                game_over(screen, current_player)
                break           
        
        elif (players_level(current_player) == 3):
            if (custom_monte_carlo_play(board, screen) == -1):
                game_over(screen, current_player)
                break       
            
        elif (players_level(current_player) == 4):
            if (minimax_play(board, screen) == -1):
                game_over(screen, current_player)
                break
            
        elif (players_level(current_player) == 5):
            
            if (alpha_beta_play(board, screen) == -1):
                game_over(screen, current_player)
                break
        
        elif (players_level(current_player) == 6):
            if (alpha_beta_heuristic_play(board, screen) == -1):
                game_over(screen, current_player)
                break
        
        current_player = -current_player
        
    
        pygame.display.update()

# game over menu
def game_over(screen, winner):
    game_over = pygame_menu.Menu(height=HEIGHT + 2 * PADDING,theme=theme,title='Game Over', width=WIDTH)
    draw_game_over_menu(game_over, winner)
    game_over.add.button('Exit', pygame_menu.events.EXIT)
    game_over.mainloop(screen)      
        
def main():

    run = True
    while run:
        
        draw_main_menu(screen)
        global current_player
        current_player = curr_player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.selected(pygame.mouse.get_pos()):
                    choose_pieces(screen)
                if options_button.selected(pygame.mouse.get_pos()):
                    options(screen)
                if quit_button.selected(pygame.mouse.get_pos()):
                    run = False
                
        mouse_pos = pygame.mouse.get_pos()
        start_button.update(mouse_pos)
        options_button.update(mouse_pos)
        quit_button.update(mouse_pos)
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
    

if __name__ == '__main__':
    main()