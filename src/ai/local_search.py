import random
import math
import multiprocessing
from time import time
from src.utility import is_win
from src.utility import place

from src.constant import ColorConstant, ShapeConstant
from src.model import Piece, State

from typing import Tuple


def sortPossibleMoves(moves_score):
    return moves_score[2][0] + moves_score[2][1]


class LocalSearchGroup51:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        lsmm = LocalSearchMinMaxing(state, n_player)

        best_movement = lsmm.result_after(thinking_time)  # minimax algorithm

        return best_movement


class LocalSearchMinMaxing:
    def __init__(self, state: State, n_player: int):
        self.state = state
        self.n_player = n_player
        self.result_col = multiprocessing.Value(
            'i', random.randint(0, self.state.board.col))
        self.result_shape = multiprocessing.Value('i', 0 if random.choice(
            [ShapeConstant.CROSS, ShapeConstant.CIRCLE]) == ShapeConstant.CROSS else 1)

    def other_shape(self, shape: str):
        return (ShapeConstant.CROSS if shape == ShapeConstant.CIRCLE else ShapeConstant.CIRCLE)

    def generateAllMoves(self, state: State):
        primary_shape = self.state.players[self.n_player].shape
        secondary_shape = self.other_shape(
            self.state.players[self.n_player].shape)

        possible_moves = []
        # Insert with primary shape first
        for col in range(7):
            if(state.board[0, col].shape == ShapeConstant.BLANK and self.state.players[self.n_player].quota[primary_shape] > 0):
                place(self.state, self.n_player, primary_shape, col)
                possible_moves.append(
                    (col, True, self.heuristic(self.state, self.n_player)))
                self.unplace(self.state, self.n_player, primary_shape, col)

        # Insert with secondary shape
        for col in range(7):
            if(state.board[0, col].shape == ShapeConstant.BLANK and self.state.players[self.n_player].quota[secondary_shape] > 0):
                place(self.state, self.n_player, secondary_shape, col)
                possible_moves.append(
                    (col, False, self.heuristic(self.state, self.n_player)))
                self.unplace(self.state, self.n_player, secondary_shape, col)

        # Sort all possible moves
        possible_moves.sort(reverse=True, key=sortPossibleMoves)
        return possible_moves

    def result_after(self, seconds):
        p = multiprocessing.Process(
            target=self.best_movement, name="best_movement", args=())
        p.start()

        p.join(seconds)

        if(p.is_alive()):
            p.terminate()

        return (self.result_col.value, self.state.players[self.n_player].shape if self.result_shape.value == 0 else self.other_shape(self.state.players[self.n_player].shape))

    def best_movement(self):
        self.depth_limit = 1
        win_found = False

        while(True and not win_found):
            temp = self.minimax(maximizing=True, depth=self.depth_limit,
                                alpha=-math.inf, beta=math.inf, is_start=True, alpha_tuple=None, beta_tuple=None)
            (self.result_col.value, self.result_shape.value, win_found) = temp
            self.depth_limit += 1

    def heuristic(self, state: State, player: int):
        maximizing_player = player
        minimizing_player = (player + 1) % 2

        sum_colors = 0
        sum_shapes = 0

        for col in range(7):
            for row in range(state.board.row-1, -1, -1):
                # Nanti tambahin kalau win kasih poin + INF atau - INF
                # somehow ini tidak membantu

                # winning_tuple = is_win(state.board)
                # if(winning_tuple != None):
                #   if(winning_tuple[0] == state.players[player].shape):
                #     return(88888,88888)
                #   else:
                #     return (-88888, -88888)

                if state.board[row, col].shape == ShapeConstant.BLANK:
                    if(row == 5):
                        if(col == 0):
                            sum_colors += state.board[row, col +
                                                      1].color == state.players[maximizing_player].color
                            sum_shapes += state.board[row, col +
                                                      1].shape == state.players[maximizing_player].shape

                            sum_colors -= state.board[row, col +
                                                      1].color == state.players[minimizing_player].color
                            sum_shapes -= state.board[row, col +
                                                      1].shape == state.players[minimizing_player].shape
                        elif(col == 6):
                            sum_colors += state.board[row, col -
                                                      1].color == state.players[maximizing_player].color
                            sum_shapes += state.board[row, col -
                                                      1].shape == state.players[maximizing_player].shape

                            sum_colors -= state.board[row, col -
                                                      1].color == state.players[minimizing_player].color
                            sum_shapes -= state.board[row, col -
                                                      1].shape == state.players[minimizing_player].shape
                        else:
                            sum_colors += state.board[row, col +
                                                      1].color == state.players[maximizing_player].color
                            sum_shapes += state.board[row, col +
                                                      1].shape == state.players[maximizing_player].shape
                            sum_colors += state.board[row, col -
                                                      1].color == state.players[maximizing_player].color
                            sum_shapes += state.board[row, col -
                                                      1].shape == state.players[maximizing_player].shape

                            sum_colors -= state.board[row, col +
                                                      1].color == state.players[minimizing_player].color
                            sum_shapes -= state.board[row, col +
                                                      1].shape == state.players[minimizing_player].shape
                            sum_colors -= state.board[row, col -
                                                      1].color == state.players[minimizing_player].color
                            sum_shapes -= state.board[row, col -
                                                      1].shape == state.players[minimizing_player].shape
                    else:
                        sum_colors += state.board[row+1,
                                                  col].color == state.players[maximizing_player].color
                        sum_shapes += state.board[row+1,
                                                  col].shape == state.players[maximizing_player].shape

                        sum_colors -= state.board[row+1,
                                                  col].color == state.players[minimizing_player].color
                        sum_shapes -= state.board[row+1,
                                                  col].shape == state.players[minimizing_player].shape
                        if(col == 0):
                            sum_colors += state.board[row, col +
                                                      1].color == state.players[maximizing_player].color
                            sum_shapes += state.board[row, col +
                                                      1].shape == state.players[maximizing_player].shape

                            sum_colors -= state.board[row, col +
                                                      1].color == state.players[minimizing_player].color
                            sum_shapes -= state.board[row, col +
                                                      1].shape == state.players[minimizing_player].shape
                        elif(col == 6):
                            sum_colors += state.board[row, col -
                                                      1].color == state.players[maximizing_player].color
                            sum_shapes += state.board[row, col -
                                                      1].shape == state.players[maximizing_player].shape

                            sum_colors -= state.board[row, col -
                                                      1].color == state.players[minimizing_player].color
                            sum_shapes -= state.board[row, col -
                                                      1].shape == state.players[minimizing_player].shape
                        else:
                            sum_colors += state.board[row, col +
                                                      1].color == state.players[maximizing_player].color
                            sum_shapes += state.board[row, col +
                                                      1].shape == state.players[maximizing_player].shape
                            sum_colors += state.board[row, col -
                                                      1].color == state.players[maximizing_player].color
                            sum_shapes += state.board[row, col -
                                                      1].shape == state.players[maximizing_player].shape

                            sum_colors -= state.board[row, col +
                                                      1].color == state.players[minimizing_player].color
                            sum_shapes -= state.board[row, col +
                                                      1].shape == state.players[minimizing_player].shape
                            sum_colors -= state.board[row, col -
                                                      1].color == state.players[minimizing_player].color
                            sum_shapes -= state.board[row, col -
                                                      1].shape == state.players[minimizing_player].shape
                    break
        return (sum_colors, sum_shapes)

    def choose_move(self, possible_moves: list):  # Maximizing move
        max_tuple = (-math.inf, 0)
        col = -1
        for idx, tuple in enumerate(possible_moves):
            if(tuple != None):
                tuple_sum = tuple[0] + tuple[1]
                if(tuple_sum > max_tuple[0] + max_tuple[1]):
                    max_tuple = tuple
                    col = idx
                elif(tuple_sum == max_tuple[0] + max_tuple[1]):
                    if(tuple[1] > max_tuple[1]):  # Tie Breaker Shape
                        max_tuple = tuple
                        col = idx
        return (col//2, col % 2, max_tuple[0] == 88888)

    def choose_heuristic(self, possible_moves: list, maximizing: bool) -> Tuple:
        if(maximizing):
            max_tuple = (-math.inf, -math.inf)
            oldIndex = math.inf
            for idx,tuple in enumerate(possible_moves):
                if(tuple != None):
                    tuple_sum = tuple[0] + tuple[1]
                    if(tuple_sum > max_tuple[0] + max_tuple[1]):
                        max_tuple = tuple
                        oldIndex = idx
                    elif(tuple_sum == max_tuple[0] + max_tuple[1]):
                        if(tuple[1] > max_tuple[1]):  # Tie Breaker Shape
                          max_tuple = tuple
                          oldIndex = idx
                        elif(tuple[1] == max_tuple[1]):
                          if(abs(7-idx)<abs(7-oldIndex)):
                            max_tuple = tuple
            return max_tuple
        else:
            min_tuple = (math.inf, math.inf)
            oldIndex = math.inf
            for idx,tuple in enumerate(possible_moves):
                if(tuple != None):
                    tuple_sum = tuple[0] + tuple[1]
                    if(tuple_sum < min_tuple[0] + min_tuple[1]):
                        min_tuple = tuple
                        oldIndex = idx
                    elif(tuple_sum == min_tuple[0] + min_tuple[1]):
                        if(tuple[1] < min_tuple[1]):  # Tie Breaker Shape
                            min_tuple = tuple
                            oldIndex = idx
                        elif(tuple[1] == min_tuple[1]):
                          if(abs(7-idx)<abs(7-oldIndex)):
                            min_tuple = tuple
                            oldIndex = idx
            return min_tuple

    def unplace(self, state: State, n_player: int, shape: str, col: str) -> int:

        for row in range(state.board.row):
            if state.board[row, col].shape != ShapeConstant.BLANK:
                piece = Piece(ShapeConstant.BLANK, ColorConstant.BLACK)
                state.board.set_piece(row, col, piece)
                state.players[n_player].quota[shape] += 1
                return row

        return -1

    def minimax(self, maximizing: bool, depth: int, alpha, beta, is_start: bool, alpha_tuple : tuple, beta_tuple : tuple):
        winning_tuple = is_win(self.state.board)
        
        if(winning_tuple != None):
            if(winning_tuple[0] == self.state.players[self.n_player].shape):
                return (88888, 88888)
            else:
                return (-88888, -88888)

        if(depth == 0):
            return self.heuristic(self.state, self.n_player)

        # possible_moves[0] = col 0 primary shape, 1 = col 0 secondary shape , 2 = col 1 primary shape, 3 = col 1 secondary shape, etc...
        possible_moves = [None for _ in range(14)]

        # If depth == 1 and the first move then use initial move from local search
        if(depth == 1 and is_start):
            initial_moves = self.generateAllMoves(self.state)
            primary_shape = self.state.players[self.n_player].shape
            secondary_shape = self.other_shape(
                self.state.players[self.n_player].shape)
            for move in initial_moves:
                if(move[1]):  # primary shape
                    place(self.state, self.n_player,primary_shape, move[0])

                    temp = self.minimax(False, depth-1, alpha=alpha, beta=beta, is_start=False, alpha_tuple=alpha_tuple, beta_tuple=beta_tuple)
                    score = temp[0] + temp[1]

                    alpha = max(alpha, score)
                    possible_moves[move[0]*2] = temp

                    self.unplace(self.state, self.n_player,primary_shape, move[0])

                    if(beta <= alpha):
                        return (beta_tuple[0]+1,beta_tuple[1]+1)

                else:
                    place(self.state, self.n_player, secondary_shape, move[0])

                    temp = self.minimax(False, depth-1, alpha=alpha, beta=beta, is_start=False, alpha_tuple=alpha_tuple, beta_tuple=beta_tuple)
                    score = temp[0] + temp[1]

                    alpha = max(alpha, score)
                    possible_moves[move[0]*2+1] = temp

                    self.unplace(self.state, self.n_player,secondary_shape, move[0])

                    if(beta <= alpha):
                        return (beta_tuple[0]+1,beta_tuple[1]+1)

        else:  # Depth > 1 then minmaxing
            for col in range(7):
                if(self.state.board[0, col].shape == ShapeConstant.BLANK):
                    if(maximizing):
                        primary_shape = self.state.players[self.n_player].shape
                        primary_quota = self.state.players[self.n_player].quota[primary_shape]
                        secondary_shape = self.other_shape(self.state.players[self.n_player].shape)
                        secondary_quota = self.state.players[self.n_player].quota[secondary_shape]

                       # Check for primary shape
                        if(primary_quota > 0):
                            place(self.state, self.n_player,primary_shape, col)
                            
                            temp = self.minimax(False, depth-1, alpha=alpha, beta=beta, is_start=False, alpha_tuple=alpha_tuple, beta_tuple=beta_tuple)
                            score = temp[0] + temp[1]

                            alpha = max(alpha, score)
                            alpha_tuple = (temp[0],temp[1])

                            possible_moves[col*2] = temp
                            self.unplace(self.state, self.n_player,primary_shape, col)

                            if(beta <= alpha):
                                return (beta_tuple[0]+1,beta_tuple[1]+1)

                        # Check for secondary shape
                        if(secondary_quota > 0):
                            place(self.state, self.n_player,secondary_shape, col)
                            
                            temp = self.minimax(False, depth-1, alpha=alpha, beta=beta, is_start=False, alpha_tuple=alpha_tuple, beta_tuple=beta_tuple)
                            score = temp[0] + temp[1]

                            alpha = max(alpha, score)
                            alpha_tuple = (temp[0],temp[1])
                            possible_moves[col*2+1] = temp
                            self.unplace(self.state, self.n_player,secondary_shape, col)

                            if(beta <= alpha):
                                return (beta_tuple[0]+1,beta_tuple[1]+1)
                    else:
                        primary_shape = self.state.players[(self.n_player + 1) % 2].shape
                        primary_quota = self.state.players[(self.n_player + 1) % 2].quota[primary_shape]
                        secondary_shape = self.other_shape(self.state.players[(self.n_player + 1) % 2].shape)
                        secondary_quota = self.state.players[(self.n_player + 1) % 2].quota[secondary_shape]
                        # Check for primary shape
                        if(primary_quota > 0):
                            place(self.state, (self.n_player + 1) %2, primary_shape, col)
                            
                            temp = self.minimax(True, depth-1, alpha=alpha, beta=beta, is_start=False, alpha_tuple=alpha_tuple, beta_tuple=beta_tuple)
                            score = temp[0] + temp[1]

                            beta = min(beta, score)
                            beta_tuple = (temp[0],temp[1])

                            possible_moves[col*2] = temp
                            self.unplace(self.state, (self.n_player + 1) %2, primary_shape, col)

                            if(beta <= alpha):
                                return (alpha_tuple[0]-1,alpha_tuple[1]-1)

                        # Check for secondary shape
                        if(secondary_quota > 0):
                            place(self.state, (self.n_player + 1) %2, secondary_shape, col)
                            
                            temp = self.minimax(True, depth-1, alpha=alpha, beta=beta, is_start=False, alpha_tuple=alpha_tuple, beta_tuple=beta_tuple)
                            score = temp[0] + temp[1]

                            beta = min(beta, score)
                            beta_tuple = (temp[0],temp[1])

                            possible_moves[col*2+1] = temp
                            self.unplace(self.state, (self.n_player + 1) %2, secondary_shape, col)

                            if(beta <= alpha):
                                return (alpha_tuple[0]-1,alpha_tuple[1]-1)

        if(depth == self.depth_limit):  # Pasti Maximizing
            return self.choose_move(possible_moves)

        # Standard Case
        return self.choose_heuristic(possible_moves, maximizing)
