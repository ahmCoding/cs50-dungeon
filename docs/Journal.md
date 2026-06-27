# Development Journal — cs50-dungeon

This file tells the **story** of the project: not only *what* changed, but
*why* we decided it, and which other options we said no to.

It is different from the other two documents:

- **README.md** — the shop window. What the game is, the main ideas, how to run it.
- **docs/DESIGN.md** — the blueprint. How the code looks *right now*.
- **docs/JOURNAL.md** (this file) — the journey. One entry per milestone,
  written while the reasons are still fresh.

Each entry uses the same small format:

- **Context** — what was the situation and the problem?
- **Decision** — what did we choose?
- **Why** — the reason, and the principle behind it.
- **Rejected** — the options we did *not* take, and why.

The entries below from `v0.1` to `v0.4` are a backfill, written together in one
go. From `v0.5` on, each milestone adds its own entry on its own branch.

---

## v0.1 — Walking Skeleton (2026-06-23)

*Tag: `v0.1-skeleton`*

**Context.** The project was an empty folder. I wanted something playable
*fast* (for motivation), but I did not want my old habit: build quick, but
rigid, and impossible to extend.

**Decision.** Build a *walking skeleton* — a thin but complete slice through the
whole game: a `Map` (a grid as a list of lists), a `Player` with a position and
a nested `Direction` enum (each direction is a delta tuple), free functions
`render` / `move` / `check_win` in `project.py`, a game loop in `main()`, and
the first pytest tests. The grid is never touched from outside directly; every
read goes through methods like `is_movable`, `get_tile`, `get_game_map`.

**Why.** A walking skeleton runs from day one, so I stay motivated, but it also
forces the full end-to-end shape early instead of bolting it on later.
Hiding the grid behind methods is the *Single Point of Access* idea: the
bounds check lives in exactly one place. For tests, a `from_grid` factory builds
a fixed map, so the game can be random later but the tests never are
(*determinism in tests*).

**Rejected.** Writing all the logic in one big loop first and refactoring later.
This is exactly the "fast but rigid" path I wanted to leave behind — clean
structure up front is the whole point of this project.

---

## M1 — Tile Enum (2026-06-24)

*Between `v0.1` and `v0.2` (refactor branch `refactor/tile-enum`)*

**Context.** The map stored display characters directly (`'#'`, `'.'`, `'>'`).
The core "thought in symbols". A wall *was* a `#`.

**Decision.** Replace the character dictionary with a `Tile` enum
(`WALL`, `FIELD`, `STAIRS`) using `auto()`. Keep one module-level constant
`TILE_TO_CHAR` for the translation from tile to character.

**Why.** The core should think in *concepts*, not in screen symbols. This is the
first small cut of *Separation of Concerns*: meaning (`Tile.WALL`) is now a
different thing from how it looks (`'#'`). I used `auto()` because the integer
values do not matter — only the identity of each tile does.

**Rejected.** Keep raw strings (simple, but the core stays glued to the
display). Use plain integer constants (no type safety, no shared namespace,
easy to mix up).

---

## v0.2 — Presentation Split (2026-06-24)

*Tag: `v0.2-render-split` (Milestone M2)*

**Context.** Even with the `Tile` enum, the translation tile → character still
lived in `project.py`, right next to the core logic. Meaning and presentation
were still in the same place.

**Decision.** Move *all* display knowledge — `TILE_TO_CHAR`, the player
character, and the string building — into a new package `game/render/`. The
core package `game/core/` becomes completely free of display characters.

**Why.** *Separation of Concerns* at the package level. The core gives *state*;
the render layer turns that state into characters. This is what makes a future
graphical front end possible later *without* touching the game logic. The
package layout now shows the architecture by itself.

**Rejected.** Leave the translation in `project.py` (short-term easier, but the
core would never be truly free). An early wrong cut put `render/` in a place
that blurred the core/output line, and a `render/render.py` name repeated
itself — both fixed, because the folder names should carry the design clearly.

---

## v0.3 — Renderer Interface (2026-06-24)

*Tag: `v0.3-renderer-interface` (Milestone M3)*

**Context.** There was exactly one way to draw the game: the terminal. But the
long-term vision wants swappable front ends (later maybe graphics).

**Decision.** Add an abstract base `Renderer(ABC)` with an abstract method
`draw(g_map, player)`. The concrete `TerminalRenderer` owns the symbol map as
class attributes and has a testable `to_string()` method, kept separate from
the side-effecting `draw()` that actually prints.

