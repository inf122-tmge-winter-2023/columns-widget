"""
    :module_name: cli
    :module_summary: a CLI for columns_widget
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import click

from . import columns_init

from tilematch_tools import GameEngine

@click.command()
def columns():
    """Entry point to columns"""
    ge = GameEngine([columns_init()])
    ge._game_loops[0].view.add_event_listener("KeyRelease")
    ge.run()

    
