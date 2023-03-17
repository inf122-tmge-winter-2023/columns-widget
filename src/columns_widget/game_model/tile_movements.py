"""
    :module_name: tile_movements
    :module_summary: classes that describe ColumnTile movements
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from tilematch_tools.model import MovementRule, GameBoard, Tile, NullTile

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

        
