import math
from collections import defaultdict
from typing import List, TypeVar

from mcts_c4.mcts_base import MCTS_base
from mcts_c4.node import Node

N = TypeVar('N', bound=Node)


class MCTS(MCTS_base):
    def __init__(self, exploration_weight=1, name="mcts"):
        super().__init__(exploration_weight, name)
        self.Q = defaultdict(int)
        self.N = defaultdict(int)
        self.children = dict()

    def choose(self, node: N) -> N:
        if node.terminal:
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.make_random_move()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")
            return self.Q[n] / self.N[n]

        return max(self.children[node], key=score)

    def playout(self, node: N) -> None:
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

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

    def _expand(self, node: N):
        if node in self.children:
            return
        self.children[node] = node.find_children()

    def _simulate(self, node: N) -> int:
        invert_reward = True
        while True:
            if node.terminal:
                reward = node.reward()
                reward = 1 - reward if invert_reward else reward
                return reward
            node = node.make_random_move()
            invert_reward = not invert_reward

    def _backpropagate(self, path: List[N], reward: int) -> None:
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward

    def _uct_select(self, node: N) -> N:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)
