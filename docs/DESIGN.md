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
  consumes them. This is what makes the loop testable. The same idea applies at
  method level: `Enemy.my_turn_to_move(g_map)` receives the current map instead
  of storing one.
- **Ownership follows lifetime** — a thing is owned by whatever shares its
  lifetime. Enemies are born with a floor and die with it, so the `Level` owns
  them; the player outlives every floor, so no floor owns him — he is only
  *placed* onto each floor's start.
- **Make illegal states unconstructable** — instead of checking for a bad state,
  arrange the code so it cannot be built. A `Level` spawns its own enemies from
  its own map, so an enemy on the wrong geometry cannot exist.
- **Determinism in tests** — the game may be random; tests never are. The map
  can be built from a fixed grid (`get_map_obj_from_grid`).
- **Test doubles** — a `ScriptedInput` (fake `InputSource`) feeds a fixed list
  of actions, and a `NullRenderer` (null-object `Renderer`) draws nothing, so
  the real loop can be exercised in an integration test without a keyboard or
  noisy output.
- **Neutral vocabulary at the seams** — input yields an `Action`
  (`MOVE_UP`, `QUIT`, …), never a raw key; the core speaks `Direction`, never a
  key string. Key/glyph knowledge stays inside the concrete terminal classes.

## Current State (v0.8-enemy-spawn)

The three-layer architecture is in place, the game is playable in the terminal,
reads single key presses, spans multiple dungeon levels, and now has autonomous
enemies that are owned per floor and spawn at valid random positions — frozen
under the tag `v0.8-enemy-spawn`.

- **Core**
  - `Character` — the parent of every moving entity. Holds the *shared* movement
    machinery: the position (`x`, `y`), a nested `Direction` enum, and
    `move`, `next_position`, `set_position`, `get_position`. Shared, concrete
    code — written once and inherited.
  - `Player` — a thin `Character` subclass. Its direction comes from outside
    (the key press); it adds no movement logic of its own.
  - `Enemy` — a `Character` subclass that acts on its own. `my_turn_to_move(g_map)`
    collects every passable neighbour direction, picks one at random, and stands
    still when none are free. The map is passed *as a method argument*, so the
    enemy holds no map state and runs on any map.
  - `Map` — encapsulated grid (`is_movable`, `get_tile`, `get_game_map`,
    `get_map_size`). Owns two positions: `start_position` (where the player
    appears) and `stairs_position`, exposed via `get_start_position` and
    `get_stairs_position`. Two factory methods build it: `get_map_obj`
    (random — rolls the stairs, avoiding the start tile) and
    `get_map_obj_from_grid` (hand-built — scans the grid for the stairs tile).
    New in v0.8: `get_free_map_positions()` returns a `set` of spawnable tiles —
    every `FIELD` that is not the start position. Walls and stairs drop out on
    their own because they are not `FIELD`. This is pure geometry: the map
    *offers* free tiles, it does not choose among them.
  - `Tile` enum — WALL, FIELD, STAIRS. No display characters anywhere.
  - `Level` — a floor: it owns one `Map` **plus its own** `list[Enemy]`. The
    factory `get_level_object(g_map, enemy_count=1)` spawns the enemies itself,
    drawing `enemy_count` distinct free tiles from the map via `random.sample`
    (capped at the number of free tiles). `get_map` and `get_enemies` expose the
    contents; `move_enemies()` moves every enemy of the floor (the owner moves
    its own enemies). A level cannot exist without its enemies, and an enemy
    cannot land on geometry it does not belong to.
  - `Dungeon` — an ordered list of **levels** plus a current index. The world is
    "the current floor of a stack". CQS interface: `get_current_level` (query),
    `is_last_level` (query), `next_level` (command).
