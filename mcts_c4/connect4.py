import pickle as pkl
from pathlib import Path

from tqdm import tqdm

from mcts_c4.config import SelfPlayConfig
from mcts_c4.connect4_board import Connect4Board
from mcts_c4.monte_carlo_tree_search import MCTS


# Has to be separate file than Connect4Board for pickle
def play_game():
    tree = MCTS()
    board = Connect4Board.create_empty_board(6, 7)
    print(board)
    while True:
        row = int(input("Enter row: "))
        board = board.make_move(row)
        print(board.board)
        if board.terminal:
            break

        for _ in range(500):
            tree.do_rollout(board)
        board: Connect4Board = tree.choose(board)
        print()
        print(board.board)
        if board.terminal:
            break
    print("Game ended:")
    print(board.board)


def self_play(config: SelfPlayConfig):
    tree = MCTS()
    for i in tqdm(range(config.n_self_play)):
        board = Connect4Board.create_empty_board(config.height, config.width)
        # print(board)
        while True:
            for _ in range(config.n_rollouts):
                tree.do_rollout(board)
            board = tree.choose(board)
            # print("\n" + board.board)
            if board.terminal:
                break
        print(f"{i} Game ended:")
        print(board.board)
    with open(config.save_dir / f'{config.pretty_string()}.pkl', "wb") as f:
        pkl.dump(tree, f)


def test_load():
    save_pkl = Path(__file__).parent / "pickles" / "height=6 width=7 n_rollouts=300 n_self_play=1.pkl"
    with open(save_pkl, 'rb') as f:
        tree = pkl.load(f)
    print(tree)


if __name__ == "__main__":
    config = SelfPlayConfig()
    self_play(config)
