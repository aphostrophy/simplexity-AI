import random
import multiprocessing, copy
from time import time

from src.constant import ShapeConstant
from src.model import State, Board
from src.utility import choose_heuristic, choose_move, other_shape, place, unplace

from src.ai.heuristic import heuristic;

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        pdm = ProgressiveDeepeningMinimax(state,n_player)

        best_movement = pdm.result_after(thinking_time)

        print(f'BEST MOVE PLAYER {n_player+1}',best_movement)

        return best_movement


class ProgressiveDeepeningMinimax:
  def __init__(self, state: State, n_player: int):
    self.state = state
    self.n_player = n_player
    self.result_col = multiprocessing.Value('i',0)
    self.result_shape = multiprocessing.Value('i',0)

  def result_after(self,seconds):
    p = multiprocessing.Process(target=self.best_movement, name="best_movement", args=())
    p.start()

    p.join(seconds)

    if(p.is_alive()):
      p.terminate()

    return (self.result_col.value, self.state.players[self.n_player].shape if self.result_shape.value==0 else other_shape(self.state.players[self.n_player].shape))

  def best_movement(self):
    self.result_col = random.randint(0, self.state.board.col)
    self.result_shape = random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])
    self.depth_limit = 1
    win_found = False
    while(True and not win_found):
      (self.result_col.value,self.result_shape.value, win_found) = self.minimax(maximizing= True,depth= self.depth_limit)
      self.depth_limit+=1

  def minimax(self, maximizing: bool,depth : int):
    if(depth==0):
      return heuristic(self.state,self.n_player)

    #possible_moves[0] = col 0 primary shape, 1 = col 0 secondary shape , 2 = col 1 primary shape, 3 = col 1 secondary shape, etc...
    possible_moves = [None for _ in range(14)]

    for col in range(7):
      if(self.state.board[0,col].shape == ShapeConstant.BLANK):
        if(maximizing):
          primary_shape = self.state.players[self.n_player].shape
          secondary_shape = other_shape(self.state.players[self.n_player].shape)

          #Check for primary shape
          if(self.state.players[self.n_player].quota[primary_shape]>0):
            place(self.state,self.n_player,primary_shape,col)
            possible_moves[col*2] = self.minimax(False,depth-1)
            unplace(self.state,self.n_player,primary_shape,col)

          #Check for secondary shape
          if(self.state.players[self.n_player].quota[secondary_shape]>0):
            place(self.state,self.n_player,secondary_shape,col)
            possible_moves[col*2+1] = self.minimax(False,depth-1)
            unplace(self.state,self.n_player,secondary_shape,col)
        else:
          primary_shape = self.state.players[(self.n_player + 1) % 2].shape
          secondary_shape = other_shape(self.state.players[(self.n_player + 1) % 2].shape)
          #Check for primary shape
          if(self.state.players[(self.n_player + 1) % 2].quota[primary_shape]>0):
            place(self.state,(self.n_player + 1) % 2,primary_shape,col)
            possible_moves[col*2] = self.minimax(True,depth-1)
            unplace(self.state,(self.n_player + 1) % 2,primary_shape,col)

          #Check for secondary shape
          if(self.state.players[(self.n_player + 1) % 2].quota[secondary_shape]>0):
            place(self.state,(self.n_player + 1) % 2,secondary_shape,col)
            possible_moves[col*2+1] = self.minimax(True,depth-1)
            unplace(self.state,(self.n_player + 1) % 2,secondary_shape,col)

    if(depth == self.depth_limit): #Pasti Maximizing
      print(f"POSSIBLE MOVES DEPTH {depth}",possible_moves)
      return choose_move(possible_moves)
      
    #Standard Case
    return choose_heuristic(possible_moves,maximizing)
