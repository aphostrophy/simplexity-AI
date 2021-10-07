import random
import multiprocessing
from time import time

from src.constant import ShapeConstant
from src.model import State

from src.ai.heuristic import heuristic;

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

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

    if(p.is_alive()):
      p.terminate()

    return self.result

  def best_movement(self):
    heuristic(self.state,0)
    depth = 1
    while(True):
      current_best_movement = self.minimax(True,depth)
      self.result = current_best_movement
      depth+=1

  def minimax(self, maximizing: bool,depth : int):
    return (random.randint(0, self.state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