- **Output** — abstract `Renderer` (`draw`); `TerminalRenderer` owns the symbol
  map and a testable `to_string`; `NullRenderer` for tests. `draw` takes the map
  and a `list[Character]`, stamping each entity onto the map by position — a new
  entity type joins the list instead of changing the signature (open/closed).
  The entity→glyph table `CHARACTER_TO_CHAR` is keyed on the **class object**
  (`type(character)`), typed `dict[type[Character], str]`, so a missing entry
  fails loudly rather than a rename drifting silently.
- **Input** — abstract `InputSource` (`get_action() -> Action`); `Action` enum.
  `TerminalInput` is an abstract middle class holding the shared key table;
  `CanonicalTerminal` reads a line via `input()` (Enter), `RawTerminal` reads a
  single key without Enter using a `RawMode` context manager
  (`termios`/`tty` snapshot -> `setraw` -> guaranteed restore). `ScriptedInput`
  replays a fixed action list for tests. POSIX-only; a Windows source would be
  additive.
- **Glue (`project.py`)** — `move` (pure rule), `check_stairs`,
  `is_won` (won = on the last floor *and* on the stairs), and `descend`
  (advance the dungeon + place the player on the new floor's map start — one
  inseparable operation). `play(g_dungeon, player, in_source, renderer)` runs the
  loop against the dungeon: it draws the current map together with the player and
  the current level's enemies, moves the player, handles descent, then lets the
  current level move its enemies. Enemies are read from the level, never passed
  in. `main()` wires the concrete pieces: it builds the maps, wraps each in a
  `Level`, stacks them in a `Dungeon`, and starts `play`.
- **Tests** — units for movement, collision, win detection, rendering, key->action
  mapping; the `Dungeon` (including the "don't run past the last floor"
  boundary); `is_won` (the decisive "stairs on a non-last floor does not win");
  map stairs-finding; property-style tests over 100 random maps: stairs never on
  the start tile, every free position is movable, and the start and stairs tiles
  are never returned as free. Enemy behaviour: after a move it is never inside a
  wall, a walled-in enemy stays put (deterministic), and over 100 random maps it
  always lands on a movable tile. Level spawning: the enemy count is honoured,
  and every spawned enemy stands on a free field. Plus the integration test
  driving `play` through `ScriptedInput` + `NullRenderer`. All green.
- **Tooling** — pytest, ruff, pre-commit hooks. The command line and CI are the
  source of truth, not the IDE.

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
- `v0.7-first-enemy` — a `Character` parent shared by `Player` and a new `Enemy`
  that moves on its own after each player turn; the renderer takes a list of
  drawables keyed on the class object.
- `v0.8-enemy-spawn` — enemies are owned per floor by a new `Level` (map + its
  enemies); the `Dungeon` holds levels; enemies spawn at valid random positions
  (not wall, not stairs, not start) via a `Map` free-tiles query. The hardcoded
  orphan enemy is gone.

**Later gameplay arc** (direction, not commitments)

- Combat + HP: walking into an enemy attacks it; stats on entities. Next.
- Items / inventory and XP.
- Treasure / goal object as an alternative win condition (a thing to pick up,
  related to loot/inventory rather than descent).
- A `Game` aggregate holding player + dungeon and owning `play` — designable now
  that per-floor ownership is clean.
- Save / load and an end-of-run summary (serialization, aggregated state).
- Procedural dungeon generation (where map validation becomes real: exactly one
  staircase, start tile walkable); permadeath.

**Known small cleanups (parked)**

- The player's floor-1 start is still hardcoded in `main()` and matches the map
  start only by coincidence; it should be read from the first level's map start,
  as `descend` already does — one source of truth. Behaviour-preserving today.
- Clear the terminal between frames — the view scrolls instead of redrawing.
- A pre-push / CI guard that runs the tests, so the IDE cannot wave a red push
  through as green.

## Working Method

One milestone = one branch = one merge. `main` stays stable and playable at all
times; features grow on `feature/…` or `refactor/…` branches and are merged
only when finished and tested. Branches are deleted locally and remotely after
merge; milestones are marked with annotated tags, pushed separately.