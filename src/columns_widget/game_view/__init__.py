"""
    :module_name: game_view
    :module_summary: view class for columns
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from tilematch_tools import GameView, GameState, GameEvent


class ColumnsView(GameView):
    """Class representing the columns view"""
    def __init__(self, parent, game_state: GameState):
        super().__init__(parent, game_state)

class ShiftFallerLeft(GameEvent):
    def __call__(self, event):
        self.listener.shift_faller_left()

class ShiftFallerRight(GameEvent):
    def __call__(self, event):
        self.listener.shift_faller_right()

class RotateFallerUp(GameEvent):
    def __call__(self, event):
        self.listener.rotate_faller_up()

class RotateFallerDown(GameEvent):
    def __call__(self, event):
        self.listener.rotate_faller_down()
