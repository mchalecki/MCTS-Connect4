from abc import ABC, abstractmethod
from typing import TypeVar

from mcts_c4.node import Node

N = TypeVar('N', bound=Node)


class MCTS_base(ABC):

    @abstractmethod
    def __init__(self, exploration_weight: float, name: str):
        self.exploration_weight = exploration_weight
        self.name = name

    @abstractmethod
    def choose(self, node: N) -> N:
        pass

    @abstractmethod
    def playout(self, node: N) -> None:
        pass
