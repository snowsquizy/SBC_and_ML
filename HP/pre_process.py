#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pre_process.py
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

# Import the timeit function
import timeit


class process_input:
    """
    Class to pre-process the Tic Tac Toe Input Data
    prior to sending it for training in the Neural Network
    """

    def __init__(
        self,
        g_b,
        b_team,
        tr_perc,
        va_perc,
            te_perc):
        """
        Class Constructor for data pre processing prior to
        sending it to the neural network for training.
        Args:
            g_b (obj)[] : Tic Tac Toe Completed Game Boards.
            teams (string)[] : Team Identifers.
            tr_perc (float) : Percentage of Boards for Training.
            va_perc (float) : Percentage of Boards for Validation.
            te_perc (float) : Percentage of Boards for Final Testing.
        Returns:
            none.
        """
        start_time = timeit.default_timer()
        x_data = []
        y_data = []
        # Training Boards
        self.x_train = []
        self.y_train = []
        # Validation Boards
        self.x_valid = []
        self.y_valid = []
        # Testing Boards
        self.x_test = []
        self.y_test = []
        # Iterate through all game boards
        for game in g_b:
            t_board = list(game.board)
            for i in range(0, len(game.board)):
                if (t_board[i] == b_team[0]):
                    t_board[i] = -1
                elif (t_board[i] == b_team[1]):
                    t_board[i] = 1
                else:
                    t_board[i] = 0
            x_data.append(t_board)
            # Update Game winner variable
            if (game.winner == b_team[0]):
                game.winner = -1
            elif (game.winner == b_team[1]):
                game.winner = 1
            else:
                game.winner = 0
            y_entry = [0]*3
            y_entry[(game.winner + 1) % 3] = 1
            y_data.append(y_entry)
        # Separate Training and Test Data
        tr_num = int(len(g_b)*tr_perc)
        va_num = int(len(g_b)*va_perc) + tr_num
        self.x_train = x_data[:tr_num]
        self.y_train = y_data[:tr_num]
        self.x_valid = x_data[tr_num:va_num]
        self.y_valid = y_data[tr_num:va_num]
        self.x_test = x_data[va_num:]
        self.y_test = y_data[va_num:]
        self.preprocessing_time = timeit.default_timer() - start_time


def main():

    return 0


if __name__ == '__main__':
    main()
