#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Board import Board
from Players import HumanPlayer, AIPlayer


def play():
    board = Board()
    player1 = HumanPlayer('X')
    player2 = AIPlayer('O', 6)

    print("Let's play connect four!\nTo place a move, type a number [1-7]")

    current_player = player1
    other_player = player2

    winner = None
    game_over = False

    while not game_over:
        print(board)

        move_allowed = False
        while not move_allowed:
            move = current_player.get_move(board, other_player)
            move_allowed = board.try_place_piece(move, current_player.sign)

        game_over, winner = board.is_game_over(board.board, current_player.sign,
                                               other_player.sign)
        current_player, other_player = other_player, current_player

    print(board)
    if winner:
        print("Computer ", 'won!\nGame over')
    else:
        print('Tie game!')

    ans = input('Do you want to play again? y/n\n')

    if ans.lower() == 'y':
        play()


play()
