from pydantic.main import BaseModel


class MainConfig(BaseModel):
    height: int = 6
    width: int = 7
    n_rollouts: int = 300


class SelfPlayConfig(MainConfig):
    n_self_play = 1
