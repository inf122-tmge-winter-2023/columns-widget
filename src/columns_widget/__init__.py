"""
    :module_name: columns_widget
    :module_summary: A widget hosting an instance of Columns tile matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
import time
import queue

from tilematch_tools import GameLoop, GameState, NullTile
from tilematch_tools.model.exceptions import InvalidBoardPositionError

from .game_model import ColumnsColor, ColumnsTile, ColumnsFaller, \
                        ColumnsScoring, ColumnsBoard, \
                        SingleStepDescent, AbsoluteDescent, \
                        ThreeFoldNorth, ThreeFoldEast, ThreeFoldSouth, ThreeFoldWest, \
                        ThreeFoldNorthEast, ThreeFoldNorthWest, \
                        ThreeFoldSouthEast, ThreeFoldSouthWest, \
                        FallerShiftRight, FallerShiftLeft, \
                        FallerShuffleUp, FallerShuffleDown
from .game_view import ColumnsControls, ColumnsView

LOGGER = logging.getLogger(__name__)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMAT = logging.Formatter('[%(asctime)s|%(name)s|%(levelname)s] - %(message)s')

LOGGER.setLevel(logging.INFO)
LOG_HANDLER.setLevel(logging.INFO)

LOG_HANDLER.setFormatter(LOG_FORMAT)
LOGGER.addHandler(LOG_HANDLER)

__version__ = (0, 0, 1)


class ColumnsGameState(GameState):
    """
        Columns game state logic
    """

    def __init__(self, board: ColumnsBoard, score: ColumnsScoring):
        LOGGER.info('New columns game state')
        super().__init__(board, score)
        self._active_faller = None
        self._next_faller = ColumnsFaller()
        self._fallen = []

    @property
    def active_faller(self) -> ColumnsFaller:
        """
            Return a reference to current active faller
            :rtype: ColumnsFaller
        """
        return self._active_faller

    @property
    def next_faller(self) -> ColumnsFaller:
        """
            Return a reference to the next faller
            :rtype: ColumnsFaller
        """
        return self._next_faller

    @property
    def match_rules(self):
        return [
                ThreeFoldNorth,
                ThreeFoldSouth,
                ThreeFoldEast,
                ThreeFoldWest,
                ThreeFoldNorthWest,
                ThreeFoldNorthEast,
                ThreeFoldSouthWest,
                ThreeFoldSouthEast
                ]

    def shift_faller_left(self):
        if not self._active_faller:
            return

        FallerShiftLeft().move(self.board, self._active_faller)

    def shift_faller_right(self):
        if not self._active_faller:
            return

        FallerShiftRight().move(self.board, self._active_faller)

    def rotate_faller_up(self):
        if not self._active_faller:
            return

        FallerShuffleUp().move(self.board, self._active_faller, self.board, self._active_faller) # list twice for after move callback

    def rotate_faller_down(self):
        if not self._active_faller:
            return

        FallerShuffleDown().move(self.board, self._active_faller, self.board, self._active_faller) #list twice for after move callback

    def cycle_fallers(self) -> None:
        LOGGER.info('Cycling fallers')
        if self._active_faller:
            self._fallen.append(self._active_faller)
            self._active_faller = None
        else:
            self._active_faller = self._next_faller
            self._next_faller = ColumnsFaller()

    def drop_faller(self) -> None:
        if self.faller_can_fall():
            for tile in self._active_faller.members:
                SingleStepDescent().move(self.board, tile)
        else:
            self.cycle_fallers()

    def faller_can_fall(self) -> bool:
        """Determine whether the faller is able to fall"""
        if self._active_faller:
            try:
                bottom_of_faller = self._active_faller.members[0].position
                return isinstance(self.board.tile_at(bottom_of_faller.x, bottom_of_faller.y - 1), NullTile)
            except InvalidBoardPositionError:
                LOGGER.error('Faller is at the bottom of the board')
                return False
        return False

    def collapse_all(self):
        for x in range(1, ColumnsBoard.COLUMNS_BOARD_WIDTH + 1):
            for y in range(1, ColumnsBoard.COLUMNS_BOARD_HEIGHT + 1):
                AbsoluteDescent().move(self.board, self.board.tile_at(x, y))


class ColumnsGameLoop(GameLoop):
    """
        Game loop logic for columns
    """

    def handle_input(self):
        self._handle_key_inputs()
        self._move_faller()

    def find_matches(self, match_rules):
        if self.state.active_faller:
            return []
        return [
            match_rule().check_match(self.state.board, x, y)
            for match_rule in match_rules
            for x in range(1, self.state.board.num_cols + 1)
            for y in range(1, self.state.board.num_rows + 1)
            if match_rule().check_match(self.state.board, x, y) is not None
        ]

    def clear_matches(self, matches):
        for match in matches:
            self._state.clear_match(match)
            self._state.adjust_score(match)

        self.await_delay()
        self.update_view()
        
        self.state.collapse_all()
 
    def update_view(self):
        super().update_view()

    def gameover(self):
        super().gameover()

    def _move_faller(self):
        self.state.drop_faller()

    def _handle_key_inputs(self):
        try:
            while True:
                key = self.view.key_event
                LOGGER.info('Processing %s key input', key)
                if key == 'a': self.state.shift_faller_left() 
                if key == 'd': self.state.shift_faller_right()
                if key == 'w': self.state.rotate_faller_up()
                if key == 's': self.state.rotate_faller_down()
        except queue.Empty:
            LOGGER.info('No more key inputs to process')
