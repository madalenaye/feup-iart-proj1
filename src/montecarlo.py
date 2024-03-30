from collections import defaultdict
from typing import Any, List, Tuple

from gameState import GameState
from gameTree import MoveType, TreeNode, get_next_moves
import random
from math import sqrt,log
import time
CONST_UCB = 1.4

class MonteCarloNode(TreeNode):
    _visits = 0
    _results = defaultdict(int)
    _untried_moves: List[Tuple[GameState, MoveType]] = []
    _intended_player : int

    def __init__(self, state, moves = [], intended_player = -1) -> None:
        """
            When intended_player is not specified (-1), it will default to the current player's on that state
        """
        super().__init__(state, moves)
        # wins have key 1, losses have key -1, there are no draws in the context of this game
        self._results[1] = 0
        self._results[-1] = 0
        self._intended_player = intended_player if intended_player != -1 else self.state.player
        self.untried_actions()
    
    def q(self):
        return self._results[1] - self._results[-1]

    def n(self):
        return self._visits

    def untried_actions(self):

        self._untried_moves = list(get_next_moves(self.state))
        return self._untried_moves
    
    def is_fully_expanded(self):
        return len(self._untried_moves) == 0
    
    def expand(self):
        # i think it's best to select a random move from the bunch, to avoid "local optima".
        # In the grand scheme of things, it's okay to do this because MCST is just a statistical method.
        next_action = random.choice(self._untried_moves)
        # next_action = self._untried_moves[0]
        self._untried_moves.remove(next_action)

        new_node = MonteCarloNode(next_action[0], next_action[1], self._intended_player)
        self.add_children(new_node)
        
        return new_node
    
    def best_child(self):
        return max(
            self.children, 
            key= lambda x: (x.q()/x.n()) + CONST_UCB * sqrt(log(self.n()) / x.n())
        )
    
    def _selection_policy(self):

        current_node = self
        # we check if the node hasn't already ended
        while not current_node.state.check_win_condition() != -1:
            if not current_node.is_fully_expanded():
                # print("EXPAND")
                return current_node.expand()
            else:
                current_node = current_node.best_child()    
        return current_node
    
    def _simulation_policy(self, parent, next_moves):
        return random.choice(next_moves)[0]

    def simulate(self, simulation_func):
        current_game_state = self.state

        while not current_game_state.check_win_condition() != -1:
            
            # need to convert get_next_moves to a list, because random.choice requires len and get
            current_game_state = simulation_func(current_game_state, list(get_next_moves(current_game_state)))
        
        return 1 if current_game_state.check_win_condition() == self._intended_player else -1
    
    def backpropagate(self, result):
        
        current_node = self
        while current_node != None:
            current_node._results[result] += 1
            current_node._visits += 1

            current_node = current_node.previous

    def run_simulation(self, max_computation_time=5, max_simulations=2000):
        """
            max_computation_time is determined in seconds
        """
        start_time = time.time()
        simulations_ran = 0
        while time.time() - start_time < max_computation_time:
            if simulations_ran > max_simulations:
                break
            selected_node = self._selection_policy()
            result = selected_node.simulate(self._simulation_policy)
            selected_node.backpropagate(result)
            simulations_ran += 1

        print(f"Simulations ran: {simulations_ran}")

        return self.best_child()
    
class CustomPolicyMonteCarloNode(MonteCarloNode):
    def __init__(self, state, moves = [], intended_player = -1) -> None:
        super().__init__(state, moves, intended_player)

    def _simulation_policy(self, parent, next_moves) -> Any:
        if next_moves[0][1][0][1] == None:
            return random.choice(next_moves)[0]
        max_diff = max(map(lambda x: len(x[1]), next_moves))
        return random.choice(list([move for move in next_moves if len(move[1]) == max_diff]))[0]


if __name__ == '__main__':
    
    state = GameState()
    move = state.get_valid_moves()[0]
    state = state.apply_move(move, state.check_if_move_takes(move)[0])

    # we start monte carlo on the first move of the black pieces
    monte_carlo = MonteCarloNode(state)
    best_move = monte_carlo.run_simulation(5)
    print(best_move)