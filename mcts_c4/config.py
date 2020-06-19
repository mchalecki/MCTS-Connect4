from pathlib import Path

from pydantic.main import BaseModel


class MainConfig(BaseModel):
    height: int = 6
    width: int = 7
    n_rollouts: int = 100

    def pretty_string(self):
        return f"{self.height}_{self.width}_{self.n_rollouts}"


class SelfPlayConfig(MainConfig):
    # Exclusive
    n_self_play: int = None
    time: int = 1  # in minutes

    save_dir = Path(__file__).parent / "pickles"
    log_dir = Path(__file__).parent / "log"

    def pretty_string(self):
        if self.time:
            return '_'.join([f"{self.time}m", super().pretty_string()])
        else:
            return '_'.join([f"{self.n_self_play}p", super().pretty_string()])
