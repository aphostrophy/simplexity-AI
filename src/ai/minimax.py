import random
import multiprocessing
from time import time

from src.constant import ShapeConstant
from src.model import State

from src.ai.heuristic import Heuristic;

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        pdm = ProgressiveDeepeningMinimax(state,n_player)

        best_movement = pdm.result_after(thinking_time)

        return best_movement


class ProgressiveDeepeningMinimax:
  def __init__(self, state: State, n_player: int):
    self.state = state
    self.n_player = n_player
    self.result = (random.randint(0, self.state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

  def result_after(self,seconds):
    p = multiprocessing.Process(target=self.best_movement, name="best_movement", args=())
    p.start()

    p.join(seconds)

    return self.result

  def infinite_while(self):
    i = True
    while(True):
      i != i

  def best_movement(self):
    current_best_movement = (random.randint(0, self.state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
    self.result = current_best_movement
