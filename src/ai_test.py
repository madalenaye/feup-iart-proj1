import multiprocessing
import itertools
from typing import List, Tuple

from board import Board
from gameState import GameState
from gameTree import MoveType
from icecream import ic
from montecarlo import MonteCarloNode, CustomPolicyMonteCarloNode

NUM_OF_TURNS = 100
NUM_OF_GAMES = 15
AI_LIST = ["minimax", "montecarlo", "custom_montecarlo", "alpha-beta"]


def step_game(ai_type: str, state: GameState) -> GameState:
    move : List[MoveType] = None
    if ai_type == "minimax":
        board = Board()
        board.state = state
        move = board.execute_best_move_minimax()
    if ai_type == "montecarlo":
        node = MonteCarloNode(state)
        new_node = node.run_simulation(max_computation_time=5)
        move = new_node.moves
    if ai_type == "custom_montecarlo":
        node = CustomPolicyMonteCarloNode(state)
        new_node = node.run_simulation(max_computation_time=5)
        move = new_node.moves
    if ai_type == "alpha-beta":
        board = Board()
        board.state = state
        move = board.execute_best_move_alpha_beta()

    if move == None:
        print(f"Didn't found moves in {ai_type}, win condition: {state.check_win_condition()}")
        ic(state.state, state.player)
    new_state = state
    for step in move:
        new_state = new_state.apply_move(step[0], step[1])
    
    return new_state


def playout_game(args: Tuple[str, str]) -> Tuple[Tuple[str, str], str]:
    state = GameState()
    for i in range(NUM_OF_TURNS):
        state = step_game(args[i % 2], state)
        if state.check_win_condition() != -1:
            return (args, args[state.check_win_condition()])
    #Return a draw
    return (args, None)

def main():
    # we need permutations because we want to them to play on both sides, to avoid bias
    game_list: List[Tuple[str, str]] = itertools.permutations(AI_LIST, 2)
    game_list = itertools.repeat(list(game_list), NUM_OF_GAMES)
    game_list = [ item for row in game_list for item in row ]
    game_list = list(game_list)

    # format: tuple with adversaries -> tuple with wins of adversary 0, wins of adversary 1, and "draws"
    stats = {}

    with multiprocessing.Pool(multiprocessing.cpu_count() - 2) as pool:
        # one game per cpu, seems okay
        games = pool.imap_unordered(playout_game, game_list, 1)
        for result in games:

            normalized_game = tuple(sorted(list(result[0])))
            if normalized_game not in stats:
                stats[normalized_game] = (0,0,0)
            
            if result[1] == None:
                stats[normalized_game] = (stats[normalized_game][0], stats[normalized_game][1], stats[normalized_game][2] + 1)
                continue

            new_stats = list(stats[normalized_game])
            new_stats[normalized_game.index(result[1])] += 1
            stats[normalized_game] = tuple(new_stats)
            print(stats)


if __name__ == "__main__":
    main()