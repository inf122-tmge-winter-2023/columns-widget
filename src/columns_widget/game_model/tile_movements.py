"""
    :module_name: tile_movements
    :module_summary: classes that describe ColumnTile movements
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from tilematch_tools.model import MovementRule

class SingleStepDescent(MovementRule):
    """
        Class that specifies that a ColumnsTile should make a descent by one level
    """

    def __init__(self):
        super().__init__(0, -1)

    def exec(self, x: int, y: int) -> (int, int):
        """
            Provide information required to apply this movement rule
            :arg x: current x position
            :arg y: current y position
            :arg type: int
            :arg type: int
            :returns: new position
            :rtype: (int, int)
        """
        return (x + self._dx, y + self._dy)
