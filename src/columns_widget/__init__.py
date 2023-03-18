"""
    :module_name: columns_widget
    :module_summary: A widget hosting an instance of Columns tile matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging

from tilematch_tools import GameLoop
from tilematch_tools import GameState

from .game_model import ColumnsColor, ColumnsTile, ColumnsFaller, ColumnsScoring, ColumnsBoard
from .game_view import ColumnsControls, ColumnsView

LOGGER = logging.getLogger(__name__)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMAT = logging.Formatter('[%(asctime)s|%(name)s|%(levelname)s] - %(message)s')

LOGGER.setLevel(logging.DEBUG)
LOG_HANDLER.setLevel(logging.DEBUG)

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


class ColumnsGameLoop(GameLoop):
    """
        Game loop logic for columns
    """

    def handle_input(self):
        super().handle_input()

    def find_matches(self, match_rules):
        super().find_matches(match_rules)

    def clear_matches(self, matches):
        super().clear_matches(matches)

    def update_view(self):
        super().update_view()

    def gameover(self):
        super().gameover()
    


