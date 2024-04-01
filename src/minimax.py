from typing import Iterator, List, Tuple
from gameState import CaptureType, GameState
from gameTree import get_next_moves
from icecream import ic

def minimax(node: GameState, depth: int, ai_player: int) -> int:
    """
    Minimax algorithm implementation.
    """


    if depth == 0:
        return node.evaluate_game_state(ai_player)

    if ai_player == node.player:
        max_eval = float('-inf')
        for next_state, _ in get_next_moves(node):
            eval_child = minimax(next_state, depth - 1, ai_player)
            max_eval = max(max_eval, eval_child)
        return max_eval
    else:
        min_eval = float('inf')
        for next_state, _ in get_next_moves(node):
            eval_child = minimax(next_state, depth - 1, ai_player)
            min_eval = min(min_eval, eval_child)
        return min_eval


def alpha_beta(node: GameState, depth: int, ai_player: int, alpha: int, beta: int) -> int:
    """
    Minimax algorithm implementation with alpha-beta pruning.
    """

    if depth == 0:
        return node.evaluate_game_state(ai_player)

    if ai_player == node.player:
        max_eval = float('-inf')
        for next_state, _ in get_next_moves(node):
            eval_child = alpha_beta(next_state, depth - 1, ai_player, alpha, beta)
            max_eval = max(max_eval, eval_child)
            alpha = max(alpha, eval_child)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for next_state, _ in get_next_moves(node):
            eval_child = alpha_beta(next_state, depth - 1, ai_player, alpha, beta)
            min_eval = min(min_eval, eval_child)
            beta = min(beta, eval_child)
            if beta <= alpha:
                break
        return min_eval
    
def alpha_beta_heuristic(node: GameState, depth: int, ai_player: int, alpha: int, beta: int) -> int:
    """
    Minimax algorithm implementation with alpha-beta pruning.
    """

    if depth == 0:
        return node.evaluate_game_state_heuristic(ai_player)

    if ai_player == node.player:
        max_eval = float('-inf')
        for next_state, _ in get_next_moves(node):
            eval_child = alpha_beta(next_state, depth - 1, ai_player, alpha, beta)
            max_eval = max(max_eval, eval_child)
            alpha = max(alpha, eval_child)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for next_state, _ in get_next_moves(node):
            eval_child = alpha_beta(next_state, depth - 1, ai_player, alpha, beta)
            min_eval = min(min_eval, eval_child)
            beta = min(beta, eval_child)
            if beta <= alpha:
                break
        return min_eval

