"""
    :module_name: columns_widget
    :module_summary: A widget hosting an instance of Columns tile matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
import time

from tilematch_tools import GameLoop, GameState, NullTile
from tilematch_tools.model.exceptions import InvalidBoardPositionError

from .game_model import ColumnsColor, ColumnsTile, ColumnsFaller, \
        ColumnsScoring, ColumnsBoard, \
                        SingleStepDescent
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
        self._last_fall = time.time_ns()

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

    def cycle_fallers(self) -> None:
        LOGGER.info('Cycling fallers')
        self._active_faller = self._next_faller
        self._next_faller = ColumnsFaller()

    def drop_faller(self) -> None:
        self.__await_faller_delay()
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

    def __await_faller_delay(self) -> None:
        while time.time_ns() < self._last_fall + 1_000_000_000:
            pass
        self._last_fall = time.time_ns()


class ColumnsGameLoop(GameLoop):
    """
        Game loop logic for columns
    """

    def handle_input(self):
        super().handle_input()
        self._move_faller()

    def find_matches(self, match_rules):
        super().find_matches(match_rules)

    def clear_matches(self, matches):
        super().clear_matches(matches)

    def update_view(self):
        super().update_view()

    def gameover(self):
        super().gameover()

    def _move_faller(self):
        self.state.drop_faller()

    


