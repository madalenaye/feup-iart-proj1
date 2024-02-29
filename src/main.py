from board import Board
import pygame



def main():
    pygame.init()
    width = 900
    height = 500
    screen = pygame.display.set_mode((width, height))
    BOARD_COLOR = (217, 217, 217)
    screen.fill(BOARD_COLOR)
    board = Board(screen)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        board.draw_lines(screen, width, height)
        board.draw_pieces(screen, width, height)
        pygame.display.update()
        
    pygame.quit()
    

if __name__ == '__main__':
    main()