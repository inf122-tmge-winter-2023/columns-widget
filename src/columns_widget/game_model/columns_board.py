"""
    :module_name: columns_board
    :module_summary: game board for columns tile matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from tilematch_tools.model import GameBoard

class ColumnsBoard(GameBoard):
    """
        Class representing a columns gameboard
    """
    COLUMNS_BOARD_HEIGHT = 13
    COLUMNS_BOARD_WIDTH = 7
