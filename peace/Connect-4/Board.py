#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from termcolor import colored
    colored_imported = True
except ImportError:
    colored_imported = False


class Board:
    """Gam  e board for Connect 4"""
    def __init__(self, width=7, height=6):
        self.width = width
        self.height = height
        self.board = self.__build_board(width, height)
        self.undo_stack = []
        self.segment_indexes = self.__segment_indexes()
        self.__segment_indexes_by_index = self.__segment_indexes_by_index()

    def __build_board(self, width, height):
        return [[' ' for x in range(width)] for y in range(height)]

    def try_place_piece(self, move, curr_sign):
        """Tries to put piece to board. Returns True if move is possible and row the piece was put"""
        for i in range(len(self.board)):
            row = self.height - i - 1   # Pieces are added from bottom to up
            if self.board[row][move-1] == ' ':
                self.board[row][move-1] = curr_sign
                self.undo_stack.append(move - 1)
                return True, row

        # print 'Not allowed'
        return False, None

    def undo(self):
        try:
            value = self.undo_stack.pop()
        except IndexError:
            print('Nothing to undo')
            return False
        for row in self.board:
            if not row[value] == ' ':
                row[value] = ' '
                return value

    def is_game_over(self, board, curr_sign, opponent_sign, move=None):
        if move:
            # Check if specific move causes game over (specific case)
            col, row = move
            for indexes in self.__segment_indexes_by_index[row * 7 + col]:
                # indexes contains four board indexes as tuples
                segment = ''.join([board[index[0]][index[1]] for index in indexes])

                if segment == 4 * curr_sign:
                    return True, curr_sign
                elif segment == 4 * opponent_sign:
                    return True, opponent_sign
        else:
            # Check if game is over (general case)
            for indexes in self.segment_indexes:
                # indexes contains four board indexes as tuples
                segment = ''.join([self.board[index[0]][index[1]] for index in indexes])

                if segment == 4 * curr_sign:
                    return True, curr_sign
                elif segment == 4 * opponent_sign:
                    return True, opponent_sign

        if not self.__is_legal_moves_left():
            # If tie game, no winner is returned
            return True, None

        # If game is not over, no winner is returned
        return False, None

    def __segment_indexes(self):

        # Get indexes from rows, columns and diagonal lines and combine them to segments
        rows = [[(y, x) for x in range(self.width)] for y in range(self.height)]
        columns = [[(x, y) for x in range(self.height)] for y in range(self.width)]

        up = [[(x, y) for x in range(self.height) for y in range(self.width)
               if x + y == z] for z in range(3, 9)]
        down = [[(x, y) for x in range(self.height) for y in range(self.width)
                 if x - y == z] for z in range(-3, 3)]

        segments = rows + columns + up + down

        # Split segments to smaller, 4 length pieces
        # These are every possible chain of four in the game
        # Each element in returned list is a list of indexes (which are tuples)

        return [segments[x][i:i+4] for x in range(len(segments)) for i in range(len(segments[x])-3)]

    def __segment_indexes_by_index(self):
        segment_indexes_by_index = [[] for x in range(self.width * self.height)]
        for col in range(self.width):
            for row in range(self.height):
                for index in self.segment_indexes:
                    if (col, row) in index:
                        segment_indexes_by_index[col*7 + row].append(index)

        return segment_indexes_by_index

    def __is_legal_moves_left(self, board=None):
        if board is None:
            board = self.board
        return ' ' in [board[0][x] for x in range(self.width)]

    def __str__(self):
        numbers = [str(x) for x in range(1, self.width + 1)]
        if colored_imported:
            print(colored(' ' + ' '.join(numbers), 'cyan'))
        else:
            print(' ' + ' '.join(numbers))

        s = ''
        for row in self.board:
            if colored_imported:
                s += colored('|', 'red') + colored('|', 'red').join(row) + colored('|\n', 'red')
            else:
                s += '|' + '|'.join(row) + '|\n'

        return s

    def __hash__(self):
        tmp = str(self.board)
        return hash(tmp)

