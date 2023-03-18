"""
    :module_name: cli
    :module_summary: a CLI for columns_widget
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import click

from . import ColumnsGameState, ColumnsView, ColumnsGameLoop, ColumnsBoard, ColumnsScoring

from tilematch_tools import GameEngine, BoardFactory

def columns_init() -> ColumnsGameLoop:
    """
        Initialize objects needed to start a game of columns
        :returns: game objects
        :rtype: ColumnsGameLoop
    """
    board = BoardFactory.create_board(ColumnsBoard, ColumnsBoard.COLUMNS_BOARD_WIDTH, ColumnsBoard.COLUMNS_BOARD_HEIGHT)
    score = ColumnsScoring()
    state = ColumnsGameState(board, score)
    view = ColumnsView(state)
    loop = ColumnsGameLoop(state, view)
    return loop

@click.command()
def columns():
    """Entry point to columns"""
    GameEngine([columns_init()]).run()

    
