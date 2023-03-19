"""
    :module_name: tile_movements
    :module_summary: classes that describe ColumnTile movements
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging

from tilematch_tools.model import MovementRule, GameBoard, Tile, NullTile
from tilematch_tools.model.exceptions import IllegalTileMovementException
from .columns_tile import ColumnsFaller

LOGGER = logging.getLogger(__name__)

class SingleStepDescent(MovementRule):
    """
        Class that specifies that a ColumnsTile should make a descent by one level
    """
    def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
        """
            Logic for executing this tile movement. Should raise exception if cannot be completed
            :arg board: gameboard move will be executed on
            :arg tile_to_move: tile to be moved by this movement rule
            :arg type: GameBoard
            :arg type: Tile
            :raises: IllegalTileMovementException if the tile movement is illegal
            :raises: InvalidBoardPositionError if the tile's new position is invalid
        """
        tile_to_move.position = (tile_to_move.position.x, tile_to_move.position.y - 1)
        board.place_tile(tile_to_move)

    def _mark_null(self, board: GameBoard):
        if self._origin_y == ColumnsFaller.STAGED:
            LOGGER.info('Tile fell from y=%d, not marking the staged tile as null', ColumnsFaller.STAGED)
            return

        LOGGER.info('Marking (%d, %d) with a null tile', self._origin_x, self._origin_y)
        board.place_tile(
                NullTile(
                    **{
                        'position': (self._origin_x, self._origin_y),
                        'color': '#D3D3D3'
                    }
                )
        )


class AbsoluteDescent(MovementRule):
    """
        Class that specifies that a ColumnsTile descent until blocked
    """
    def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
        """
            Logic for executing this tile movement. Should raise exception if cannot be completed
            :arg board: gameboard move will be executed on
            :arg tile_to_move: tile to be moved by this movement rule
            :arg type: GameBoard
            :arg type: Tile
            :raises: IllegalTileMovementException if the tile movement is illegal
            :raises: InvalidBoardPositionError if the tile's new position is invalid
        """
        descent_file = tile_to_move.position.x 
        new_y_lvl = tile_to_move.position.y
        while new_y_lvl > 1 and isinstance(board.tile_at(descent_file, new_y_lvl - 1), NullTile):
            new_y_lvl -= 1

        if tile_to_move.position.y != new_y_lvl:
            tile_to_move.position = (descent_file, new_y_lvl)
            board.place_tile(tile_to_move)
        else:
            LOGGER.error('Tile at (%d, %d is already as low as possible', tile_to_move.position.x, tile_to_move.position.y)
            raise IllegalTileMovementException(f'Tile at ({tile_to_move.position.x}, {tile_to_move.position.y}) is already as low as possible')
