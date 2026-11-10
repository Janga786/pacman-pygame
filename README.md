# Pac-Man in Pygame

A small Pac-Man clone in one Python file (`pacman.py`, 443 lines). Personal learning project.

## Run it

```bash
pip install pygame
python pacman.py
```

Arrow keys steer. Dots are worth 10 points. You have three lives; clearing the maze starts the next level with Pac-Man and the ghosts 0.5 px/frame faster.

## What is in the file

| Piece | Role |
| --- | --- |
| `Wall`, `Dot`, `PowerPellet` | maze cells built from the ASCII `LEVEL_LAYOUT` by `build_level()` |
| `Pacman` | player; moves 2 px per frame, snaps to the 20 px grid when blocked, draws a mouth arc |
| `Ghost` | four ghosts with different target rules (Blinky: Pac-Man; Pinky: 4 tiles ahead; Inky: reflected off Blinky; Clyde: chase when far, retreat when close) |
| `reset_level()`, `game_over()`, `main()`, `main_loop()` | respawn after a death or level clear, game-over screen, setup, and the 60 fps loop |

Ghost steering: when a ghost is blocked, it considers the non-reversing directions that are open and picks the one whose next tile is closest (squared Euclidean distance) to its target; if none is open it reverses.

## Known gaps

- Power pellets (+50, ghosts frightened for 7 s, +200 per eaten ghost) and screen-edge wrapping are implemented in code, but the current maze layout has no power pellets and no open side tunnel, so neither comes up in play.
- Ghosts only re-choose direction when they hit a wall, not at every intersection.

## License

[MIT](LICENSE). Pac-Man is a trademark of BANDAI NAMCO Entertainment Inc.; no original game assets are included (see the notice in `LICENSE`).
