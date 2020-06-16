"""
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Luke Harold Miles, July 2019, Public Domain Dedication
See also https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""
import math
from collections import defaultdict
from typing import List, TypeVar

from mcts_c4.node import Node

N = TypeVar('N', bound=Node)


class MCTS_AMAF:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

        self.name = "mcts_amaf"

    def choose(self, node: N) -> N:
        "Choose the best successor of node. (Choose a move in the game)"
        if node.terminal:
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.make_random_move()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node: N) -> None:
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node) # znajdz lisc przechodzac z metoda UCT
        leaf = path[-1]
        self._expand(leaf) # expand = dodaj dziecko do dicta wraz z jego wszystkimi rozwinieciami
        reward, simulated_path = self._simulate(leaf)
        self._backpropagate(path, simulated_path, reward)

    def _select(self, node: N) -> List[N]:
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal (empty node children set)
                return path
            unexplored = self.children[node] - self.children.keys() # dzieci z danego stanu minus stany ktore juz byly odwiedzane(skadkolwiek)
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node: N):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def _simulate(self, node: N) -> (int, List[N]):
        "Returns the reward and travelled nodes for a random simulation (to completion) of `node`"
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
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path + simulated_path):
            if node in self.children: # update only expanded nodes, all for path, possibly not all for simulated path
                self.N[node] += 1
                self.Q[node] += reward
                reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node: N) -> N:
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)
