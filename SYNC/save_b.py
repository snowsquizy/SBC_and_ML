#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  save_b.py
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
# Used for saving boards to a file
import pickle


class save_boards:
    """
    Saving Game boards for use later
    """

    def __init__(self, game_boards, b_file):
        """
        Saving Boards constructor.
        Args:
            game_boards[] (boards) : Current game boards for saving.
            b_file (str) : Filename for saving boards too.
        Returns:
        none.
        """
        # Save game boards
        pickle.dump(game_boards, open(b_file, 'wb'))


def main():

    return 0

if __name__ == '__main__':
    main()
