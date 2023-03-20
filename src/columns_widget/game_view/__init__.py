"""
    :module_name: game_view
    :module_summary: view class for columns
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from tilematch_tools import View, GameState

class ColumnsView(View):
    """Class representing the columns view"""
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
