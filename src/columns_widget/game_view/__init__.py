"""
    :module_name: game_view
    :module_summary: view class for columns
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import tkinter as tk

from tilematch_tools import GameView, GameState, GameEvent, GameInfo
from tilematch_tools.view.board_view import BoundingBox
from tilematch_tools.model import TileColor

class ColumnsNextFallerView(GameInfo):
    top = BoundingBox(0, 0, 30, 30)
    center = BoundingBox(0, 30, 30, 60)
    bottom = BoundingBox(0, 60, 30, 90)
    def __init__(self, parent, game_to_watch: GameState, **options):
        self._watching = game_to_watch
        self._tiles = {}
        super().__init__(parent, **options)

    def create_widgets(self):
        self._next_label = tk.Label(self, text='Next: ', font=self.font, width=10, anchor=tk.N)
        self._next_display = tk.Canvas(self, width=30, height=90) # enough for three tiles stacked on top of each other
        self._init_display()

    def place_widgets(self):
        self._next_label.grid(column=0, row=0)
        self._next_display.grid(column=0, row=1)

    def _init_display(self):
        self._tiles['top'] = self._next_display.create_rectangle(
                self.top.start_x, 
                self.top.start_y, 
                self.top.end_x,
                self.top.end_y, 
                fill=TileColor.LIGHT_GRAY, 
                width=1
            )

        self._tiles['center'] = self._next_display.create_rectangle(
                self.center.start_x, 
                self.center.start_y, 
                self.center.end_x,
                self.center.end_y, 
                fill=TileColor.LIGHT_GRAY, 
                width=1
            )
        self._tiles['bottom'] = self._next_display.create_rectangle(
                self.bottom.start_x, 
                self.bottom.start_y, 
                self.bottom.end_x,
                self.bottom.end_y, 
                fill=TileColor.LIGHT_GRAY, 
                width=1
            )

    def update(self):
        self._next_display.itemconfig(
                self._tiles['bottom'],
                fill=self.watching.members[0].color,
                outline=self.watching.members[0].border,
                width=1
            )
            
        self._next_display.itemconfig(
                self._tiles['center'],
                fill=self.watching.members[1].color,
                outline=self.watching.members[1].border,
                width=1
            )

        self._next_display.itemconfig(
                self._tiles['top'],
                fill=self.watching.members[2].color,
                outline=self.watching.members[2].border,
                width=1
            )

    @property
    def watching(self):
        return self._watching.next_faller

class ColumnsView(GameView):
    """Class representing the columns view"""
    def __init__(self, parent, game_state: GameState):
        super().__init__(parent, game_state, 'Columns')
        self._add_next_view()

    @property
    def watching(self):
        return self._game

    def _add_next_view(self):
        self._game_widgets['next'] = ColumnsNextFallerView(self, self.watching)
        self._game_widgets['next'].grid(column=6, row=2, padx=30)

class ShiftFallerLeft(GameEvent):
    def __call__(self, event):
        self.listener.shift_faller_left()

class ShiftFallerRight(GameEvent):
    def __call__(self, event):
        self.listener.shift_faller_right()

class RotateFallerUp(GameEvent):
    def __call__(self, event):
        self.listener.rotate_faller_up()

class RotateFallerDown(GameEvent):
    def __call__(self, event):
        self.listener.rotate_faller_down()
