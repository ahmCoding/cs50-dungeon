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

## Current State (v0.4-input-layer)

The three-layer architecture is in place and the game is playable in the
terminal, frozen under the tag `v0.4-input-layer`:

- **Core** — `Map` (encapsulated grid; `is_movable`, `get_tile`,
  `get_game_map`, `get_map_size`), `Player` (position + nested `Direction`
  enum), `Tile` enum (WALL, FIELD, STAIRS). No display characters anywhere.
- **Output** — abstract `Renderer` (`draw(g_map, player)`); `TerminalRenderer`
  owns the symbol map (`TILE_TO_CHAR`, `PLAYER_CHAR`) and a testable
  `to_string`, with a thin `draw` that prints it; `NullRenderer` for tests.
- **Input** — abstract `InputSource` (`get_action() -> Action`); `Action` enum
  (`MOVE_*`, `QUIT`, `NONE`); `TerminalInput` owns the key map and reads via
  `input()`; `ScriptedInput` replays a fixed action list for tests.
- **Glue (`project.py`)** — `move` (a pure rule taking a `Direction`),
  `check_win`, an `ACTION_TO_DIRECTION` dispatch table, and the extracted
  `play(g_map, player, in_source, renderer)` loop. `main()` wires up the
  concrete terminal pieces and calls `play`.
- **Tests** — units for movement, collision, win detection, rendering
  (`to_string`), and key→action mapping (parametrized); plus an *integration*
  test that drives the real `play` loop through `ScriptedInput` + `NullRenderer`.
- **Tooling** — pytest, ruff, pre-commit hooks. All tests green; runs from the
  command line, not just the IDE.

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

**Next**

- **v0.5 — Event-driven input (immediate next).** A new `InputSource` that
  reads a *single key press without Enter*, so one keystroke = one turn. The
  game stays turn-based (one move per press; auto-repeat while a key is held is
  deferred as a later option). The OS-specific raw-key reading
  (`termios`/`tty`, or a small lib such as `readchar`) is isolated entirely
  inside this new class — the loop, core, and renderer are untouched. This is
  the first real payoff of the input abstraction.

**Later gameplay arc** (direction, not commitments)

- Stairs → next level: multiple maps, a depth counter, map switching.
- First enemy: a second entity that moves — entities beyond the player, turn
  order.
- Combat + HP: walking into an enemy attacks it; stats on entities.
- Items / inventory and XP.
- Save / load and an end-of-run summary (serialization, aggregated state).
- Procedural dungeon generation; permadeath.

## Working Method

One milestone = one branch = one merge. `main` stays stable and playable at all
times; features grow on `feature/…` or `refactor/…` branches and are merged
only when finished and tested. Branches are deleted locally and remotely after
merge; milestones are marked with annotated tags, pushed separately.