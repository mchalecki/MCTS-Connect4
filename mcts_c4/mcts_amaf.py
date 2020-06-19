import math
from typing import List, TypeVar

from mcts_c4.monte_carlo_tree_search import MCTS
from mcts_c4.node import Node

N = TypeVar('N', bound=Node)


class MCTS_AMAF(MCTS):
    def __init__(self, exploration_weight=1):
        super().__init__(exploration_weight, "mcts_amaf")

    def playout(self, node: N) -> None:
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward, simulated_path = self._simulate(leaf)
        self._backpropagate(path, simulated_path, reward)

    def _select(self, node: N) -> List[N]:
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)

    def _simulate(self, node: N) -> (int, List[N]):
        invert_reward = True
        simulated_path = []
        while True:
            if node.terminal:
                reward = node.reward()
                reward = 1 - reward if invert_reward else reward
                return reward, simulated_path
            node = node.make_random_move()
            simulated_path.append(node)
            invert_reward = not invert_reward

    def _backpropagate(self, path: List[N], simulated_path: List[N], reward: int) -> None:
        for node in reversed(path + simulated_path):
            if node in self.children:
                self.N[node] += 1
                self.Q[node] += reward
                reward = 1 - reward