**Why.** *Polymorphism over an interface* and *program to the interface*: the
game loop depends on the abstract `Renderer`, not on any concrete class.
Splitting `to_string()` (pure, returns a string) from `draw()` (prints) means I
can test the rendering by checking a returned string, with no need to capture
stdout.

**Python note.** `abc` enforcement happens at instantiation *runtime*, not at
compile time (different from C++/Java). Class-body attributes act like
`static const` members shared by all instances.

**Rejected.** Build the graphical renderer now. *YAGNI* — at this point I only
need the *seam* (the interface), not a second implementation.

---

## v0.4 — Input Layer (2026-06-25)

*Tag: `v0.4-input-layer` (Milestone M4)*

**Context.** `main()` read keys with `input()` and decided what to do inline.
The loop could not be tested, and key knowledge was mixed into the loop.

**Decision.** Add a `game/input/` package: an abstract `InputSource(ABC)` with
`get_action() -> Action`; an `Action` enum (`MOVE_*`, `QUIT`, `NONE`); a
concrete `TerminalInput` that owns a `KEY_TO_ACTION` map; and a `ScriptedInput`
test double. `move()` now takes a `Direction` directly, and an
`ACTION_TO_DIRECTION` table does the dispatch. The game loop is taken out of
`main()` into an injectable function `play(g_map, player, in_source, renderer)`.

**Why.** *Dependency Injection*: `play()` *receives* its parts, while `main()`
*builds* them. *Neutral vocabulary at the seams*: input gives back an `Action`,
never a raw key; the core speaks `Direction`, never a key string. Because the
loop is now an injectable function typed against the two interfaces, a real
*integration test* can drive the true `play()` with `ScriptedInput` and a
`NullRenderer` — no keyboard, no noisy output.

**Lesson.** A first version of the loop test re-built the dispatch logic *inside
the test*. That tests a copy, not the real code. The fix was to extract the loop
so the test runs the production path.

**Rejected.** Keep the loop in `main()` (then I must fake stdin/stdout to test
it). Pass raw keys into the core (that would glue the core to the terminal).

---

## v0.5 — Event Input (single key, raw mode) (2026-06-26)

*Tag: `v0.5-event-input` (milestone: event-driven input)*

**Context.** Until v0.4 the player typed a letter and then pressed Enter
(canonical mode). For a game this is slow — one move needs two key presses. The
goal of v0.5: **one key press = one turn**, with no Enter. The game stays
turn-based (one move per press; auto-repeat on hold is left for later).

**Decision.** Add a new `InputSource` that reads a single *raw* byte from the
terminal, using only the standard library (`termios` + `tty`). The low-level
key code is locked inside this new class; the loop, core, and renderer do not
change. In detail:

- `TerminalInput` becomes an abstract *middle* class (child of `InputSource`,
  parent of the concrete terminal classes) and holds the shared
  `STR_TO_ACTION` table.
- The old line-based class is renamed `CanonicalTerminal` — an honest name, it
  runs in canonical mode.
- The new `RawTerminal` reads one byte in raw mode.
- The raw on/off logic is pulled out into its own context manager `RawMode` in
  `game/input/raw_mode.py`. `RawTerminal` *uses* it (composition); it does not
  *inherit* it.

**Why.**

- *Stdlib over a library* (`termios`/`tty` instead of e.g. `readchar`): the goal
  of the whole project is learning. Building raw mode by hand shows the terminal
  from the inside, and keeps `requirements.txt` empty (zero dependencies).
- *Snapshot, not guess*: `RawMode.__enter__` saves the current terminal settings
  with `tcgetattr` and restores exactly them with `tcsetattr`. It does not reset
  to a "default" — it puts back whatever was there before. This is robust for any
  starting state and does not depend on the Python version.
- *Guaranteed cleanup*: a `with` block is a `try/finally` in disguise. Even if
  the read raises (or the program crashes mid-read), the terminal is set back to
  normal. Without this, a crash would leave the shell broken (no Enter, no echo).
- *Information hiding through a per-call lifecycle*: raw mode is switched on and
  off *inside* each `get_action()` call. So `main()` never learns that a raw mode
  exists — it only sees an `InputSource`. The contract stays at one method
  (`get_action`); no `start()`/`stop()` is needed. This is cheap here because the
  game is turn-based (a few reads per second, not thousands).
- *Single Responsibility / composition over inheritance*: `RawMode` knows only
  "switch the tty to raw and back"; `RawTerminal` knows only "give the next
  Action". The input class *has* a mode switch instead of *being* one.
- *Three honest levels*: `InputSource` (neutral contract, no terminal knowledge)
  → `TerminalInput` (reads characters from the keyboard, holds the table) →
  `CanonicalTerminal` / `RawTerminal` (differ only in *how* they read). Shared
  knowledge lives in the shared parent, not copied into the siblings (DRY).

