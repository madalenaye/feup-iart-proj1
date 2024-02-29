from gameState import GameState
import pygame

class Board:
    state = GameState()
    SQUARE_SIZE = 100
    colors = {
        0: (255,255,255),
        1: (26,31,36),
        -1: (196, 157, 123)
    }
     
    def __init__(self, screen) -> None:
        self.state.init_pieces()
    

    def draw_lines(self,screen,width,height):
        screen.fill((196, 157, 123))
        
        rows=len(self.state.state)
        cols = len(self.state.state[0])
        
        for row in range(rows):
            pygame.draw.line(screen, (0,0,0),(self.SQUARE_SIZE/2,self.SQUARE_SIZE/2 + row * self.SQUARE_SIZE),(cols*self.SQUARE_SIZE - self.SQUARE_SIZE/2,self.SQUARE_SIZE/2+row * self.SQUARE_SIZE),int(self.SQUARE_SIZE/25))
    
        for col in range(cols):
            pygame.draw.line(screen, (0,0,0),(self.SQUARE_SIZE/2 + col * self.SQUARE_SIZE,self.SQUARE_SIZE/2),(self.SQUARE_SIZE/2+col * self.SQUARE_SIZE,rows*self.SQUARE_SIZE - self.SQUARE_SIZE/2),int(self.SQUARE_SIZE/25))

        for col in range(cols//2):
            aux_col =col*2
            final_col=min(cols-1,aux_col+4)
            pygame.draw.line(screen, (0,0,0),(self.SQUARE_SIZE/2 + aux_col * self.SQUARE_SIZE,self.SQUARE_SIZE/2),(self.SQUARE_SIZE/2 + final_col * self.SQUARE_SIZE,self.SQUARE_SIZE/2 + (final_col-aux_col) * self.SQUARE_SIZE),int(self.SQUARE_SIZE/18))

            if col==0:
                final_col=min(cols-1,aux_col+2)
                pygame.draw.line(screen, (0,0,0),(self.SQUARE_SIZE/2 + aux_col * self.SQUARE_SIZE,5*self.SQUARE_SIZE/2),(self.SQUARE_SIZE/2 + final_col * self.SQUARE_SIZE,5*self.SQUARE_SIZE/2 + (final_col-aux_col) * self.SQUARE_SIZE),int(self.SQUARE_SIZE/18))

        for col in range(cols//2):
            aux_col =col*2+2
            final_col=max(0,aux_col-4)
            pygame.draw.line(screen, (0,0,0),(self.SQUARE_SIZE/2 + aux_col * self.SQUARE_SIZE,self.SQUARE_SIZE/2),(self.SQUARE_SIZE/2 + final_col * self.SQUARE_SIZE,self.SQUARE_SIZE/2 + (aux_col-final_col) * self.SQUARE_SIZE),int(self.SQUARE_SIZE/18))

            if col==3:
                final_col=max(0,aux_col-2)
                pygame.draw.line(screen, (0,0,0),(self.SQUARE_SIZE/2 + aux_col * self.SQUARE_SIZE,5*self.SQUARE_SIZE/2),(self.SQUARE_SIZE/2 + final_col * self.SQUARE_SIZE,5*self.SQUARE_SIZE/2 + (aux_col-final_col) * self.SQUARE_SIZE),int(self.SQUARE_SIZE/18))
    
    def draw_pieces(self, screen, width, height):
        col = 0
        row = 0
        for row in range(len(self.state.state)):
            for col in range(len(self.state.state[0])):
                x = col * self.SQUARE_SIZE + self.SQUARE_SIZE / 2
                y = row * self.SQUARE_SIZE + self.SQUARE_SIZE / 2
                i = self.state.state[row][col]
                if i != -1:
                    pygame.draw.circle(screen, (0,0,0), (x, height-y), 27)
                    pygame.draw.circle(screen, self.colors[i], (x, height-y), 25)
        
    