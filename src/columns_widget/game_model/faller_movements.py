"""
    :module_name: faller_movements
    :module_summary: classes describing movements for ColumnsFallers
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
from abc import abstractmethod

from .columns_tile import ColumnsTile, ColumnsFaller, ColumnsColor

from tilematch_tools.model import MovementRule, NullTile, GameBoard
from tilematch_tools.model.exceptions import IllegalTileMovementException, InvalidBoardPositionError

LOGGER = logging.getLogger(__name__)

class FallerMovementRule(MovementRule):
    """
        Class that generalizes how a ColumnsFaller moves
    """

    def __init__(self, callback = None):
        self._after = callback
        self._faller_origins = None

    def move(self, board: GameBoard, faller: ColumnsFaller, *callback_args) -> None:
        """
            Apply this movement rule to the given faller on the specific gameboard
            Then calls the callback if one exists
            :arg board: gameboard the move will be made on
            :arg faller: faller to be moved
            :arg *callback_args: additional arguments to be passed to the callback
            :arg type: GameBoard
            :arg type: Tile
            :arg type: tuple
        """
        self._faller_origins = faller.positions
        try:
            LOGGER.info(
                    'Attempting to move faller on descent file %d', 
                    faller.descent_file
                    )
            self.apply(board, faller)
        except (IllegalTileMovementException, InvalidBoardPositionError):
            LOGGER.error('Could not apply movement rule %s. Reverting tile state', str(self))
            self.revert(board, faller)
        else:
            for i, tile in enumerate(faller.members):
                LOGGER.info(
                        'faller successfully moved from (%d, %d) -> (%d, %d)',
                        self._faller_origins[i][0],
                        self._faller_origins[i][1],
                        tile.position.x,
                        tile.position.y
                        )
            self._mark_null(board)
        finally:
            if self._after:
                self._after(*callback_args)
    
    @abstractmethod
    def apply(self, board: GameBoard, faller: ColumnsFaller) -> None:
        """
            Logic for executing this tile movement. Should raise exception if cannot be completed
            :arg board: gameboard move will be executed on
            :arg faller: faller to be moved by this movement rule (really a collection of tiles)
            :arg type: GameBoard
            :arg type: ColumnsFaller
            :raises: IllegalTileMovementException if the tile movement is illegal
            :raises: InvalidBoardPositionError if the tile's new position is invalid
        """
        LOGGER.warning('Using the default implementation. This is meant to be overridden!')

    def revert(self, board: GameBoard, faller: ColumnsFaller) -> None:
        """
            Reverts this movement rule by restoring faller original position
            :arg board: gameboard on which move will be reverted
            :arg faller: faller which will be un-moved
            :arg type: GameBoard
            :arg type: ColumnsFaller
            :returns: Nothing
            :rtype: None
        """
        for i, tile in enumerate(faller.members):
            LOGGER.info(
                    'Reverting faller member %d to position (%d, %d)',
                    i,
                    self._faller_origins[i][0],
                    self._faller_origins[i][1]
            )
            tile.position = (self._faller_origins[i][0], self._faller_origins[i][1])

    def _mark_null(self, board: GameBoard) -> None:
        for x, y in self._faller_origins:
            LOGGER.info('Marking (%d, %d) with a null tile', x, y)
            if y != ColumnsFaller.STAGED:
                board.place_tile(
                    NullTile(
                        **{
                            'position': (x, y),
                            'color': '#D3D3D3'
                        }
                    )
                )

 

class FallerShiftRight(FallerMovementRule):
    """
        Class that specfies how a ColumnsFaller shifts right
    """
    def apply(self, board: GameBoard, faller: ColumnsFaller) -> None:
        """
            Logic for executing this tile movement. Should raise exception if cannot be completed
            :arg board: gameboard move will be executed on
            :arg faller: faller to be moved by this movement rule (really a collection of tiles)
            :arg type: GameBoard
            :arg type: ColumnsFaller
            :raises: IllegalTileMovementException if the tile movement is illegal
            :raises: InvalidBoardPositionError if the tile's new position is invalid
        """
        for tile in faller.members:
            tile.position = (tile.position.x + 1, tile.position.y)
            if tile.position.y != ColumnsFaller.STAGED:
                board.place_tile(tile)