**Raw vs. cbreak.** Both modes give single bytes with no Enter. The only real
difference is `Ctrl+C`: cbreak keeps it as a kill signal, raw delivers it as a
plain byte. We chose **raw** on purpose — the game is left with `q` as the exit,
and we want full control of the keys; `Ctrl+C` is not needed as an escape. This
has nothing to do with cross-platform support (both are POSIX only).

**Windows.** `termios` is POSIX only, so `RawTerminal` runs on Linux and macOS,
not on Windows. We leave the door open: a future `WindowsInput` (using `msvcrt`)
would be a *new* `InputSource`, added next to the others — no rewrite, because
the seam already sits in the right place. We do not write untested Windows code
now (YAGNI, and never ship code you cannot run).

**Rejected.**

- A small library like `readchar` (one line, works everywhere at once) — it
  would hide exactly the part we want to learn, and add a dependency.
- Arrow keys — they send multi-byte escape sequences; we keep single letters
  (`w/a/s/d/q`), so this complexity is avoided. (This is a separate choice from
  raw vs. cbreak.)
- Replacing `CanonicalTerminal` with the new class — it is still a valid,
  portable, easy-to-test `InputSource` and a natural fallback. Additive design.
- A session lifecycle in `main()` (raw on at start, off at end) — it would leak
  a detail of `RawTerminal` to the caller and force a bigger interface.

---
## v0.6 — Multiple Levels (2026-06-27)

*Tag: `v0.6-multi-level`*

**Context.** Until now the whole game ran on *one* map. The long-term vision
needs many floors. This was the smallest, most self-contained next step: the
loop barely changes, and it lays the foundation that random generation and
enemies will later build on. Stairs already existed as a tile but only meant
"you win". With more than one floor, "reached the stairs" and "the game is over"
are no longer the same event.

**Decision.**

- A new core type `Dungeon` holds an ordered list of maps plus a current index.
  Its public interface is three methods, split by CQS: `get_current_map`
  (query), `is_last_map` (query), `next_map` (command, advances the index).
- Winning is no longer a property of a tile. It is a property of the game state:
  you win when you reach the stairs *and* there is no next floor. `is_won` checks
  exactly that (`is_last_map()` and on the stairs). The old `check_win` /
  `_win_tile` are deleted.
- On descending, the player is moved to a fixed start position that the map now
  owns. `Map` gains `start_position` and `stairs_position` (+ getters); the
  random factory rolls the stairs (never on the start tile), the grid factory
  scans the grid for the stairs tile. `Player` gains `set_position`.
- The level change is extracted into one function `descend(dungeon, player)`:
  advance the floor *and* place the player on the new start — together,
  inseparably. `play` now runs on the `Dungeon`, fetching the current map fresh
  each turn instead of holding it.

**Why.**

- *One concept per milestone.* The branch does exactly one thing: introduce
  floors. A `Game` aggregate was tempting here but was pushed back, because it
  was justified by *future* features (enemies, difficulty) we do not have yet.
- *CQS, and "two methods are easier to merge into one than one is to split".*
  Advancing (command) and asking "is there a next floor?" (query) are separate,
  so the loop can safely *ask* before it *acts*. This is what makes the
  "ask first, then descend" order in `play` possible.
- *Win is state, not a tile.* Pressing two meanings into the stairs tile (next
  level vs. you win) would force the code to ask "which floor am I on?" to know
  what the stairs mean. Splitting them keeps the stairs with a single meaning:
  "go to the next floor". Winning falls out when "next" points to nothing.
- *Information hiding.* The dungeon owns its index and list; `play` never sees
  `len(...) - 1`. The map owns its start and stairs positions; `play` never
  hardcodes coordinates — it asks the map.
- *Make the bad state impossible, don't check for it.* `descend` bundles "switch
  map" and "move player" so a caller cannot do one without the other (which was
  exactly an earlier bug: changing the map left the player on stale coordinates).
- *The map owns its start position*, not the player. "Where do you start on this
  floor" is knowledge about the level's geometry. Putting it on the map also
  leaves the door open for later random generation to keep that tile clear.
- *One source of truth.* `play` does not cache the current map; it calls
  `get_current_map()` each turn. After a descend the index is the only place the
  "where am I" state lives.
- *Property-style test for random code.* The rule "the stairs never land on the
  start tile" is checked by building 100 random maps and asserting the invariant
  on each, rather than fixing a seed and asserting one position. This needs no
  change to the production code (no seed parameter to inject) and tests the
  *rule*, not one example. The trade-off: it is probabilistic, not a proof.

