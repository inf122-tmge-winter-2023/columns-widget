"""
    :module_name: columns_scoring
    :module_summary: scoring class for columns
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from tilematch_tools.model import Scoring, MatchCondition

class ColumnsScoring(Scoring):
    """Class representing the columns scoring system"""

    def award_for_match(self, match: MatchCondition.MatchFound):
        """
            award the points specified by a given match condition to the score
            :arg match: the match condition awarding points
            :arg type: MatchFound
            :returns: nothing
            :rtype: None
        """
        super().award_for_match(match)
