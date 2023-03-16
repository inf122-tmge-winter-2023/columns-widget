"""
    :module_name: columns_tile
    :module_summary: class representing a columns tile
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import random
import logging
from enum import StrEnum

from tilematch_tools.model import Tile, TileGroup
from tilematch_tools.core import TileBuilder

from .columns_board import ColumnsBoard

LOGGER = logging.getLogger(__name__)

class ColumnsColor(StrEnum):
    RED = "#a10b0b"
    ORANGE = "#ad6211"
    YELLOW = "#dce31b"
    GREEN = "#3ec934"
    BLUE = "#4a8af0"
    MAGENTA = "#b71ceb"


class ColumnsTile(Tile):
    """Class representing a colums tile"""
    def __repr__(self):
        """Sane string representation"""
        if self.color == ColumnsColor.RED:
            return 'R'
        if self.color == ColumnsColor.ORANGE:
            return 'O'
        if self.color == ColumnsColor.GREEN:
            return 'G'
        if self.color == ColumnsColor.BLUE:
            return 'B'
        if self.color == ColumnsColor.MAGENTA:
            return 'M'
        return '?'

class ColumnsFaller(TileGroup):
    """Class representing a falling tile group"""

    def __init__(self):
        center, upper, lower = self._random_set_of_three()
        super().__init__(center)
        self.add_sibling_tile(upper, 0, 1)
        self.add_sibling_tile(lower, 0, -1)
        self._descent_file = random.randint(1, ColumnsBoard.COLUMNS_BOARD_WIDTH)

    def _random_set_of_three(self) -> (ColumnsTile, ColumnsTile, ColumnsTile):
        """
            Helper method for generating a random set of three tiles
            :returns: random tile set
            :rtype: tuple
        """
        return [
                self._random_columns_tile() 
                for _ in range(3)
                ]

    def _random_columns_tile(self) -> ColumnsTile:
        """
            Helper method for generating a random columns tile
            :returns: random tile
            :rtype: ColumnsTile
        """
        return TileBuilder() \
                .add_position(self._descent_file, None) \ # tiles with None as y-position are staged
                .add_color(random.choice(list(ColumnsColor))) \
                .construct(tile_type=ColumnsTile)
