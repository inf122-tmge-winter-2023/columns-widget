"""
    :module_name: match_rules
    :module_summary: match rule definitions for Columns
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging

from tilematch_tools.model.match import MatchCondition, ScanDelta
from tilematch_tools.model.exceptions import InvalidBoardPositionError
from tilematch_tools.model import GameBoard, NullTile

LOGGER = logging.getLogger(__name__)

class ThreeFoldMatch(MatchCondition):
    """
        A generalized three match condition
    """

    def check_match(self, board: GameBoard, start_x: int, start_y: int) -> MatchCondition.MatchFound or None:
        """
            Check for a three-match on the given board starting at the specified position
            :arg board: the board to check a match for
            :arg start_x: the x position the match scan starts at
            :arg start_y: the y position the match scan starts at
            :arg type: GameBoard
            :arg type: int
            :arg type: int
            :returns: A object describing the match if one was found, None otherwise
            :rtype: MatchFound or None
        """
        if isinstance(board.tile_at(start_x, start_y), NullTile):
            LOGGER.info('No tile to match at (%d, %d)', start_x, start_y)
            return
        matching_tiles = [board.tile_at(start_x, start_y)]
        LOGGER.info('Checking for match starting at (%d, %d). Using %s as the scan delta', start_x, start_y, str(self._scan_delta))
        try:
            for i in range(1, 3):
                LOGGER.info(
                        'Checking if (%d, %d) can be added to the match',
                        start_x + self._scan_delta.value[0] * i,
                        start_y + self._scan_delta.value[1] * i
                        )
                if all(self._eq(prev, board.tile_at(start_x + self._scan_delta.value[0] * i, start_y + self._scan_delta.value[1] * i)) for prev in matching_tiles):
                    LOGGER.info('Tile at (%d, %d) joined the match!', start_x + self._scan_delta.value[0] * i, start_y + self._scan_delta.value[1] * i)
                    matching_tiles.append(board.tile_at(start_x + self._scan_delta.value[0] * i, start_y + self._scan_delta.value[1] * i))
                else:
                    LOGGER.info('Tile at (%d, %d) broke the streak! Come on dude, WTF?!?', start_x + self._scan_delta.value[0] * i, start_x + self._scan_delta.value[1] * i)
                    return
        except InvalidBoardPositionError:
            LOGGER.info('Matching sequence starting at (%d, %d) abruptly terminated', start_x, start_y)
            return
        else:
            LOGGER.info('Match of three discovered at (%d, %d)', start_x, start_y)
            return MatchCondition.MatchFound(self.point_value * len(matching_tiles), matching_tiles)

class ThreeFoldNorth(ThreeFoldMatch):
    """Three match in an upward direction"""
    def __init__(self):
        super().__init__(ScanDelta.UP, 3)
    
class ThreeFoldSouth(ThreeFoldMatch):
    """Three match in an downward direction"""
    def __init__(self):
        super().__init__(ScanDelta.DOWN, 3)

class ThreeFoldEast(ThreeFoldMatch):
    """Three match in an eastward direction"""
    def __init__(self):
        super().__init__(ScanDelta.RIGHT, 3)

class ThreeFoldWest(ThreeFoldMatch):
    """Three match in an westward direction"""
    def __init__(self):
        super().__init__(ScanDelta.LEFT, 3)

class ThreeFoldNorthWest(ThreeFoldMatch):
    """Three match in an nothwestward direction"""
    def __init__(self):
        super().__init__(ScanDelta.UPANDLEFT, 3)

class ThreeFoldNorthEast(ThreeFoldMatch):
    """Three match in an norteastward direction"""
    def __init__(self):
        super().__init__(ScanDelta.UPANDRIGHT, 3)

class ThreeFoldSouthEast(ThreeFoldMatch):
    """Three match in an southeastward direction"""
    def __init__(self):
        super().__init__(ScanDelta.DOWNANDRIGHT, 3)

class ThreeFoldSouthWest(ThreeFoldMatch):
    """Three match in an southwestward direction"""
    def __init__(self):
        super().__init__(ScanDelta.DOWNANDLEFT, 3)
