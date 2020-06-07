from mcts_c4.connect4 import Connect4Board


def test_winning_combos_1():
    board = Connect4Board.create_empty_board(4, 4)
    combos = list(board.winning_combos())
    assert combos == [((0, 0), (0, 1), (0, 2), (0, 3)), ((1, 0), (1, 1), (1, 2), (1, 3)),
                      ((2, 0), (2, 1), (2, 2), (2, 3)), ((3, 0), (3, 1), (3, 2), (3, 3)),
                      ((0, 0), (1, 0), (2, 0), (3, 0)), ((0, 1), (1, 1), (2, 1), (3, 1)),
                      ((0, 2), (1, 2), (2, 2), (3, 2)), ((0, 3), (1, 3), (2, 3), (3, 3)),
                      ((0, 0), (1, 1), (2, 2), (3, 3)), ((0, 3), (1, 2), (2, 1), (3, 0))]
