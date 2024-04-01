from board import Board
import pygame
import pygame_menu
from constants import * 
from menu import *
import sys
from montecarlo import MonteCarloNode, CustomPolicyMonteCarloNode
from gameTree import greedy, TreeNode
import time


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 2 * PADDING))


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


def play(screen):
    pygame.display.set_caption('Fanorona')
    board = Board()
    run = True
    while run:
        board.draw_board(screen)
        board.draw_pieces(screen)
        home_button.draw_button(screen)
        retry_button.draw_button(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and (home_button.selected(pygame.mouse.get_pos()) or retry_button.selected(pygame.mouse.get_pos())):
                if home_button.selected(pygame.mouse.get_pos()):
                    main()
                if retry_button.selected(pygame.mouse.get_pos()):
                    board = Board()
                    continue
            if (players_level(curr_player) == 0):
                human_play(board, screen)
            elif (players_level(curr_player) == 1):
                greedy_play(board, screen)
            elif (players_level(curr_player) == 2):
                minimax_play(board, screen)
            elif (players_level(curr_player) == 3):
                monte_carlo_play(board, screen)
            elif (players_level(curr_player) == 4):
                alpha_beta_play(board, screen)
'''
def play(screen):
    
    pygame.display.set_caption('Fanorona')
    board = Board()
    run = True
    while run:
        board.draw_board(screen)
        board.draw_pieces(screen)
        home_button.draw_button(screen)
        retry_button.draw_button(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and (home_button.selected(pygame.mouse.get_pos()) or retry_button.selected(pygame.mouse.get_pos())):
                if home_button.selected(pygame.mouse.get_pos()):
                    main()
                if retry_button.selected(pygame.mouse.get_pos()):
                    board = Board()
                    continue
            if event.type == pygame.MOUSEBUTTONDOWN and not board.selected_piece:
                pos = pygame.mouse.get_pos()
                row, col = board.get_row_col_from_mouse(pos)
                board.selected_piece = (col, row)
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN and board.selected_piece:
                row, col = board.get_row_col_from_mouse(pygame.mouse.get_pos())
                board.draw_move(screen, board.selected_piece, (col,row))
                board.selected_piece = None
            
            
        if board.selected_piece:
            board.draw_valid_moves(screen, row, col)

        if board.state.player == 0:

            if(board.state.check_win_condition() != -1):
                break
            print("running greedy")
            moves = greedy(board.state)
            for move in moves:
                board.state = board.state.apply_move(move[0], move[1])
                board.draw_board(screen)
                board.draw_pieces(screen)
                pygame.display.update()
                pygame.time.wait(1000)
                
        # if board.state.player == 1:
        #     board.draw_board(screen)
        #     board.draw_pieces(screen)
        #     pygame.display.update()
        #     if(board.state.check_win_condition() != -1):
        #         break
        #     print("running monte carlo")
        #     monte_carlo = MonteCarloNode(board.state.clone_board())
        #     node = monte_carlo.run_simulation(5)
        #     print("found move")
        #     for move in node.moves:
        #         board.state = board.state.apply_move(move[0], move[1])
        #         board.draw_board(screen)
        #         board.draw_pieces(screen)
        #         pygame.display.update()
        #         pygame.time.wait(1000)
                
        
        home_button.update(pygame.mouse.get_pos())
        retry_button.update(pygame.mouse.get_pos())
        
        pygame.display.update()
'''       
        
        
def main():

    run = True
    while run:
        
        draw_main_menu(screen)
              
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