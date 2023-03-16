"""Tests for columns tile"""

import pytest

from tilematch_tools.model.tiles import Tile, TileShape, TileGroup
from columns_widget.game_model import ColumnsColor, ColumnsTile, ColumnsFaller

class TestColumnsColor:
    def test_color_count_is_six(self):
        assert len(ColumnsColor) == 6

    def test_members_can_be_used_as_str(self):
        try:
            for color in ColumnsColor:
                color + ""
        except TypeError:
            assert False, f'Members of ColumnColor are not string like'

class TestColumnsTile:
    def setup_method(self):
        self.the_tile = ColumnsTile(**{'position': (None, None), 'color': ColumnsColor.RED})

    def test_columns_tile_is_instance_of_tile(self):
        assert isinstance(self.the_tile, Tile)

    def test_columns_tile_color_is_from_game_specific_enum(self):
        assert self.the_tile.color in ColumnsColor

    def test_columns_tile_shape_is_square(self):
        assert self.the_tile.shape == TileShape.SQUARE

    @pytest.mark.parametrize('color, _repr', [
        (ColumnsColor.RED, 'R'),
        (ColumnsColor.ORANGE, 'O'),
        (ColumnsColor.YELLOW, 'Y'),
        (ColumnsColor.GREEN, 'G'),
        (ColumnsColor.BLUE, 'B'),
        (ColumnsColor.MAGENTA, 'M'),
        ('#anothercolor', '?')
        ])
    def test_columns_tile_representation(self, color, _repr):
        the_tile = ColumnsTile(**{'position': (None, None), 'color': color})
        assert repr(the_tile) == _repr

class TestColumnsFaller:
    def setup_method(self):
        self.the_faller = ColumnsFaller()

    def test_faller_contains_three_tiles(self):
        assert self.the_faller.size == 3
