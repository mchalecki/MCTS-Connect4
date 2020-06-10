from dataclasses import dataclass, field
from random import choice
from typing import Optional, Tuple, Generator, Set

import numpy as np

from mcts_c4.monte_carlo_tree_search import Node, MCTS

Pos = Tuple[int, int]  # h,w


@dataclass
class Connect4Board(Node):
    board: np.ndarray
    height: int
    width: int

    turn: bool = True
    winner: bool = None
    terminal: bool = False

    empty_field: int = field(init=False, default=5)

    def find_children(self) -> Set['Connect4Board']:
        if self.terminal:  # If the game is finished then no moves can be made
            return set()
        return {
            self.make_move(i) for i in self.avaliable_moves()
        }

    def avaliable_moves(self) -> Generator[int, None, None]:
        for i in range(0, self.width):
            if self.empty_in_arr(self.board[:, i]):
                yield i

    def make_random_move(self) -> 'Connect4Board':
        if self.terminal:
            return None  # If the game is finished then no moves can be made
        avaliable_moves = list(self.avaliable_moves())
        if not avaliable_moves:
            raise RuntimeError("Game should have ended")
        return self.make_move(choice(avaliable_moves))

    def reward(self) -> float:
        if not self.terminal:
            raise RuntimeError(f"reward called on nonterminal board {self}")
        if self.winner is self.turn:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"reward called on unreachable board {self}")
        if self.turn is (not self.winner):
            return 0  # Your opponent has just won. Bad.
        if self.winner is None:
            return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type {self.winner}")

    def make_move(self, index) -> 'Connect4Board':
        new_board = None

        performed_action = False
        for i in range(self.height - 1, -1, -1):
            if self.board[i][index] == self.empty_field:  # move is avaliable
                new_board = self.board.copy()
                new_board[i][index] = self.turn
                performed_action = True
                break
        if not performed_action:
            raise RuntimeError(f"Illegal move, tried to do {index}")

        turn = not self.turn
        winner = self.check_winners(new_board)
        is_terminal = (winner is not None) or not self.empty_in_arr(new_board)
        return Connect4Board(new_board, self.height, self.width, turn, winner, is_terminal)

    def check_winners(self, board: np.ndarray) -> Optional[bool]:  # _find_winner
        "Returns None if no winner, True if player with True turn, False if other one"
        for p1, p2, p3, p4 in self.winning_combos():
            v1, v2, v3, v4 = board[p1], board[p2], board[p3], board[p4]
            if v1 == v2 == v3 == v4 and (v1 == True or v1 == False):
                return v1

    @staticmethod
    def create_empty_board(h: int, w: int) -> 'Connect4Board':
        board = np.empty((h, w,))
        c4_board = Connect4Board(board, h, w)
        c4_board.board[:] = c4_board.empty_field
        return c4_board

    def winning_combos(self) -> Generator[Tuple[Pos, Pos, Pos, Pos], None, None]:
        # Horizontal
        for y in range(0, self.height):
            for x in range(0, self.width - 3):
                yield (y, x), (y, x + 1), (y, x + 2), (y, x + 3)
        # Vertical
        for x in range(0, self.width):
            for y in range(0, self.height - 3):
                yield (y, x), (y + 1, x), (y + 2, x), (y + 3, x)
        # Diagonal right
        for x in range(0, self.width - 3):
            for y in range(0, self.height - 3):
                yield (y, x), (y + 1, x + 1), (y + 2, x + 2), (y + 3, x + 3)
        # Diagonal left
        for x in range(self.width - 1, -1 + 3, -1):
            for y in range(0, self.height - 3):
                yield (y, x), (y + 1, x - 1), (y + 2, x - 2), (y + 3, x - 3)

    def __eq__(self, other: 'Connect4Board') -> bool:
        return (self.board == other.board).all()

    def __hash__(self):
        return hash(self.board.tostring())

    def empty_in_arr(self, arr: np.array) -> bool:
        return (arr == self.empty_field).any()


def nan_in_np_arr(arr: np.array) -> bool:
    # https://stackoverflow.com/questions/6736590/fast-check-for-nan-in-numpy
    return np.isnan(np.sum(arr))



