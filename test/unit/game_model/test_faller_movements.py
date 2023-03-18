"""Tests for faller movements"""

import pytest

from tilematch_tools import BoardFactory, NullTile, TileBuilder

from columns_widget.game_model import FallerShiftRight, FallerShiftLeft, ColumnsBoard, ColumnsTile, ColumnsColor, ColumnsFaller

class TestFallerShiftMovement:
    def setup_method(self):
        self.faller = ColumnsFaller()
        for y, tile in enumerate(self.faller.members, 5):
            tile.position = (4, y)
        self.board = BoardFactory.create_board_with_tiles(
                ColumnsBoard,
                ColumnsBoard.COLUMNS_BOARD_WIDTH,
                ColumnsBoard.COLUMNS_BOARD_HEIGHT,
                self.faller.members
                )

    @pytest.mark.parametrize('shifter, result_file', [
        (FallerShiftRight(), 5),
        (FallerShiftLeft(), 3)
    ])
    def test_single_successful_shift_in_descent_file(self, shifter, result_file):
        shifter.move(self.board, self.faller)
        assert all(tile.position.x == result_file for tile in self.faller.members)

    @pytest.mark.parametrize('shifter, result_file', [
        (FallerShiftRight(), 7),
        (FallerShiftLeft(), 1)
    ])
    def test_multiple_successful_shifts_in_descent_file(self, shifter, result_file):
        for _ in range(3):
            shifter.move(self.board, self.faller)

        assert all(tile.position.x == result_file for tile in self.faller.members)

    @pytest.mark.parametrize('shifter, result_file', [
        (FallerShiftRight(), 7),
        (FallerShiftLeft(), 1)
    ])
    def test_cannot_beyond_edge_of_board(self, shifter, result_file):
        for _ in range(4):
            shifter.move(self.board, self.faller)

        assert all(tile.position.x == result_file for tile in self.faller.members)

    @pytest.mark.parametrize('shifter, block_file, result_file', [
        (FallerShiftRight(), 7, 6),
        (FallerShiftLeft(), 1, 2)
    ])
    def test_cannot_move_to_file_if_blocked_at_bottom(self, shifter, block_file, result_file):
        self.board.place_tile(TileBuilder().add_position(block_file, 5).add_color(ColumnsColor.RED).construct(ColumnsTile))
        for _ in range(3):
            shifter.move(self.board, self.faller)

        assert all(tile.position.x == result_file for tile in self.faller.members)

    @pytest.mark.parametrize('shifter, block_file, result_file', [
        (FallerShiftRight(), 7, 6),
        (FallerShiftLeft(), 1, 2)
    ])
    def test_cannot_move_to_file_if_blocked_at_center(self, shifter, block_file, result_file):
        self.board.place_tile(TileBuilder().add_position(block_file, 6).add_color(ColumnsColor.RED).construct(ColumnsTile))
        for _ in range(3):
            shifter.move(self.board, self.faller)

        assert all(tile.position.x == result_file for tile in self.faller.members)

    @pytest.mark.parametrize('shifter, block_file, result_file', [
        (FallerShiftRight(), 7, 6),
        (FallerShiftLeft(), 1, 2)
    ])
    def test_cannot_move_to_file_if_blocked_at_top(self, shifter, block_file, result_file):
        self.board.place_tile(TileBuilder().add_position(block_file, 7).add_color(ColumnsColor.RED).construct(ColumnsTile))
        for _ in range(3):
            shifter.move(self.board, self.faller)

        assert all(tile.position.x == result_file for tile in self.faller.members)
