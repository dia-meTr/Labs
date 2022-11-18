#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Alghoritms import Algorithm


class HumanPlayer:
    def __init__(self, sign):
        self.sign = sign

    def get_move(self, board, opponent):
        while True:
            move = input()
            if self.__is_valid(move, board):
                break
            print('Please give a valid column number')

        return int(move)

    @staticmethod
    def __is_valid(move, board):
        try:
            move = int(move)
        except ValueError:
            return False

        return 0 < move <= board.width


class AIPlayer:
    def __init__(self, sign, depth):
        self.sign = sign
        self.depth = depth

    def get_move(self, board, opponent):
        n = Algorithm(board, self.depth)
        move = n.calculate_move(board, self.sign, opponent.sign)
        return move
