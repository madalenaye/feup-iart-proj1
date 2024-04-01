import time
from gameState import GameState
from gameTree import *
from minimax import *
from constants import *
from icecream import ic
import sys
import pygame

class Board:
    state : GameState = GameState()
    selected_piece = None
     
    def __init__(self) -> None:
        self.state.init_pieces()
    
    # Draws the board lines
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
    
    # Draws the pieces on the board
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
    
    # Returns the row and column of the clicked piece
    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = 4 - (y // SQUARE_SIZE) 
        col =  x // SQUARE_SIZE
        return row, col
    
    def get_piece(self, row, col):
        return self.state.state[row][col]
    
    # Draws the valid moves for the selected piece
    def draw_valid_moves(self, screen, row, col):
        valid_moves = self.state.get_valid_moves()
        for move in valid_moves:
            from_pos, to_pos = move
            if (from_pos[0] == col and from_pos[1] == row):
                if (self.state.player == 0):
                    pygame.draw.circle(screen, GREEN, (to_pos[0] * SQUARE_SIZE + SQUARE_SIZE / 2, (4-to_pos[1]) * SQUARE_SIZE + SQUARE_SIZE / 2), 25)
                else:
                    pygame.draw.circle(screen, GREEN, (to_pos[0] * SQUARE_SIZE + SQUARE_SIZE / 2, (4-to_pos[1]) * SQUARE_SIZE + SQUARE_SIZE / 2), 25)
    
    # returns the best move for the current player using the minimax algorithm
    def execute_best_move_minimax(self) -> List[MoveType]:
        best_minimax_value = float('-inf')
        best_move = None

        for next_state, moves in get_next_moves(self.state):
            # Call minimax function to get the value
            minimax_value = minimax(next_state, depth=2, ai_player=self.state.player)  # Adjust depth as needed

            # Update best move if necessary
            if minimax_value > best_minimax_value:
                best_minimax_value = minimax_value
                best_move = moves
        # Execute the best move
        return best_move
    

    def execute_best_move_alpha_beta(self) -> List[MoveType]:
        best_minimax_value = float('-inf')
        best_move = None

        for next_state, moves in get_next_moves(self.state):
            # Call minimax function to get the value
            minimax_value = alpha_beta(next_state, depth=5, ai_player=self.state.player,alpha=float('-inf'),beta=float('inf'))  # Adjust depth as needed

            # Update best move if necessary
            if minimax_value > best_minimax_value:
                best_minimax_value = minimax_value
                best_move = moves
        # Execute the best move
        return best_move

    def execute_best_move_alpha_beta_heuristic(self) -> List[MoveType]:
        best_minimax_value = float('-inf')
        best_move = None

        for next_state, moves in get_next_moves(self.state):
            # Call minimax function to get the value
            minimax_value = alpha_beta_heuristic(next_state, depth=5, ai_player=self.state.player,alpha=float('-inf'),beta=float('inf'))  # Adjust depth as needed

            # Update best move if necessary
            if minimax_value > best_minimax_value:
                best_minimax_value = minimax_value
                best_move = moves
        # Execute the best move
        return best_move

    # handles the moves where the player has multiple types of captures
    def draw_move_types(self, screen, move, valid_move_types):
        diff = (move[1][0] - move[0][0], move[1][1] - move[0][1])
        
        # horizontal moves
        if diff == (1,0) or diff == (-1,0):
            pygame.draw.circle(screen, RED, ((move[0][0] + diff[0]*2) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1]) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
            pygame.draw.circle(screen, RED, ((move[0][0] - diff[0]) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1]) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
        # vertical moves
        if diff == (0,-1):
            pygame.draw.circle(screen, RED, ((move[0][0]) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1] - 1) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
            pygame.draw.circle(screen, RED, ((move[0][0]) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1] + 2) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
        if diff == (0, 1):
            pygame.draw.circle(screen, RED, ((move[0][0]) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1] + 1) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
            pygame.draw.circle(screen, RED, ((move[0][0]) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1] - 2) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
        # diagonal moves
        if diff == (1, -1) or diff == (-1, -1): 
            pygame.draw.circle(screen, RED, ((move[0][0] + diff[0]*2) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1] + 2) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
            pygame.draw.circle(screen, RED, ((move[0][0] - diff[0]) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1] - 1 ) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
        if diff == (-1, 1) or diff == (1,1):
            pygame.draw.circle(screen, RED, ((move[0][0] + diff[0]*2) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1] - 2) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)
            pygame.draw.circle(screen, RED, ((move[0][0] - diff[0]) * SQUARE_SIZE + SQUARE_SIZE / 2, (4-move[0][1] + 1 ) * SQUARE_SIZE + SQUARE_SIZE / 2), 10)

    def draw_move(self, screen, from_pos, to_pos):
        valid_moves = self.state.get_valid_moves()
        if (from_pos, to_pos) not in valid_moves:
            return
        valid_move_types = self.state.check_if_move_takes((from_pos, to_pos))
        ic(valid_move_types)
        if len(valid_move_types) < 2:
            self.state = self.state.apply_move((from_pos, to_pos), 
                                            None if valid_move_types == [] else valid_move_types[0])
        else:
            # move type selection
            run = True
            while run:
                self.draw_move_types(screen, (from_pos, to_pos), valid_move_types)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = self.get_row_col_from_mouse(pygame.mouse.get_pos())
                        diff = (to_pos[0] - from_pos[0], to_pos[1] - from_pos[1])
                        if (to_pos[1]+diff[1], to_pos[0]+diff[0]) == click:
                            self.state = self.state.apply_move((from_pos, to_pos), CaptureType.APPROACH)
                        elif (from_pos[1]-diff[1], from_pos[0]-diff[0]) == click:
                            self.state = self.state.apply_move((from_pos, to_pos), CaptureType.WITHDRAWAL)
                        run = False
                pygame.display.update()
            
        self.state.check_win_condition()
        self.draw_board(screen)
        self.draw_pieces(screen)

            
        
    
if __name__ == '__main__':
    board = Board()
    start = time.time()
    board.execute_best_move()
    print(f"Took {time.time() - start}s")