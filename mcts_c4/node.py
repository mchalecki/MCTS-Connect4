from abc import abstractmethod, ABC
from typing import Set


class Node(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    @abstractmethod
    def find_children(self) -> Set['Node']:
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def make_random_move(self) -> 'Node':
        "Random successor of this board state (for more efficient simulation)"
        return None

    @property
    @abstractmethod
    def terminal(self) -> bool:
        pass

    @abstractmethod
    def reward(self) -> int:
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True
