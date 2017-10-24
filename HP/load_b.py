#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  load_b.py
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
# Used for Loading Boards from File
import _pickle as pickle


class load_boards:
    """
    Load game boards from a file
    """

    def __init__(self):
        """
        Class Constructor to load
        """
        self.game_boards = []


def get_game_boards(b_file):
    """
    Load Game boards from file.
    Args:
        cf (configuration) : Configuration Details
    Returns:
        game_boards[] (boards) : List of boards
    """
    # Create object for boards
    l = load_boards()
    # Load Boards
    l.game_boards = pickle.load(open(b_file, 'rb'))
    # Return all game boards
    return l.game_boards


def main():
    return 0

if __name__ == '__main__':
    main()
