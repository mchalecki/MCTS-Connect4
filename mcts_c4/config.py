from pathlib import Path

from pydantic.main import BaseModel


class MainConfig(BaseModel):
    height: int = 6
    width: int = 7
    n_rollouts: int = 50

    def pretty_string(self):
        return f"{self.height}_{self.width}_{self.n_rollouts}"


class SelfPlayConfig(MainConfig):
    n_self_play = 1
    save_dir = Path(__file__).parent / "pickles"

    def pretty_string(self):
        return '_'.join([f"{self.n_self_play}", super().pretty_string()])
