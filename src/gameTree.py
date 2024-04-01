from typing import Iterator, List, Tuple
from gameState import CaptureType, GameState
from icecream import ic

MoveType = Tuple[Tuple[Tuple[int, int], Tuple[int, int]], CaptureType]

class TreeNode:
    state: GameState
    moves: List[MoveType]
    previous: 'TreeNode' = None
    children: List['TreeNode']

    def __init__(self, state, moves = []) -> None:
        self.state = state
        self.moves = moves
        self.children = []

    def add_children(self, child: 'TreeNode'):
        self.children.append(child)
        child.previous = self

# This assumes that capture is always obligatory.
def get_next_moves(intial_state: GameState) -> Iterator[Tuple[GameState, List[MoveType]]]:
    """
        This takes a GameState and returns all sequences of moves lazily. This returns a tuple with
        the new GameState (where it's always the opposite player's turn) and the sequence of moves required
        to make it onto the the new state (because there can be multiple moves in a player's turn).  
    """
    moves = intial_state.get_valid_moves()
    if moves == []:
        return
    # if there's a non capture move avaliable we can assume that all list elements are non-capture moves
    if intial_state.check_if_move_takes(moves[0]) == []:
        for i in moves:
            new_state = intial_state.apply_move(i, None)
            yield (new_state, [(i, None)])
        return

    def helper(state:GameState, list_moves:List[MoveType]) -> Iterator[Tuple[GameState, List[MoveType]]]:
        new_moves = state.get_valid_moves()
        for capture_move in new_moves:
            types = state.check_if_move_takes(capture_move)
            for capture_type in types:
                new_state = state.apply_move(capture_move, capture_type)
                if(new_state.player != state.player):
                    # We reached a state where there are no consequent moves, therefore we can return
                    yield (new_state, [*list_moves, (capture_move, capture_type)])
                else:
                    yield from helper(new_state, [*list_moves, (capture_move, capture_type)])
                
    
    yield from helper(intial_state, [])


def greedy(state: GameState) -> List[MoveType]:
    
    node = TreeNode(state)
    scores = []
    
    for i in get_next_moves(node.state):
        child_node = TreeNode(i[0], i[1])
        node.add_children(child_node)
        
    for child in node.children:
        new_state = child.state
        score = new_state.evaluate_game_state(state.player)
        print(score)
        scores.append((child, score))
        

    best_child = max(scores, key=lambda x: x[1])
    print(best_child[0].moves)
    return best_child[0].moves

    
    

if __name__ == '__main__':
    # Here you can see how to get the next moves, you want to incorporate a version of this into your search function.
    #  get_next_moves() is lazy so you can stop the get_next_moves in the middle (in case of alpha beta pruning) in a
    #  more efficient way
    ic(list(get_next_moves(GameState())))
    node = TreeNode(GameState())
    for i in get_next_moves(node.state):
        child_node = TreeNode(i[0], i[1])
        node.add_children(child_node)
    
    state = GameState()
    mov = greedy(state, 1)
    for (i, j) in mov:
        new_state = state.apply_move(i, j)
    ic(greedy(new_state, 0))