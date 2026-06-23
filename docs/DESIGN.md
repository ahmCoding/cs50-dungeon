# Design & Architecture

This document is the map of the project: where it stands today, where it is
going, which parts we touch in each step, and the reasoning behind the main
architectural decisions. Progress itself is tracked through Git tags and
commits, not in this file.

## Vision

A terminal-based, turn-based, ASCII roguelike that is genuinely fun to play in
the terminal. The long-term goal is a real, playable game — not a tech demo.
A graphical front end may follow later, so the design separates game logic
from presentation from the start.

Long-term feature ideas: multiple dungeon levels, enemies, combat, inventory,
loot, experience points, save/load, procedurally generated dungeons.

## Architectural Principles

The core idea driving the structure is a strict separation into three layers:

1. **Core (game logic).** Rules, state, and what-happens-when. Knows nothing
   about the terminal or graphics. Tiles are expressed as concepts
   (wall, floor, stairs), never as display characters.
2. **Output (presentation).** Takes the game state and makes it visible.
   Terminal today, graphics later. Swappable behind a common interface.
3. **Input.** Translates a key press (or, later, a mouse click or other event)
   into an action for the core. Also swappable.

Supporting principles applied throughout:

- **Encapsulation / information hiding** — the map exposes behaviour
  (`is_movable`, `get_tile`), never its raw grid.
- **Single point of access** — all tile reads go through one guarded method,
  so bounds checking lives in exactly one place.
- **Dependency injection** — the map can be built randomly (for play) or from a
  fixed grid (for tests); the data source is supplied from outside.
- **Determinism in tests** — the game may be random; tests never are.
- **Polymorphism over an interface** — an abstract renderer with concrete
  terminal/graphics children lets the front end be swapped without touching
  the core.

## Current State (v0.1-skeleton)

A working walking skeleton, frozen under the tag `v0.1-skeleton`:

- ASCII map with walls (`#`), floor (`.`), and a staircase goal (`>`).
- `Map` class encapsulating the grid; access via `is_movable`, `get_tile`,
  `get_game_map`, `get_map_size`.
- `Player` class holding position, with a nested `Direction` enum.
- Free functions `render`, `move`, `check_win` in `project.py`.
- Game loop in `main()` (WASD + Enter, `:q` to quit).
- pytest tests covering movement, collision, win detection, and rendering,
  using a deterministic map built via `get_map_obj_from_grid`.
- Tooling: ruff + pre-commit hooks.

## Roadmap

The next phase reshapes the core toward the three-layer design before any new
gameplay features are added. Each milestone is self-contained, kept on its own
branch, and left with all tests green.

- **M1 — Tile types as an enum.** Replace the character dictionary with a
  `Tile` enum (WALL, FLOOR, STAIRS). The core thinks in concepts, not symbols.
- **M2 — Separate presentation from the core.** Move all character/newline
  knowledge out of `Map`/`render` into a dedicated rendering layer. The core
  yields state; the renderer turns it into characters.
- **M3 — Renderer as a swappable interface.** Introduce an abstract `Renderer`
  base with a `TerminalRenderer`. Prepares for a future graphical renderer
  without building one yet.

Beyond M3: input events, then gameplay features (enemies, levels, combat, …).

## Working Method

One milestone = one branch = one merge. `main` stays stable and playable at all
times; features grow on `feature/…` or `refactor/…` branches and are merged
only when finished and tested.