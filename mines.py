#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from random import randint
from time import sleep

from board import Dir
from utils import TextInput, nl, first
from mines_lib import MinesBoard, Mines, Tile
from avkutil import Term

size       = 6, 6
num_mines  = randint(4, 8)
mark_key   = 'm'
padding    = 2, 1

commands   = {
                b'a' : "left",
                b'd' : "right",
                b'w' : "up",
                b's' : "down",
                b't' : "toggle",
                b'm' : "mark",
                b'\n': "move",
                b' ' : "move",
                b'q' : "quit",
                }

class Commands:
    player = None
    commands = commands

    def __getitem__(self, cmd):
        return getattr(self, self.commands[cmd])

    def move_dir(self, dir):
        loc = board.nextloc(board.current, dir)
        self.highlight(loc)

    def down(self):
        self.move_dir(Dir(0,1))
    def up(self):
        self.move_dir(Dir(0,-1))
    def right(self):
        self.move_dir(Dir(1,0))
    def left(self):
        self.move_dir(Dir(-1,0))

    def toggle(self):
        if board.hl_visible:
            board.hl_visible = False
            board.draw()
        else:
            i = board[board.current]
            board[board.current] = '*'
            board.draw()
            board[board.current] = i
            board.hl_visible = True

    def move(self):
        loc = board.current
        board.hl_visible = False
        board.reveal(board[loc])
        return board[loc]

    def mark(self):
        loc = board.current
        board.hl_visible = False
        board[loc].toggle_mark()
        return board[loc]

    def highlight(self, loc):
        if not loc: return
        i = board[loc]
        board[loc] = '*'
        board.draw()
        board[loc] = i
        board.current = loc
        board.hl_visible = True

    def quit(self):
        sys.exit()


class BasicInterface:
    def run(self):
        # allow entering of multiple (up to 10) locations
        # pattern        = "%s? loc%s" % (mark_key, " loc?"*9)
        # self.textinput = TextInput(pattern, board, singlechar_cmds=True)
        self.term = Term()
        while True:
            board.draw()
            tile = self.get_move()
            mines.check_end(tile)

    def get_move(self):
        """Get user command and return the tile to reveal."""
        while True:
            cmd = self.term.getch()
            try:
                val = commands[cmd]()
                if val:
                    return val
            except KeyError:
                print("unknown command:", cmd)

    def make_move(self):
        "UNUSED."
        cmd  = self.textinput.getinput()
        mark = bool(first(cmd) == mark_key)
        if mark: cmd.pop(0)

        for loc in cmd:
            tile = board[loc]
            tile.toggle_mark() if mark else board.reveal(tile)
            mines.check_end(tile)


if __name__ == "__main__":
    board = MinesBoard(size, Tile, num_mines=num_mines, num_grid=False, padding=padding)
    mines = Mines(board)
    commands = Commands()
    try:
        BasicInterface().run()
    except KeyboardInterrupt:
        pass
