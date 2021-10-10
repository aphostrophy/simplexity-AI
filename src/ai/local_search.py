import random
import multiprocessing
from time import time
from src.utility import is_win
from src.utility import choose_move, choose_heuristic, other_shape, place, unplace
from src.ai.heuristic import heuristic

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List


def sortPossibleMoves(moves_score):
    return moves_score[2][0] + moves_score[2][1]


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        lsmm = LocalSearchMinMaxing(state, n_player)

        best_movement = lsmm.result_after(thinking_time)  # minimax algorithm

        print(f'BEST MOVE PLAYER {n_player+1}', best_movement)

        return best_movement


class LocalSearchMinMaxing:
    def __init__(self, state: State, n_player: int):
        self.state = state
        self.n_player = n_player
        self.result_col = multiprocessing.Value(
            'i', random.randint(0, self.state.board.col))
        self.result_shape = multiprocessing.Value('i', 0 if random.choice(
            [ShapeConstant.CROSS, ShapeConstant.CIRCLE]) == ShapeConstant.CROSS else 1)

    def generateAllMoves(self, state: State):
        primary_shape = self.state.players[self.n_player].shape
        secondary_shape = other_shape(
            self.state.players[self.n_player].shape)

        possible_moves = []
        # Insert with primary shape first
        for col in range(7):
            if(state.board[0, col].shape == ShapeConstant.BLANK and self.state.players[self.n_player].quota[primary_shape] > 0):
                place(self.state, self.n_player, primary_shape, col)
                possible_moves.append(
                    (col, True, heuristic(self.state, self.n_player)))
                unplace(self.state, self.n_player, primary_shape, col)

        # Insert with secondary shape
        for col in range(7):
            if(state.board[0, col].shape == ShapeConstant.BLANK and self.state.players[self.n_player].quota[secondary_shape] > 0):
                place(self.state, self.n_player, secondary_shape, col)
                possible_moves.append(
                    (col, False, heuristic(self.state, self.n_player)))
                unplace(self.state, self.n_player, secondary_shape, col)

        # Sort all possible moves
        possible_moves.sort(key=sortPossibleMoves)
        return possible_moves

    def result_after(self, seconds):
        p = multiprocessing.Process(
            target=self.best_movement, name="best_movement", args=())
        p.start()

        p.join(seconds)

        if(p.is_alive()):
            p.terminate()

        return (self.result_col.value, self.state.players[self.n_player].shape if self.result_shape.value == 0 else other_shape(self.state.players[self.n_player].shape))

    def best_movement(self):
        self.depth_limit = 1
        win_found = False

        while(True and not win_found):
            (self.result_col.value, self.result_shape.value, win_found) = self.minimax(
                maximizing=True, depth=self.depth_limit, is_start=True)
            self.depth_limit += 1

    def minimax(self, maximizing: bool, depth: int, is_start: bool):
        if(depth == 0):
            return heuristic(self.state, self.n_player)

        # possible_moves[0] = col 0 primary shape, 1 = col 0 secondary shape , 2 = col 1 primary shape, 3 = col 1 secondary shape, etc...
        possible_moves = [None for _ in range(14)]

        winning_tuple = is_win(self.state.board)
        if(winning_tuple != None):
            if(winning_tuple[0] == self.state.players[self.n_player].shape):
                return (88888, 88888)
            else:
                return (-88888, -88888)

        # If depth == 1 and the first move then use initial move from local search
        if(depth == 1 and is_start):
            initial_moves = self.generateAllMoves(self.state)
            print(initial_moves)
            primary_shape = self.state.players[self.n_player].shape
            secondary_shape = other_shape(
                self.state.players[self.n_player].shape)
            for move in initial_moves:
                if(move[1]):  # primary shape
                    place(self.state, self.n_player, primary_shape, move[0])
                    possible_moves[move[0] *
                                   2] = self.minimax(False, depth-1, False)
                    unplace(self.state, self.n_player, primary_shape, move[0])
                else:
                    place(self.state, self.n_player, secondary_shape, move[0])
                    possible_moves[move[0]*2 +
                                   1] = self.minimax(False, depth-1, False)
                    unplace(self.state, self.n_player,
                            secondary_shape, move[0])

        else:  # Depth > 1 then minmaxing
            for col in range(7):
                if(self.state.board[0, col].shape == ShapeConstant.BLANK):
                    if(maximizing):
                        primary_shape = self.state.players[self.n_player].shape
                        secondary_shape = other_shape(
                            self.state.players[self.n_player].shape)

                        # Check for primary shape
                        if(self.state.players[self.n_player].quota[primary_shape] > 0):
                            place(self.state, self.n_player,
                                  primary_shape, col)
                            possible_moves[col *
                                           2] = self.minimax(False, depth-1, False)
                            unplace(self.state, self.n_player,
                                    primary_shape, col)

                        # Check for secondary shape
                        if(self.state.players[self.n_player].quota[secondary_shape] > 0):
                            place(self.state, self.n_player,
                                  secondary_shape, col)
                            possible_moves[col*2 +
                                           1] = self.minimax(False, depth-1, False)
                            unplace(self.state, self.n_player,
                                    secondary_shape, col)
                    else:
                        primary_shape = self.state.players[(
                            self.n_player + 1) % 2].shape
                        secondary_shape = other_shape(
                            self.state.players[(self.n_player + 1) % 2].shape)
                        # Check for primary shape
                        if(self.state.players[(self.n_player + 1) % 2].quota[primary_shape] > 0):
                            place(self.state, (self.n_player + 1) %
                                  2, primary_shape, col)
                            possible_moves[col *
                                           2] = self.minimax(True, depth-1, False)
                            unplace(self.state, (self.n_player + 1) %
                                    2, primary_shape, col)

                        # Check for secondary shape
                        if(self.state.players[(self.n_player + 1) % 2].quota[secondary_shape] > 0):
                            place(self.state, (self.n_player + 1) %
                                  2, secondary_shape, col)
                            possible_moves[col*2 +
                                           1] = self.minimax(True, depth-1, False)
                            unplace(self.state, (self.n_player + 1) %
                                    2, secondary_shape, col)

        if(depth == self.depth_limit):  # Pasti Maximizing
            # print(f"POSSIBLE MOVES DEPTH {depth}", possible_moves)
            return choose_move(possible_moves)

        # Standard Case
        return choose_heuristic(possible_moves, maximizing)
