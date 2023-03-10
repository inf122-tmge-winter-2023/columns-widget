"""
    :module_name: cli
    :module_summary: a CLI for columns_widget
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import click
import tilematch_tools

@click.command()
def columns():
    """Entry point to columns"""
    click.echo('Hello World!')
