from board import Board
import pygame
from constants import *
from montecarlo import MonteCarloNode 
from gameTree import minimax,TreeNode
import time



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    board = Board(screen)

    board.draw_board(screen)
    board.draw_pieces(screen)
    pygame.display.update()
    
    run = True
    while run:
        board.draw_board(screen)
        board.draw_pieces(screen)

        if board.state.player == 0:
            pygame.display.update()
            board.execute_best_move(screen)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
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



            
        pygame.display.update()
    pygame.quit()
    

if __name__ == '__main__':
    main()