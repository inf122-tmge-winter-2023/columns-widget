"""
    :module_name: cli
    :module_summary: a CLI for columns_widget
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import click

from . import ColumnsBoard, ColumnsScoring, ColumnsGameState, ColumnsGameLoop, ColumnsView

from tilematch_tools import GameEngine, BoardFactory, Game


def columns_init() -> Game:
    """
        Initialize objects needed to start a game of columns
        :returns: game objects
        :rtype: Game
    """

    board = BoardFactory.create_board(ColumnsBoard, ColumnsBoard.COLUMNS_BOARD_WIDTH, ColumnsBoard.COLUMNS_BOARD_HEIGHT)
    score = ColumnsScoring()
    state = ColumnsGameState(board, score)
    return Game(state, ColumnsGameLoop, ColumnsView, 750_000_000)


@click.command()
def columns():
    """Entry point to columns"""
    ge = GameEngine([columns_init()])
    ge.run()

    
