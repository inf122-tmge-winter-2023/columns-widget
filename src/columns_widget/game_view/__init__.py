"""
    :module_name: game_view
    :module_summary: view class for columns
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from tilematch_tools import GameView, GameState

class ColumnsView(GameView):
    """Class representing the columns view"""
    def __init__(self, parent, game_state: GameState):
        super().__init__(parent, game_state)
