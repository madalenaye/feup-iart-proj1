from gameState import GameState
from constants import *
from icecream import ic
import pygame

class Board:
    state = GameState()
    selected_piece = None
     
    def __init__(self, screen) -> None:
        self.state.init_pieces()
    
        
    def draw_board(self,screen):
        
        screen.fill(BOARD_COLOR)
        rows=len(self.state.state)
        cols = len(self.state.state[0])
        
        for row in range(rows):
            pygame.draw.line(screen, BLACK,(SQUARE_SIZE/2,SQUARE_SIZE/2 + row * SQUARE_SIZE),(cols*SQUARE_SIZE - SQUARE_SIZE/2,SQUARE_SIZE/2+row * SQUARE_SIZE),int(SQUARE_SIZE/25))
    
        for col in range(cols):
            pygame.draw.line(screen, BLACK,(SQUARE_SIZE/2 + col * SQUARE_SIZE,SQUARE_SIZE/2),(SQUARE_SIZE/2+col * SQUARE_SIZE,rows*SQUARE_SIZE - SQUARE_SIZE/2),int(SQUARE_SIZE/25))

        for col in range(cols//2):
            aux_col =col*2
            final_col=min(cols-1,aux_col+4)
            pygame.draw.line(screen, BLACK,(SQUARE_SIZE/2 + aux_col * SQUARE_SIZE,SQUARE_SIZE/2),(SQUARE_SIZE/2 + final_col * SQUARE_SIZE,SQUARE_SIZE/2 + (final_col-aux_col) * SQUARE_SIZE),int(SQUARE_SIZE/18))

            if col==0:
                final_col=min(cols-1,aux_col+2)
                pygame.draw.line(screen, BLACK,(SQUARE_SIZE/2 + aux_col * SQUARE_SIZE,5*SQUARE_SIZE/2),(SQUARE_SIZE/2 + final_col * SQUARE_SIZE,5*SQUARE_SIZE/2 + (final_col-aux_col) * SQUARE_SIZE),int(SQUARE_SIZE/18))

        for col in range(cols//2):
            aux_col =col*2+2
            final_col=max(0,aux_col-4)
            pygame.draw.line(screen, BLACK,(SQUARE_SIZE/2 + aux_col * SQUARE_SIZE,SQUARE_SIZE/2),(SQUARE_SIZE/2 + final_col * SQUARE_SIZE,SQUARE_SIZE/2 + (aux_col-final_col) * SQUARE_SIZE),int(SQUARE_SIZE/18))

            if col==3:
                final_col=max(0,aux_col-2)
                pygame.draw.line(screen, BLACK,(SQUARE_SIZE/2 + aux_col * SQUARE_SIZE,5*SQUARE_SIZE/2),(SQUARE_SIZE/2 + final_col * SQUARE_SIZE,5*SQUARE_SIZE/2 + (aux_col-final_col) * SQUARE_SIZE),int(SQUARE_SIZE/18))
    
    def draw_pieces(self, screen):
        col = 0
        row = 0
        for row in range(len(self.state.state)):
            for col in range(len(self.state.state[0])):
                x = col * SQUARE_SIZE + SQUARE_SIZE / 2
                y = row * SQUARE_SIZE + SQUARE_SIZE / 2
                i = self.state.state[row][col]
                if i != -1:
                    pygame.draw.circle(screen, BLACK, (x, HEIGHT-y), 25)
                    pygame.draw.circle(screen,  colors[i], (x, HEIGHT-y), 23)
    
    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = 4 - (y // SQUARE_SIZE) 
        col =  x // SQUARE_SIZE
        return row, col
    
    def get_piece(self, row, col):
        return self.state.state[row][col]
    
    def draw_valid_moves(self, screen, row, col):
        valid_moves = self.state.get_valid_moves()
        for move in valid_moves:
            from_pos, to_pos = move
            if (from_pos[0] == col and from_pos[1] == row):
                pygame.draw.circle(screen, GRAY, (to_pos[0] * SQUARE_SIZE + SQUARE_SIZE / 2, (4-to_pos[1]) * SQUARE_SIZE + SQUARE_SIZE / 2), 25)
    
    def draw_move(self, screen, from_pos, to_pos):
        valid_moves = self.state.get_valid_moves()
        if (from_pos, to_pos) not in valid_moves:
            return
        valid_move_types = self.state.check_if_move_takes((from_pos, to_pos)) 
        # FIXME(luisd): Refactor this in order to make user choose the capture type if there's multiple capture types
        self.state = self.state.apply_move((from_pos, to_pos), 
                                           None if valid_move_types == [] else valid_move_types[0])
        self.draw_pieces(screen)
            
        
    
    