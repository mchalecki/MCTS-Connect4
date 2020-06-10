import pickle as pkl
from pathlib import Path

from fastapi import FastAPI

from mcts_c4.connect4 import Connect4Board

app = FastAPI()

save_pkl = Path(__file__).parent / "pickles" / "1_6_7_50.pkl"
with open(save_pkl, 'rb') as f:
    tree = pkl.load(f)


@app.get("/new_game")
async def root():
    try:
        print(app.state.board.board)
    except AttributeError:
        print("Dont have board")
    board = Connect4Board.create_empty_board(6, 7)
    app.state.board = board
    return 200
