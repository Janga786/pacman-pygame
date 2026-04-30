<div align="center">

# Pacman in 443 Lines of Pygame

**A complete, single-file Pacman clone built directly on Pygame: hand-laid maze, four ghosts each with their own pursuit AI, dots, power pellets, screen wrapping through the side tunnels, score tracking, and a game-over / level-reset state machine.**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.x-green.svg)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## Run it

```bash
pip install pygame
python pacman.py
```

Use the **arrow keys** to steer.  Eat the dots.  Eat a power pellet
to make the ghosts edible for a few seconds.  Don't get caught.

## What's in the file

The game is one self-contained Python module with five Pygame
`Sprite` subclasses that compose the world:

| Class            | Role |
| ---------------- | ---- |
| `Wall`           | one cell of the maze; participates in collision via a sprite group |
| `Dot`            | one collectible pellet, +10 to the score |
| `PowerPellet`    | one big pellet, +50 to the score and triggers ghost-vulnerability |
| `Pacman`         | player avatar with grid-snapping movement, mouth-arc rendering, screen-wrap through the tunnels |
| `Ghost`          | enemy with target-chasing AI; chooses the direction at every grid intersection that minimises Manhattan distance to its target |

…and four module-level helpers wire them up:

| Function       | What it does |
| -------------- | ------------ |
| `build_level()` | parses the level layout (an ASCII string) into wall + dot + power-pellet + ghost sprite groups |
| `reset_level()` | re-instantiates the world after a death or a level clear |
| `game_over()`   | draws the score, holds a few hundred ms, then exits |
| `main()`        | the standard Pygame event loop: poll input → update sprites → draw everything → flip the buffer at 60 fps |

## Design notes

A handful of small touches that come up in the source:

- **Grid-snapping movement.**  Pacman and the ghosts move in 20 px
  steps and only commit a direction change when they're aligned to a
  grid cell.  This keeps the ghosts' AI pathfinding from getting
  confused by half-steps and matches the original arcade feel.

- **Direction as a tuple.**  Directions are stored as 2-element
  velocity vectors (`UP = (0, -1)`, `RIGHT = (1, 0)`, …) rather than
  enums, so the move step is just one line of vector addition rather
  than a four-way `if`/`elif` chain.

- **Side-tunnel wrapping.**  Pacman and the ghosts both wrap from the
  far-left tunnel exit to the far-right and vice versa — a one-line
  modulo on the x coordinate against `WIDTH`.

- **Per-ghost target selection.**  Each ghost has its own target
  position (its "personality" in the original arcade game).  The AI
  is the textbook implementation: at every intersection, enumerate
  the directions that don't run into a wall and aren't a 180° flip,
  pick the one that minimises Euclidean distance to the target.
  When no valid choice exists the ghost reverses.

## Why a single file?

Game-of-life-sized projects don't need a build system, a test suite,
or a package layout.  Splitting Pacman across `entities.py`,
`world.py`, `ai.py` etc. would *increase* the cognitive cost of
reading the code, not decrease it.  443 lines top-to-bottom is the
right granularity to print out and read on paper.

## License

[MIT](LICENSE) — free for commercial, educational, and recreational use.
