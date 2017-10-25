#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  board.py
#
#  Board Module
#
#  Copyright 2017 Andrew Taylor <andrew@snowsquizy.id.au>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
""" Libraries """
# Required for Unit Tests.
from random import randint
from random import seed

"""Variables used for test_function """
# Team 1 = 1.0
t_1 = 1
# Team 2 = -1.0
t_2 = -1
# Total Tests to run. Maximum allowable == 10
total_tests = 10
# Test the board position Middle Left
middle_left = 3
# Middle Left board Values
test_ml = [-1, 0, -1, 1, 1, -1, -1, 1, 1, 1]
# Game Winners
test_winner = [-1, 1, -1, -1, 0, -1, 1, -1, -1, 0]
# Total Number of Game Moves taken
test_moves = [9, 6, 7, 9, 9, 7, 8, 7, 9, 9]


class TicTacToe:
    """
    Square Board Object
    """

    def __init__(self, dim_x, dim_y):
        """
        Constructor that creates a board of dim_x * dim_y for playing
        connect the dots.  The minimum number of positions in a row
        allowed is equal to the length of dim_x.
        Args:
            dim_x (int) : X direction length for the board
            dim_y (int) : Y direction length for the board
        """
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_total = self.dim_x * self.dim_y
        self.board = [0]*self.dim_total
        self.finished = False
        self.check_point = dim_x + dim_y - 1
        self.check_length = self.dim_x * 2 + 2
        self.winner = 0
        self.moves = []
        self.checks = []
        self.create_checks()

    def create_checks(self):
        """
        Creates the 8 check locations to determine a winner
        """
        for i in range(0, self.dim_x):
            add = i
            multi = i
            temp1 = []
            temp2 = []
            for j in range(0, self.dim_y):
                temp1.append(j * self.dim_y + add)
                temp2.append(multi * self.dim_y + j)
            self.checks.append(temp1)
            self.checks.append(temp2)
        temp3 = []
        temp4 = []
        for k in range(0, self.dim_x):
            temp3.append(k * self.dim_x + k)
            temp4.append(k * self.dim_x + (self.dim_x - k - 1))
        self.checks.append(temp3)
        self.checks.append(temp4)

    def game_board(self):
        """
        Prints the board with current moves applied.
        """
        print('Board State')
        for i in range(0, self.dim_x):
            print(self.board[i*self.dim_x:(i+1)*self.dim_x])

    def game_moves(self):
        """
        Prints number of moves taken for current game.
        """
        print('Number of Moves: ' + str(len(self.moves)))

    def game_move_number(self):
        """
        Returns the number of moves taken in the game.
        Args:
            none
        Returns:
            len(self.moves) (int) : Total number of moves taken in game
                                    so far
        """
        return len(self.moves)

    def game_finished(self):
        ''' Prints if game is completed T/F '''
        if (self.finished):
            print('* Game Finished *')
        else:
            print('** Game Ongoing *')

    def game_move_order(self):
        ''' Prints the order of the moves for the game '''
        print(self.moves)

    def game_winner(self):
        ''' Prints the game winner '''
        print('Game Winner    : ' + str(self.winner))

    def game_details(self):
        ''' Prints full Game Details including the following
        board details
        game finished
        game winner
        number of moves taken '''
        self.game_board()
        self.game_finished()
        self.game_winner()
        self.game_moves()
        self.game_move_order()
        print('**********************')

    def check_move(self, position):
        ''' Checks if supplied x,y position is available
        Returns 'true' value if move not available '''
        if (self.board[position] != 0):
            return 1
        else:
            return 0

    def check_board(self, team):
        """
        Checks to see if there is a winner of the game by interogating
        the board vs the checks attribute
        Args:
            none
        Returns:
            True if game is won
            False if game is continuing
        """
        for a in range(0, len(self.checks)):
            checker = self.checks[a]
            won = []
            for b in range(0, self.dim_x):
                if (self.board[checker[b]] == team):
                    won.append(True)
                else:
                    won.append(False)
            if (won.count(True) == self.dim_x):
                self.finished = True
                self.winner = team
                return 1
        return 0

    def move(self, position, team):
        ''' Adds a team marker to a spot on the board
        at the provided position '''
        self.board[position] = team
        self.moves.append(position)
        if (self.dim_total == len(self.moves)):
            self.finished = True
        return 0


def test_function():
    ''' Test Case to Test all methods '''
    # empty list for created games
    tb = []
    # Set Random Seed to ensure created games are the same
    seed(1000)
    # Number of Testing games to create
    for a in range(0, total_tests):
        tb.append(TicTacToe(3, 3))
        # Tests the default Atributes of each game
        assert tb[a].finished is False
        assert len(tb[a].moves) == 0
        assert tb[a].winner == 0
        assert tb[a].dim_x == 3
        assert tb[a].dim_x == 3
        assert tb[a].dim_total == tb[a].dim_x * tb[a].dim_y
        assert len(set(tb[a].board)) == 1
        assert len(tb[a].checks) == tb[a].check_length
        assert tb[a].check_point == 5
        # Create a Random Game
        for b in range(0, tb[a].dim_total):
            if (b % 2 == 0):
                team = t_1
            else:
                team = t_2
            position = randint(0, tb[a].dim_total-1)
            while(tb[a].check_move(position)):
                position = randint(0, tb[a].dim_total-1)
            tb[a].move(position, team)
            if (len(tb[a].moves) > tb[a].check_point):
                if (tb[a].check_board(team)):
                    break
        # Display the Game Details
        tb[a].game_details()
        # Test the results against the Unit Test Variables
        assert tb[a].board[middle_left] == test_ml[a]
        assert tb[a].winner == test_winner[a]
        assert len(tb[a].moves) == test_moves[a]


if __name__ == '__main__':
    ''' Test the module with total_test of tic tac toe games '''
    test_function()
