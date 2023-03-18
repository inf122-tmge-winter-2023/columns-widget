"""
    :module_name: game_view
    :module_summary: view class for columns
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from tilematch_tools import View, GameState

class ColumnsControls:
    SHUFFLE_FALLER_DOWN = 'KeyPress-S'
    SHUFFLE_FALLER_UP = 'KeyPress-W'
    SHIFT_FALLER_LEFT = 'KeyPress-A'
    SHIFT_FALLER_RIGHT = 'KeyPress-D'

class ColumnsView(View):
    """Class representing the columns view"""
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

        #self._bind_keys()

    def _bind_keys(self) -> None:
        """
            Bind the keys necessary for a game of columns
            :rtype: None
        """
        self.add_event_listener(ColumnsControls.SHUFFLE_FALLER_DOWN)
        self.add_event_listener(ColumnsControls.SHUFFLE_FALLER_UP)
        self.add_event_listener(ColumnsControls.SHIFT_FALLER_LEFT)
        self.add_event_listener(ColumnsControls.SHIFT_FALLER_RIGHT)
