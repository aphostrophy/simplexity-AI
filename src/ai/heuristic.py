from src.model.state import State
from src.constant import ShapeConstant, GameConstant
from src.utility import is_win
import math

#Player 0 : RED O (Only have red pieces)
#Player 1 : BLUE X (Only have blue pieces)
#Utamakan shape

def heuristic(state:State, player: int):
  maximizing_player = player
  minimizing_player = (player + 1) %2

  sum_colors = 0
  sum_shapes = 0

  winning_tuple = is_win(state.board)
  if(winning_tuple != None):
    if(winning_tuple[0] == state.players[maximizing_player].shape):
      return (math.inf,math.inf)
    else:
      return (-math.inf,math.inf)

  for col in range(7):
    for row in range(state.board.row-1,-1,-1):
      #Nanti tambahin kalau win kasih poin + INF atau - INF
      if state.board[row, col].shape == ShapeConstant.BLANK:
        if(row==5):
          if(col==0):
              sum_colors += state.board[row,col+1].color == state.players[maximizing_player].color
              sum_shapes += state.board[row,col+1].shape == state.players[maximizing_player].shape

              sum_colors -= state.board[row,col+1].color == state.players[minimizing_player].color
              sum_shapes -= state.board[row,col+1].shape == state.players[minimizing_player].shape
          elif(col==6):
              sum_colors += state.board[row,col-1].color == state.players[maximizing_player].color
              sum_shapes += state.board[row,col-1].shape == state.players[maximizing_player].shape

              sum_colors -= state.board[row,col-1].color == state.players[minimizing_player].color
              sum_shapes -= state.board[row,col-1].shape == state.players[minimizing_player].shape
          else:
              sum_colors += state.board[row,col+1].color == state.players[maximizing_player].color
              sum_shapes += state.board[row,col+1].shape == state.players[maximizing_player].shape
              sum_colors += state.board[row,col-1].color == state.players[maximizing_player].color
              sum_shapes += state.board[row,col-1].shape == state.players[maximizing_player].shape

              sum_colors -= state.board[row,col+1].color == state.players[minimizing_player].color
              sum_shapes -= state.board[row,col+1].shape == state.players[minimizing_player].shape
              sum_colors -= state.board[row,col-1].color == state.players[minimizing_player].color
              sum_shapes -= state.board[row,col-1].shape == state.players[minimizing_player].shape
        else:
          sum_colors += state.board[row+1,col].color == state.players[maximizing_player].color
          sum_shapes += state.board[row+1,col].shape == state.players[maximizing_player].shape

          sum_colors -= state.board[row+1,col].color == state.players[minimizing_player].color
          sum_shapes -= state.board[row+1,col].shape == state.players[minimizing_player].shape
          if(col==0):
              sum_colors += state.board[row,col+1].color == state.players[maximizing_player].color
              sum_shapes += state.board[row,col+1].shape == state.players[maximizing_player].shape

              sum_colors -= state.board[row,col+1].color == state.players[minimizing_player].color
              sum_shapes -= state.board[row,col+1].shape == state.players[minimizing_player].shape
          elif(col==6):
              sum_colors += state.board[row,col-1].color == state.players[maximizing_player].color
              sum_shapes += state.board[row,col-1].shape == state.players[maximizing_player].shape

              sum_colors -= state.board[row,col-1].color == state.players[minimizing_player].color
              sum_shapes -= state.board[row,col-1].shape == state.players[minimizing_player].shape
          else:
              sum_colors += state.board[row,col+1].color == state.players[maximizing_player].color
              sum_shapes += state.board[row,col+1].shape == state.players[maximizing_player].shape
              sum_colors += state.board[row,col-1].color == state.players[maximizing_player].color
              sum_shapes += state.board[row,col-1].shape == state.players[maximizing_player].shape

              sum_colors -= state.board[row,col+1].color == state.players[minimizing_player].color
              sum_shapes -= state.board[row,col+1].shape == state.players[minimizing_player].shape
              sum_colors -= state.board[row,col-1].color == state.players[minimizing_player].color
              sum_shapes -= state.board[row,col-1].shape == state.players[minimizing_player].shape
        break
  return (sum_colors,sum_shapes)