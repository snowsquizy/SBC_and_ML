#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  create.py
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
""" Library Imports """
import board
from random import randint


class create_boards:
    """
    Creates a list of board objects
    """

    def __init__(self):
        """
        Class Constructor.
        Args:
            none.
        Returns:
            none.
        """
        self.game_boards = []


def get_game_boards(b_number, b_dim, b_teams):
    """
    Returns the created game boards
    Args:
        b_number (int) : Number of Boards to Create.
        b_dim (int) : Side length of game Boards.
        b_teams[] : List with Team identifiers.
    Returns:
        game_boards[] (boards) : Created game boards
    """
    # Create a object for storing games
    c = create_boards()
    # Create Game boards
    for i in range(0, b_number):
        c_b = board.TicTacToe(b_dim, b_dim)
        for a in range(0, b_dim * b_dim):
            if (a % 2 == 0):
                team = b_teams[0]
            else:
                team = b_teams[1]
            position = randint(0, b_dim * b_dim - 1)
            while(c_b.check_move(position)):
                position = randint(0, b_dim * b_dim - 1)
            c_b.move(position, team)
            if (len(c_b.moves) > c_b.check_point):
                if (c_b.check_board(team)):
                    break
        # Add game to collection
        c.game_boards.append(c_b)
    # Return all boards created
    return c.game_boards


def main():

    return 0

if __name__ == '__main__':
    main()
