from mcts_c4.connect4 import Connect4Board


def test_winning_combos_1():
    board = Connect4Board.create_empty_board(4, 4)
    combos = list(board.winning_combos())
    assert combos == [((0, 0), (0, 1), (0, 2), (0, 3)), ((1, 0), (1, 1), (1, 2), (1, 3)),
                      ((2, 0), (2, 1), (2, 2), (2, 3)), ((3, 0), (3, 1), (3, 2), (3, 3)),
                      ((0, 0), (1, 0), (2, 0), (3, 0)), ((0, 1), (1, 1), (2, 1), (3, 1)),
                      ((0, 2), (1, 2), (2, 2), (3, 2)), ((0, 3), (1, 3), (2, 3), (3, 3)),
                      ((0, 0), (1, 1), (2, 2), (3, 3)), ((0, 3), (1, 2), (2, 1), (3, 0))]
    assert len(combos) == 10


def test_winning_combos_2():
    board = Connect4Board.create_empty_board(5, 5)
    combos = list(board.winning_combos())
    assert len(combos) == 28


def test_moves_1():
    board = Connect4Board.create_empty_board(4, 4)
    moves = list(board.avaliable_moves())
    assert len(moves) == 4
    new_board = board.make_move(0)
    assert new_board.board[3, 0] == 1
