"""
    :module_name: cli
    :module_summary: a CLI for columns_widget
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import click

from . import ColumnsGameFactory

from tilematch_tools import GameEngine

@click.command()
def columns():
    """Entry point to columns"""
    ge = GameEngine([ColumnsGameFactory.create_game()])
    ge.run()

    
