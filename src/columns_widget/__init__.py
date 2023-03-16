"""
    :module_name: columns_widget
    :module_summary: A widget hosting an instance of Columns tile matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging

LOGGER = logging.getLogger(__name__)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMAT = logging.Formatter('[%(asctime)s|%(name)s|%(levelname)s] - %(message)s')

LOGGER.setLevel(logging.DEBUG)
LOG_HANDLER.setLevel(logging.DEBUG)

LOG_HANDLER.setFormatter(LOG_FORMAT)
LOGGER.addHandler(LOG_HANDLER)

__version__ = (0, 0, 1)

from .columns_tile import ColumnsColor, ColumnsTile, ColumnsFaller
