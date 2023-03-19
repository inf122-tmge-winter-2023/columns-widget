"""Tests for columns match rules"""

import pytest
import itertools

from tilematch_tools.core import BoardFactory, TileBuilder
from tilematch_tools.model import NullTile
from columns_widget.game_model import ColumnsBoard, ColumnsTile, ColumnsColor
from columns_widget.game_model.match_rules import *

match_rules = [
           ThreeFoldNorth(),
           ThreeFoldEast(),
           ThreeFoldSouth(),
           ThreeFoldWest(),
           ThreeFoldNorthEast(),
           ThreeFoldSouthEast(),
           ThreeFoldSouthWest(),
           ThreeFoldNorthWest()
            ]
init_tiles = [
            TileBuilder().add_position(1, 1).add_color(ColumnsColor.RED).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(1, 2).add_color(ColumnsColor.RED).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(1, 3).add_color(ColumnsColor.RED).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(1, 7).add_color(ColumnsColor.BLUE).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(2, 7).add_color(ColumnsColor.BLUE).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(3, 7).add_color(ColumnsColor.BLUE).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(2, 2).add_color(ColumnsColor.YELLOW).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(3, 3).add_color(ColumnsColor.YELLOW).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(4, 4).add_color(ColumnsColor.YELLOW).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(3, 12).add_color(ColumnsColor.GREEN).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(4, 11).add_color(ColumnsColor.GREEN).construct(tile_type=ColumnsTile),
            TileBuilder().add_position(5, 10).add_color(ColumnsColor.GREEN).construct(tile_type=ColumnsTile)
                ]
expected_matches = [
        (ThreeFoldNorth, init_tiles[0]),
        (ThreeFoldEast, init_tiles[3]),
        (ThreeFoldSouth, init_tiles[2]),
        (ThreeFoldWest, init_tiles[5]),
        (ThreeFoldNorthEast, init_tiles[6]),
        (ThreeFoldSouthEast, init_tiles[9]),
        (ThreeFoldSouthWest, init_tiles[8]),
        (ThreeFoldNorthWest, init_tiles[11])
        ]

class TestColumnsMatchRules:

    def setup_method(self):
        self.board = BoardFactory.create_board_with_tiles(
                ColumnsBoard, 
                ColumnsBoard.COLUMNS_BOARD_WIDTH,
                ColumnsBoard.COLUMNS_BOARD_HEIGHT,
                init_tiles)

    @pytest.mark.parametrize('start, rule', 
            itertools.product(init_tiles, match_rules)
    )
    def test_three_fold_matches(self, start, rule):
        if any(id(start) == id(match[1]) for match in filter(lambda m: m[0] is type(rule), expected_matches)):
            assert rule.check_match(
                    self.board,
                    start.position.x,
                    start.position.y
                    ) is not None
        else:
            assert rule.check_match(
                    self.board, 
                    start.position.x,
                    start.position.y
                   ) is None

    @pytest.mark.parametrize('x, y, rule', 
        itertools.product(
            range(1, ColumnsBoard.COLUMNS_BOARD_WIDTH), 
            range(1, ColumnsBoard.COLUMNS_BOARD_HEIGHT),
            match_rules
            )
    )
    def test_three_fold_match_result_is_none_when_starting_at_null_tile(self, x, y, rule):
        if isinstance(self.board.tile_at(x, y), NullTile):
            assert rule.check_match(self.board, x, y) is None
        else:
            assert True
