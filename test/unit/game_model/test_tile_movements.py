"""Tests for ColumnsTile Movement"""

import pytest

from tilematch_tools.core import BoardFactory, TileBuilder
from tilematch_tools.model import NullTile
from columns_widget.game_model import (SingleStepDescent,
                                       AbsoluteDescent,
                                       ColumnsBoard,
                                       ColumnsTile,
                                       ColumnsColor
                                       )

@pytest.fixture
def fall():
    return SingleStepDescent()

@pytest.fixture
def collapse():
    return AbsoluteDescent()

class TestColumnsTileMovement:
    def setup_method(self):
        init_tiles = [
                TileBuilder().add_position(3, 1).add_color(ColumnsColor.RED).construct(ColumnsTile),
                TileBuilder().add_position(4, 1).add_color(ColumnsColor.YELLOW).construct(ColumnsTile),
                TileBuilder().add_position(5, 1).add_color(ColumnsColor.GREEN).construct(ColumnsTile),
                TileBuilder().add_position(4, 4).add_color(ColumnsColor.BLUE).construct(ColumnsTile),
                TileBuilder().add_position(7, 7).add_color(ColumnsColor.ORANGE).construct(ColumnsTile)
                ]
        self.board = BoardFactory.create_board_with_tiles(
                ColumnsBoard,
                ColumnsBoard.COLUMNS_BOARD_WIDTH,
                ColumnsBoard.COLUMNS_BOARD_HEIGHT,
                init_tiles
                )

    def test_falling_tiles_falls_one_step_at_a_time(self, fall):
        fall.move(self.board, self.board.tile_at(4, 4))
        assert isinstance(self.board.tile_at(4, 4), NullTile)
        assert isinstance(self.board.tile_at(4, 3), ColumnsTile)

    def test_falling_tiles_falls_until_blocked(self, collapse):
        collapse.move(self.board, self.board.tile_at(4, 4))
        assert isinstance(self.board.tile_at(4, 4), NullTile)
        assert isinstance(self.board.tile_at(4, 2), ColumnsTile)

    def test_falling_tiles_stops_at_bottom_of_board(self, collapse):
        collapse.move(self.board, self.board.tile_at(7, 7))
        assert isinstance(self.board.tile_at(7, 7), NullTile)
        assert isinstance(self.board.tile_at(7, 1), ColumnsTile)
       
    def test_cannot_move_a_null_tile(self, fall, collapse):
        fall.move(self.board, self.board.tile_at(5, 5))
        assert isinstance(self.board.tile_at(5, 5), NullTile)
        collapse.move(self.board, self.board.tile_at(5, 5))
        assert isinstance(self.board.tile_at(5, 5), NullTile)

