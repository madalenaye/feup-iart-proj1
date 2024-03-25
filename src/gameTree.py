from typing import Iterator, List, Self
from gameState import GameState

class TreeNode:
    state: GameState
    previous: Self = None
    children: List[Self] = []

    def __init__(self, state) -> None:
        self.state = state

    def add_children(self, child: Self):
        child.previous = self
        self.children.append(child)


def get_next_moves(state: GameState) -> Iterator[GameState]:
    pass

if __name__ == '__main__':
    node = TreeNode(GameState())