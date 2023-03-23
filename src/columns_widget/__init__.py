"""
    :module_name: columns_widget
    :module_summary: A widget hosting an instance of Columns tile matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
import time

from tilematch_tools import GameLoop, GameState, NullTile, BoardFactory
from tilematch_tools.model.exceptions import InvalidBoardPositionError

from .game_model import ColumnsColor, ColumnsTile, ColumnsFaller, \
                        ColumnsScoring, ColumnsBoard, \
                        SingleStepDescent, AbsoluteDescent, \
                        ThreeFoldNorth, ThreeFoldEast, ThreeFoldSouth, ThreeFoldWest, \
                        ThreeFoldNorthEast, ThreeFoldNorthWest, \
                        ThreeFoldSouthEast, ThreeFoldSouthWest, \
                        FallerShiftRight, FallerShiftLeft, \
                        FallerShuffleUp, FallerShuffleDown
from .game_view import ColumnsView, ShiftFallerLeft, ShiftFallerRight, RotateFallerUp, RotateFallerDown

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
    
    def gameover(self):
        if self.prev_faller:
            return any(
                tile.position.y == ColumnsFaller.STAGED
                for tile in self.prev_faller.members
            )
        return False



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
    def prev_faller(self) -> ColumnsFaller or None:
        """
            Return a reference to the last faller that has fallen
            :rtype: ColumnsFaller if at least one faller has fallen or None
        """
        return self._fallen[-1] if self._fallen else None

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
        for tile in self.board:
            AbsoluteDescent().move(self.board, tile)


class ColumnsGameLoop(GameLoop):
    """
        Game loop logic for columns
    """
    P1_BIND = {'up': 'w', 'down': 's', 'left': 'a', 'right': 'd'}
    P2_BIND = {'up': 'i', 'down': 'k', 'left': 'j', 'right': 'l'}

    __count = 0

    def __init__(self, state, view, delay):
        super().__init__(state, view, delay)
        if ColumnsGameLoop.__count > 0:
            self.bind_inputs(self.P2_BIND)
        else:
            self.bind_inputs(self.P1_BIND)
            ColumnsGameLoop.__count += 1

    def tick(self):
        self.state.drop_faller()

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


    def clean_up_state(self):
        self.state.collapse_all()
        time.sleep(1)

    
    def bind_inputs(self, bindings = {'up': 'w', 'down': 's', 'left': 'a', 'right': 'd'}):
        self.view.bind_key(f'<KeyRelease-{bindings["left"]}>', ShiftFallerLeft(self.state))
        self.view.bind_key(f'<KeyRelease-{bindings["right"]}>', ShiftFallerRight(self.state))
        self.view.bind_key(f'<KeyRelease-{bindings["up"]}>', RotateFallerUp(self.state))
        self.view.bind_key(f'<KeyRelease-{bindings["down"]}>', RotateFallerDown(self.state))

