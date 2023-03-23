"""
    :module_name: columns_widget
    :module_summary: A widget hosting an instance of Columns tile matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging

from tilematch_tools.core import BoardFactory
from tilematch_tools.core.game_factory import Game, GameFactory

from .columns import ColumnsGameState, ColumnsGameLoop
from .game_model import ColumnsBoard, ColumnsScoring
from .game_view import ColumnsView

LOGGER = logging.getLogger(__name__)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMAT = logging.Formatter('[%(asctime)s|%(name)s|%(levelname)s] - %(message)s')

LOGGER.setLevel(logging.INFO)
LOG_HANDLER.setLevel(logging.INFO)

LOG_HANDLER.setFormatter(LOG_FORMAT)
LOGGER.addHandler(LOG_HANDLER)

__version__ = (0, 0, 1)


class ColumnsGame(Game):
    TICK = 750_000_000
            

class ColumnsGameFactory(GameFactory):
    @staticmethod
    def create_game() -> ColumnsGame:
        board = BoardFactory.create_board(ColumnsBoard, ColumnsBoard.COLUMNS_BOARD_WIDTH, ColumnsBoard.COLUMNS_BOARD_HEIGHT)
        score = ColumnsScoring()
        state = ColumnsGameState(board, score)
        return ColumnsGame(state, ColumnsGameLoop, ColumnsView, ColumnsGame.TICK)
 