**Rejected / parked.**

- *Treasure / goal object as the win condition.* It felt cooler than "reach the
  stairs", but a pick-up object with its own position and state belongs with
  loot/inventory, not with "multiple floors". Parked as its own future
  milestone.
- *A `Game` aggregate that owns player + dungeon and holds `play`.* A real and
  probably good idea — but a separate concern from multi-level, and better
  designed *after* enemies exist, when we know what it must really hold.
- *Up/down stairs and directional travel* (top stairs go down, bottom stairs go
  up). Deferred; two floors and one direction are enough to prove the seam.
- *Random spawn position on a new floor.* Would immediately require "forbidden
  zones" (don't spawn in a wall / on the stairs). A fixed start position is the
  cheapest thing that proves the transition. Random can come additively later.
- *Map validation* (exactly one staircase, start tile walkable, stairs present).
  Not needed while *I* hand-build every grid — I am the reliable source. It
  becomes real with **procedural generation**, where a machine builds grids that
  can truly be broken. Added at that seam, then.
- *Factory clean-up of the `None` default.* `Map.__init__` takes
  `stairs_position=None` so one constructor can serve both factories (the random
  one sets it right after; the grid one passes it in). The `None` is a
  *transient* construction state, never a valid "floor without stairs". But the
  getter's type (`tuple | None`) currently advertises a state that never reaches
  a caller. Planned as its own small `refactor/` step: move the rolling into the
  random factory so `__init__` always *requires* a real position, the type
  becomes `tuple[int, int]`, and the getter can no longer return `None`. Also on
  the radar: declaring the whole map state in one place (e.g. `@dataclass`).

---
## refactor/factory-cleanup — Constructor takes a real stairs position (2026-06-27)

**Context.** After v0.6, `Map.__init__` accepted `stairs_position: tuple | None`.
When `None` came in, the constructor itself rolled a random stairs position. The
side effect lived in the getter: `get_stairs_position()` was typed `tuple | None`,
so it advertised a "floor without stairs" state to every caller. That state never
actually happened — the `None` was only a transient moment during construction.
The type was lying about reality.

**Decision.** Move the rolling out of the constructor into the factory.
- A private static helper `_create_2d_tile_grid` now builds the grid *and* rolls
  the stairs position, returning both.
- `get_map_obj` (random) calls it and hands a finished position to the constructor.
- `get_map_obj_from_grid` scans the given grid for the `STAIRS` tile and hands the
  found position in.
- `__init__` now *requires* `stairs_position: tuple[int, int]` — no `None`.
- The getter is now typed `tuple[int, int]` and carries no defensive assert.
Cleaned up in the same pass: dead post-construction writes in the grid factory
(`tmp_obj._height = …` etc.) were removed — the constructor already sets those.
And `_stairs_tile` is no longer stored per instance; `get_stairs_tile()` is now a
`@staticmethod` returning the constant `Tile.STAIRS`.

**Why.** *Make illegal states unrepresentable instead of checking for them.* Once
both factories must produce a real position and the constructor demands one,
`None` can never reach the field — so the type can honestly say `tuple[int, int]`
and no runtime check is needed. *Single Responsibility*: the constructor stores
state, the factory builds it; the rolling logic now lives where it belongs.
*Encapsulation*: nothing writes the Map's private fields from outside anymore.
*Constant ≠ instance state*: a value identical for every Map (`Tile.STAIRS`) does
not belong in `__init__`; a `@staticmethod` says that plainly while keeping the
Map as the single place that knows which tile means "goal" (so `project.py` still
does not need to import `Tile`).

**Lesson.** The same line — `assert x is not None` — was right in one place and
dead in another. In the grid-scan loop, `None` is a real "not found yet" sentinel,
so the assert both checks a reachable state and narrows the type for the checker.
In the getter, `None` was unreachable after the refactor, so the identical assert
guarded nothing. Whether a guard means anything depends on whether the guarded
state can actually be reached.

**Rejected.** A version tag (e.g. `v0.7`) for this branch. Tags mark milestones
with new *behaviour*; this refactor changes none — all 36 tests stayed green and
untouched, which is the proof. The `--no-ff` merge boundary plus this entry record
the story without diluting the version sequence. Also rejected: sentinel values
like `(-1, -1)` for "not found yet" in the grid scan. The `None`-before-loop
pattern reads clearer and the closing assert narrows the type cleanly; sentinels
would only be uglier.

---

*Next entry: `v0.7` (or the next milestone) — added on its own branch when done.*