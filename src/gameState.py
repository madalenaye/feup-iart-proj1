from typing import Tuple, List
from icecream import ic
class GameState:
    # the state is a 2D list 5x9 where (the board is inverted vertically relative to real life):
    #   -1 -> represents an empty slot
    #   0  -> represents a white piece
    #   1  -> represents a black piece
    state = [[-1 for _ in range(0, 9)] for _ in range(0,5)]

    applied_dirs = set()

    #player is always 0 or 1, where 0 represents the white player and 1 the black player
    player = 0

    def init_pieces(self) -> None:
        #init white pieces
        for i in range(0, 2):
            self.state[i] = [0 for _ in range(0, 9)]

        #middle pieces
        for i in range(0,4):
            self.state[2][i] = ~(i % 2)+2
        for i in range(5,9):
            self.state[2][i] = i % 2

        for i in range(3,5):
            self.state[i] = [1 for _ in range(0, 9)]
    
    def get_adjacent_squares(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        all_squares=[
            (pos[0]+1, pos[1]),
            (pos[0]-1, pos[1]),
            (pos[0], pos[1]+1),
            (pos[0], pos[1]-1)
        ]

        has_diagonal = pos[0] % 2 == 0

        if pos[1] % 2 == 1:
            has_diagonal = not has_diagonal
        
        if has_diagonal:
            all_squares.extend([
                (pos[0]+1, pos[1]+1),
                (pos[0]-1, pos[1]+1),
                (pos[0]-1, pos[1]-1),
                (pos[0]+1, pos[1]-1)
            ])

        return list(
                filter(lambda x: x[1] >= 0 and x[1] < 5, 
                filter(lambda x: x[0] >= 0 and x[0] < 9, all_squares)))

    # tuple has the form: (from_pos, to_pos)
    def check_if_move_takes(self, move: Tuple[Tuple[int,int],Tuple[int,int]]) -> bool:
        diff = (move[1][0]-move[0][0], move[1][1]-move[0][1])

        # check if there's a piece after the empty state
        print(self.state[move[1][1] + diff[1]][move[1][0] + diff[0]], diff)
        return self.state[move[1][1] + diff[1]][move[1][0] + diff[0]] == ~(self.player)+2

    # tuple has the form: (from_pos, to_pos)
    def get_valid_moves(self) -> List[Tuple[Tuple[int,int],Tuple[int,int]]]:
        valid_moves = set()
        player_pieces = [(x,y) for y,row in enumerate(self.state) for x,value in enumerate(row) if value == self.player]

        for piece in player_pieces:
            # check if adjcent square is free
            empty_squares = filter(lambda x: self.state[x[1]][x[0]] == -1,
                                    self.get_adjacent_squares(piece))
            for empty_square in empty_squares:
                valid_moves.add((piece, empty_square))

        piece_takes = list(map(lambda x: self.check_if_move_takes(x), valid_moves))
        if any(piece_takes):
            # return only the pieces that takes a enemy piece
            return list(
                map(
                    lambda x: x[0], 
                    filter(lambda x: x[1], 
                           zip(valid_moves, piece_takes))
                    )
                )
        
        return list(valid_moves)

    # tuple has the form: (from_pos, to_pos)
    def apply_move(self, move: Tuple[Tuple[int,int],Tuple[int,int]]) -> None:
        diff = (move[1][0]-move[0][0], move[1][1]-move[0][1])

        #replace start pos
        self.state[move[1][1]][move[1][0]] = self.state[move[0][1]][move[0][0]]
        self.state[move[0][1]][move[0][0]] = -1

        if not self.check_if_move_takes(move):
            self.player = ~(self.player)+2
            return
        
        curr_coords = (move[1][0] + diff[0], move[1][1] + diff[1])
        # while coordinates are valid
        while curr_coords[0] >= 0 and curr_coords[0] < 9 and curr_coords[1] >= 0 and curr_coords[1] < 5:
            # we exit the loop if there's no more adjacent pieces on this direction
            if self.state[curr_coords[1]][curr_coords[0]] != ~(self.player)+2:
                break
            self.state[curr_coords[1]][curr_coords[0]] = -1 # clear piece
            curr_coords = (curr_coords[0] + diff[0], curr_coords[1] + diff[1])
        
        new_valid_moves = filter(lambda x: x == move[1], self.get_valid_moves())
        piece_takes = list(map(lambda x: self.check_if_move_takes(x), new_valid_moves))
        # FIXME(luisd): check if piece takes are not in the same direction
        if any(piece_takes):
            return
        
        self.player = ~(self.player)+2
        
        
        


        
    def __init__(self) -> None:
        self.init_pieces()

if __name__ == "__main__":
    gs = GameState()
    ic(gs.state)
    valid_moves = gs.get_valid_moves()
    ic(valid_moves)
    gs.apply_move(valid_moves[0])
    ic(gs.state)
    ic(gs.player)