from board import Board
import pygame
from constants import * 



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    board = Board(screen)
    
    bg = pygame.image.load('src/images/background.jpeg')
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    
    pygame.display.set_caption('Main menu')
    
    run = True
    while run:
        screen.blit(bg, (0,0))
        #board.draw_board(screen)
        #board.draw_pieces(screen)
    
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
        
        pygame.display.update()
    pygame.quit()
    

if __name__ == '__main__':
    main()