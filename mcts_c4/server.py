import pickle as pkl
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic.main import BaseModel

from mcts_c4.connect4 import Connect4Board

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

save_pkl = Path(__file__).parent / "pickles" / "mcts_rave_30m_6_7_100.pkl"
with open(save_pkl, 'rb') as f:
    tree = pkl.load(f)


class Game(BaseModel):
    bot_starts: bool = True


@dataclass
class GameState:
    board: List[List[int]]
    winner: Optional[int]
    legal_moves: List[int]
    terminal: bool = False
    empty_field: int = 5

    @staticmethod
    def from_board(board: Connect4Board):
        return GameState(board.board.tolist(), int(board.winner) if board.winner is not None else None,
                         list(board.avaliable_moves()), board.terminal, board.empty_field)


@app.post("/new_game/")
async def create_game(game: Game) -> GameState:
    board = Connect4Board.create_empty_board(6, 7)
    app.state.game = game
    if game.bot_starts:
        for _ in range(100):
            tree.do_rollout(board)
        board = tree.choose(board)
        print(board)
    app.state.board = board
    return GameState.from_board(board)


class Move(BaseModel):
    row: int


@app.post("/make_move/")
async def make_move(move: Move) -> GameState:
    try:
        board: Connect4Board = app.state.board
    except AttributeError:
        print("Dont have board")
        return 400
    new_board = board.make_move(move.row)
    print(new_board)
    if not new_board.terminal:
        for _ in range(100):
            tree.do_rollout(new_board)
        new_board = tree.choose(new_board)
        print(new_board)
    app.state.board = new_board
    return GameState.from_board(new_board)
