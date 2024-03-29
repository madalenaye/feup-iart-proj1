from typing import Tuple, List
from typing_extensions import Self

from icecream import ic
from dataclasses import dataclass
from copy import deepcopy
from enum import Enum

CaptureType = Enum('CaptureType', ['APPROACH', 'WITHDRAWALL'])

@dataclass
class Line:
    vector: Tuple[int,int] = (0,0)
    initial_point: Tuple[int,int] = (0,0)

    # check if lines are equal by checking colinearity and if the point can be calculated
    # by the other vector
    def __eq__(self, __value: object) -> bool:
        if type(__value) != type(self):
            return False
        #check if vector is colinear by doing the dot product
        dot_z = self.vector[0]*__value.vector[1] - self.vector[1]*__value.vector[0]
        if dot_z != 0:
            return False
        
        # Handle division by 0 by checking if the other vector component isn't zero (because it will cause an
        #   indeterminate result, we also check if the there's no difference in the intial points on that 
        #   component
        if(self.vector[0] == 0):
            return self.vector[1] != 0 and (self.initial_point[0] - __value.initial_point[0]) == 0
        k_x = (self.initial_point[0] - __value.initial_point[0])/self.vector[0]

        if(self.vector[1] == 0):
            return self.vector[0] != 0 and (self.initial_point[1] - __value.initial_point[1]) == 0
        
        k_y = (self.initial_point[1] - __value.initial_point[1])/self.vector[1]

        
        if k_x != k_y:
            return False
        return True


