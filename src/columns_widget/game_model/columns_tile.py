"""
    :module_name: columns_tile
    :module_summary: class representing a columns tile
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import random
from enum import StrEnum

from tilematch_tools.model import Tile, TileGroup
from tilematch_tools.core import TileBuilder

class ColumnsColor(StrEnum):
    RED = "#a10b0b"
    ORANGE = "#ad6211"
    YELLOW = "#dce31b"
    GREEN = "#3ec934"
    BLUE = "#4a8af0"
    MAGENTA = "#b71ceb"


class ColumnsTile(Tile):
    """Class representing a colums tile"""
    pass

class ColumnsFaller(TileGroup):
    """Class representing a falling tile group"""

    def __init__(self):
        center, upper, lower = self._random_set_of_three()
        super().__init__(center)
        self.add_sibling_tile(upper, 0, 1)
        self.add_sibling_tile(lower, 0, -1)

    def _random_set_of_three(self) -> (ColumnsTile, ColumnsTile, ColumnsTile):
        """
            Helper method for generating a random set of three tiles
            :returns: random tile set
            :rtype: tuple
        """
        pass

    def _random_colums_tile(self) -> ColumnsTile:
        """
            Helper method for generating a random columns tile
            :returns: random tile
            :rtype: ColumnsTile
        """
        pass

