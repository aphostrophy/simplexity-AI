import random
import multiprocessing, copy
from time import time

from src.constant import ShapeConstant
from src.model import State, Board
from src.utility import choose_heuristic, other_shape, place, unplace

from src.ai.heuristic import heuristic;

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        print('PLAYER:',n_player + 1)

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
    depth = 1
    while(True):
      self.result = self.minimax(maximizing= True,depth= depth)
      depth+=1

  def minimax(self, maximizing: bool,depth : int):
    if(depth==0):
      return heuristic(self.state,self.n_player)

    #possible_moves[0] = col 0 primary shape, 1 = col 0 secondary shape , 2 = col 1 primary shape, 3 = col 1 secondary shape, etc...
    possible_moves = [None for _ in range(14)]

    for col in range(7):
      if(self.state.board[0,col].shape == ShapeConstant.BLANK):
        if(maximizing):
          place(self.state,self.n_player,self.state.players[self.n_player].shape,col)
          possible_moves[col*2] = self.minimax(False,depth-1)
          unplace(self.state,self.n_player,self.state.players[self.n_player].shape,col)

          place(self.state,self.n_player,other_shape(self.state.players[self.n_player].shape),col)
          possible_moves[col*2+1] = self.minimax(False,depth-1)
          unplace(self.state,self.n_player,other_shape(self.state.players[self.n_player].shape),col)
        else:
          place(self.state,(self.n_player + 1) % 2,self.state.players[(self.n_player + 1) % 2].shape,col)
          possible_moves[col*2] = self.minimax(True,depth-1)
          unplace(self.state,(self.n_player + 1) % 2,self.state.players[(self.n_player + 1) % 2].shape,col)

          place(self.state,(self.n_player + 1) % 2,other_shape(self.state.players[(self.n_player + 1) % 2].shape),col)
          possible_moves[col*2+1] = self.minimax(True,depth-1)
          unplace(self.state,(self.n_player + 1) % 2,other_shape(self.state.players[(self.n_player + 1) % 2].shape),col)
    
    choose_heuristic(possible_moves,maximizing)

    return (random.randint(0, self.state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