class GameState:
    # the state is a 2D list 5x9 where (the board is inverted vertically relative to real life):
    #   -1 -> represents an empty slot
    #   0  -> represents a white piece
    #   1  -> represents a black piece
    state = [[-1 for _ in range(0, 9)] for _ in range(0,5)]

    applied_lines: List[Line] = []
    occupied_positions: List[Tuple[int,int]] = []

    applied_piece: Tuple[int, int] = None

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

        return filter(lambda x: x[1] >= 0 and x[1] < 5, 
                filter(lambda x: x[0] >= 0 and x[0] < 9, all_squares))

    # tuple has the form: (from_pos, to_pos)
    def check_if_move_takes(self, move: Tuple[Tuple[int,int],Tuple[int,int]]) -> List[CaptureType]:
        diff = (move[1][0]-move[0][0], move[1][1]-move[0][1])
        result = []

        if (move[1][1] + diff[1] >= 0 and move[1][1] + diff[1] < 5 and move[1][0] + diff[0] >= 0 and move[1][0] + diff[0] < 9):
            # check if there's a piece after the empty state (attack by approach)
            if self.state[move[1][1] + diff[1]][move[1][0] + diff[0]] == ~(self.player)+2:
                result.append(CaptureType.APPROACH)
        
        # check if there's a piece behind the source piece (attack by withdrawal) and then check if the destiination piece is empty
        if (move[0][1] - diff[1] >= 0 and move[0][1] - diff[1] < 5 and move[0][0] - diff[0] >= 0 and move[0][0] - diff[0] < 9):
            if self.state[move[1][1]][move[1][0]] == -1 and self.state[move[0][1] - diff[1]][move[0][0] - diff[0]] == ~(self.player)+2:
                result.append(CaptureType.WITHDRAWALL)
    
        return result

    # tuple has the form: (from_pos, to_pos)
    def get_valid_moves(self) -> List[Tuple[Tuple[int,int],Tuple[int,int]]]:
        valid_moves = set(
            [(start_pos, empty_square) 
            for start_pos in [(x,y) for y,row in enumerate(self.state)for x,value in enumerate(row) if value == self.player]
            for empty_square in filter(lambda x: self.state[x[1]][x[0]] == -1,
                self.get_adjacent_squares(start_pos))
        ])
        
        #filter valid moves by checking if the line has been already used
        valid_moves = filter(
                lambda x: Line((x[1][0]-x[0][0], x[1][1]-x[0][1]), x[0]) not in self.applied_lines,valid_moves
                )
        if self.applied_piece is not None:
            # ic(self.applied_piece, valid_moves)
            valid_moves = filter(lambda x: x[0] == self.applied_piece, valid_moves)
        if len(self.occupied_positions) != 0:
            valid_moves = filter(lambda x: x[1] not in self.occupied_positions, valid_moves)

        valid_moves = set(valid_moves)

        piece_takes = list(map(lambda x: self.check_if_move_takes(x), valid_moves))
        if any(piece != [] for piece in piece_takes):
            # return only the pieces that takes a enemy piece
            return list(
                map(
                    lambda x: x[0], 
                    filter(lambda x: x[1] != [], 
                           zip(valid_moves, piece_takes))
                    )
                )
        
        return list(valid_moves)

    # tuple has the form: (from_pos, to_pos)
    def apply_move(self, move: Tuple[Tuple[int,int],Tuple[int,int]], captureType: CaptureType) -> Self:
        diff = (move[1][0]-move[0][0], move[1][1]-move[0][1])

        move_type = self.check_if_move_takes(move)
        new_board = self.clone_board()
        if move_type == [] and captureType is None:
            new_board.state[move[1][1]][move[1][0]] = new_board.state[move[0][1]][move[0][0]]
            new_board.state[move[0][1]][move[0][0]] = -1
            new_board.player = ~(self.player)+2
            return new_board
        if captureType not in move_type:
            return self
        
        #replace start pos
        new_board.state[move[1][1]][move[1][0]] = new_board.state[move[0][1]][move[0][0]]
        new_board.state[move[0][1]][move[0][0]] = -1

        if captureType == CaptureType.APPROACH:
            curr_coords = (move[1][0] + diff[0], move[1][1] + diff[1])
            # while coordinates are valid
            while curr_coords[0] >= 0 and curr_coords[0] < 9 and curr_coords[1] >= 0 and curr_coords[1] < 5:
                # we exit the loop if there's no more adjacent pieces on this direction
                if new_board.state[curr_coords[1]][curr_coords[0]] != ~(new_board.player)+2:
                    break
                new_board.state[curr_coords[1]][curr_coords[0]] = -1 # clear piece
                curr_coords = (curr_coords[0] + diff[0], curr_coords[1] + diff[1])
        else:
            curr_coords = (move[0][0] - diff[0], move[0][1] - diff[1])
            # while coordinates are valid
            while curr_coords[0] >= 0 and curr_coords[0] < 9 and curr_coords[1] >= 0 and curr_coords[1] < 5:
                # we exit the loop if there's no more adjacent pieces on this direction
                if new_board.state[curr_coords[1]][curr_coords[0]] != ~(new_board.player)+2:
                    break
                new_board.state[curr_coords[1]][curr_coords[0]] = -1 # clear piece
                curr_coords = (curr_coords[0] - diff[0], curr_coords[1] - diff[1])
        
        new_board.applied_piece = move[1]
        new_board.occupied_positions.append(move[0])
        new_board.applied_lines.append(Line(diff, move[0]))
        new_valid_moves = new_board.get_valid_moves()
        piece_takes = list(map(lambda x: new_board.check_if_move_takes(x), new_valid_moves))

        # ic(new_valid_moves, piece_takes, any(piece_takes), new_board.applied_piece)

        if any(piece_takes):
            return new_board
        
        new_board.applied_piece = None
        new_board.player = ~(new_board.player)+2
        new_board.applied_lines = []
        new_board.occupied_positions = []
        # ic(new_board.get_valid_moves())
        return new_board
        
        
    def __init__(self, state=[], applied_lines=[], occupied_positions=[], applied_piece=None, player=0) -> None:
        if state == []:
            self.init_pieces()
        else:
            self.state = state
            self.applied_lines = applied_lines
            self.occupied_positions = occupied_positions
            self.applied_piece = applied_piece
            self.player = player
    
    # cloning function in order to avoid python shenanigans with shallow copying
    def clone_board(self) -> Self:
        cloned_state = list(map(lambda x: x.copy(), self.state))
        return GameState(
            cloned_state, 
            self.applied_lines.copy(), 
            self.occupied_positions.copy(), 
            self.applied_piece, 
            self.player)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, GameState):
            return False
        result = self.state == __value.state 
        result &= self.applied_lines == __value.applied_lines 
        result &= self.occupied_positions == __value.occupied_positions 
        result &= self.applied_piece == __value.applied_piece 
        result &= self.player == __value.player
        return result

    def __hash__(self) -> int:
        return hash((tuple(list(map(lambda x: tuple(x), self.state))), 
                     tuple(self.applied_lines), 
                     tuple(self.occupied_positions), 
                     self.applied_piece, 
                     self.player))

    def check_win_condition(self) -> int:
        """
            Returns 0 if black won, 1 if white won or -1 if the game continues
        """
        flattened_state = [item for row in self.state for item in row]
        if(not any(map(lambda x: x == 1, flattened_state))):
            return 0
        if(not any(map(lambda x: x == 0, flattened_state))):
            return 1
        return -1
        

if __name__ == "__main__":
    ic(Line((1,0), (0,0)) == Line((-1,0),(1,0)))
    gs = GameState()
    ic(gs.state)
    valid_moves = gs.get_valid_moves()
    ic(valid_moves)
    gs.apply_move(valid_moves[0])
    ic(gs.state)
    ic(gs.player)
    ic(gs.get_valid_moves())        