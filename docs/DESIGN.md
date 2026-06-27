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

Roguelike traits we are aiming for: turn-based play (the player moves, then the
world reacts), descending through dungeon levels, growing stronger (XP),
enemies and combat, items and inventory, and — longer term — permadeath and
procedurally generated dungeons so every run differs.

## Architectural Principles

The core idea driving the structure is a strict separation into three layers,
each a sibling package under `game/`:

1. **Core (`game/core/`).** Rules, state, and what-happens-when. Knows nothing
   about the terminal or graphics. Tiles are expressed as concepts
   (wall, floor, stairs), never as display characters.
2. **Output (`game/render/`).** Takes the game state and makes it visible.
   Terminal today, graphics later. Swappable behind the abstract `Renderer`.
3. **Input (`game/input/`).** Translates a key press (or, later, another event)
   into an `Action` for the core. Swappable behind the abstract `InputSource`.

Supporting principles applied throughout:

- **Encapsulation / information hiding** — the map exposes behaviour
  (`is_movable`, `get_tile`), never its raw grid.
- **Single point of access** — all tile reads go through one guarded method,
  so bounds checking lives in exactly one place.
- **Polymorphism over an interface** — abstract `Renderer` / `InputSource`
  bases with concrete children; the front end and the controls can be swapped
  without touching the core.
- **Program to the interface** — the game loop (`play`) is typed against the
  abstractions (`Renderer`, `InputSource`), never the concrete classes.
- **Dependency injection** — collaborators are *received*, not *created*, by
  the code that uses them. `main()` builds the concrete pieces; `play()` only
  consumes them. This is what makes the loop testable.
- **Determinism in tests** — the game may be random; tests never are. The map
  can be built from a fixed grid (`get_map_obj_from_grid`).
- **Test doubles** — a `ScriptedInput` (fake `InputSource`) feeds a fixed list
  of actions, and a `NullRenderer` (null-object `Renderer`) draws nothing, so
  the real loop can be exercised in an integration test without a keyboard or
  noisy output.
- **Neutral vocabulary at the seams** — input yields an `Action`
  (`MOVE_UP`, `QUIT`, …), never a raw key; the core speaks `Direction`, never a
  key string. Key/glyph knowledge stays inside the concrete terminal classes.

## Current State (v0.6-multi-level)

The three-layer architecture is in place, the game is playable in the terminal,
reads single key presses, and spans multiple dungeon levels — frozen under the
tag `v0.6-multi-level`.

- **Core**
  - `Map` — encapsulated grid (`is_movable`, `get_tile`, `get_game_map`,
    `get_map_size`). Now also owns two positions: `start_position` (where the
    player appears) and `stairs_position`, exposed via `get_start_position`
    and `get_stairs_position`. Two factory methods build it: `get_map_obj`
    (random — rolls the stairs, avoiding the start tile) and
    `get_map_obj_from_grid` (hand-built — scans the grid for the stairs tile).
  - `Player` — position + nested `Direction` enum; `move`, `next_position`,
    and `set_position` (used to drop the player onto a new level's start).
  - `Tile` enum — WALL, FIELD, STAIRS. No display characters anywhere.
  - `Dungeon` — an ordered list of maps plus a current index. The world is no
    longer "a map" but "the current floor of a stack". CQS interface:
    `get_current_map` (query), `is_last_map` (query), `next_map` (command).
- **Output** — abstract `Renderer` (`draw`); `TerminalRenderer` owns the symbol
  map and a testable `to_string`; `NullRenderer` for tests.
- **Input** — abstract `InputSource` (`get_action() -> Action`); `Action` enum.
  `TerminalInput` is an abstract middle class holding the shared key table;
  `CanonicalTerminal` reads a line via `input()` (Enter), `RawTerminal` reads a
  single key without Enter using a `RawMode` context manager
  (`termios`/`tty` snapshot -> `setraw` -> guaranteed restore). `ScriptedInput`
  replays a fixed action list for tests. POSIX-only; a Windows source would be
  additive.
- **Glue (`project.py`)** — `move` (pure rule), `check_stairs`,
  `is_won` (won = on the last floor *and* on the stairs), and `descend`
  (advance the dungeon + place the player on the new floor's start — one
  inseparable operation). `play(g_dungeon, player, in_source, renderer)` runs
  the loop against the dungeon, fetching the current map fresh each turn.
  `main()` wires the concrete pieces and builds the `Dungeon`.
- **Tests** — units for movement, collision, win detection, rendering, key->action
  mapping; the `Dungeon` (including the "don't run past the last floor"
  boundary); `is_won` (the decisive "stairs on a non-last floor does not win");
  map stairs-finding; a property-style test (100 random maps, stairs never on
  the start tile); plus the integration test driving `play` through
  `ScriptedInput` + `NullRenderer`. All green.
- **Tooling** — pytest, ruff, pre-commit hooks. Runs from the command line.

## Roadmap

The refactoring/foundation phase is complete. From here we build *features* on
top of the stable three-layer base. Each milestone is self-contained, kept on
its own branch, merged with `--no-ff`, and tagged.

**Done**

- `v0.1-skeleton` — walking skeleton (ASCII map, movement, win, first tests).
- M1 — `Tile` enum (core thinks in concepts, not symbols).
- `v0.2-render-split` — presentation moved out of the core into `game/render/`.
- `v0.3-renderer-interface` — abstract `Renderer` + `TerminalRenderer`.
- `v0.4-input-layer` — abstract `InputSource` + `TerminalInput`, `Action`,
  dispatcher, `play()` extracted and integration-tested.
- `v0.5-event-input` — event-driven input: `RawTerminal` reads a single key
  without Enter via a `RawMode` context manager; `TerminalInput` becomes an
  abstract base shared with `CanonicalTerminal`. One keystroke = one turn.
- `v0.6-multi-level` — multiple maps behind a `Dungeon` container; stairs
  advance to the next floor; winning = reaching the stairs on the last floor;
  the player is placed on each new floor's start position.

**Later gameplay arc** (direction, not commitments)

- First enemy: a second entity that moves — entities beyond the player, turn
  order.
- Combat + HP: walking into an enemy attacks it; stats on entities.
- Items / inventory and XP.
- Treasure / goal object as an alternative win condition (a thing to pick up,
  related to loot/inventory rather than descent).
- Save / load and an end-of-run summary (serialization, aggregated state).
- Procedural dungeon generation (where map validation becomes real: exactly one
  staircase, start tile walkable); permadeath.

## Working Method

One milestone = one branch = one merge. `main` stays stable and playable at all
times; features grow on `feature/…` or `refactor/…` branches and are merged
only when finished and tested. Branches are deleted locally and remotely after
merge; milestones are marked with annotated tags, pushed separately.