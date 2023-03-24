# columns

## About

This is a sample game that is built on top of the `tilematch_tools` package. It emulate a simplified version of the game [Columns](https://en.wikipedia.org/wiki/Columns_(video_game)) This game is compatible to run using the built-in game engine.

## Game rules

- Tiles is set of 3 fall from the top of the board
- Every second, the falling set of tiles lowers itself down 1 level on the board
- The falling set of tiles stop falling if
    - Another tile is blocking its descent file
    - It has reached the bottom of the board
- When the falling set of tiles freezes, three of a kind matches are removed
    - This causes all tiles to collapse down as far as possible
    - Matches caused subsequently are removed as well
    - Players are awarded 3 points per matching tile
- When falling set of tiles are in motion they can
    - Be shifted to the left, as long as the file to the left is not blocked or at the edge of the board
    - Be shifted to the right, as long as the ifle to the right is not blocked or at the edge of the board
    - Rotated upward by having the top-most tile be at the bottom
    - Rotated downward by having the bottom-most tile be at the top
- Game ends
    - The game ends when a falling set of tiles freezes without all of its tiles being visible on the board

## Known issues

[View them here](https://github.com/inf122-tmge-winter-2023/columns-widget/issues/)

## Contributers

- Nathan Mendoza (nathancm@uci.edu)
