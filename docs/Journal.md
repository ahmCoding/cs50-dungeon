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

## v0.7 — First Enemy (movement & turn order) (2026-06-30)

**Context.** After v0.6 only one thing acted in the game: the player. Everything
happened on a key press. An enemy is the first thing that acts on its own, so it
is the backbone of the whole vision (combat, HP, XP, loot all hang off it). This
milestone (M1) adds a second entity that moves after the player. Combat, blocking
and contact effects are out of scope — that is M2.

**Decision.**
- Extracted a `Character` parent class out of `Player`. It holds the *shared*
  movement mechanics: position, the `Direction` enum, `set_position`,
  `get_position`, `next_position`, `move`. Both `Player` and `Enemy` inherit it,
  so the shared code is written once.
- `Player` stays a thin subclass — its direction comes from outside (the key press).
- `Enemy` adds one own method `my_turn_to_move(g_map)`: collect every passable
  neighbour direction, then pick one at random; if none are free, stand still.
  The map is passed *as a method parameter* (dependency injection at the method,
  not the constructor), so the enemy holds no map state and works on any map.
- Turn order in `play`: after the player's move, the enemy takes its turn on the
  current map. This one extra step is the heart of the milestone — the first time
  the game does something without a key press.
- Renderer: `draw` now takes `list[Character]` instead of a single player. It
  stamps each entity onto the map by position. A new entity type no longer changes
  the signature — it just joins the list. The entity→char mapping
  `CHARACTER_TO_CHAR` lives in the renderer (core stays display-free) and is keyed
  on the class object, typed `dict[type[Character], str]`.
- Three property-based tests for the enemy: after a move it is never inside a wall;
  a walled-in enemy stays exactly in place (deterministic); over 100 random maps it
  always lands on a movable tile.

**Why.**
- *Abstract marks variation, not sharing.* Shared movement is real, concrete code,
  so it lives once in the parent and is inherited. Only the *direction choice*
  differs (key vs. dice). Since only the enemy rolls, that is simply one extra
  method on the enemy — no abstract slot needed yet (YAGNI).
- *"Retry until success" is only safe if a success exists.* A walled-in enemy has
  no free neighbour, so rolling until movable would loop forever. So: collect the
  free neighbours first, choose among them, stand still if the list is empty. This
  also produces exactly the data a future "chase the player" enemy will need.
- *Open/closed for the renderer.* Passing a list of drawables instead of one fixed
  player argument means new entity types are added to the list, not to the signature.
- *Class object as dict key, not its name string.* Keying on `__class__.__name__`
  ("Enemy") breaks silently on a class rename — the string drifts away from the
  class. Keying on the class object itself moves with the rename and is checked
  statically.

**Lesson.**
- A green test can be worse than a red one. One enemy test moved the enemy on map A
  but asserted against map B; it passed by luck while testing nothing real. A red
  test shouts; a false-green whispers "all fine" and lies.
- Changing a public signature means updating *all* callers in the same step — tests
  included. After the renderer and `play` signatures changed, the suite went red
  because the test call sites still used the old shape. The green net matters most
  exactly when you reshape an interface.
- The real acceptance test of a milestone is running it, not only a green suite.
  Playing the game confirmed the enemy moves after each turn — and surfaced the
  scroll issue below.

**Rejected.**
- Putting the enemy's move logic as a function in `project.py`. That mixes three
  concerns: how an entity chooses (enemy), the move mechanics (Character), and
  wiring the turn into the loop (play). Each stays in its own place.
- Giving the enemy the map in its constructor / as instance state. The caller hands
  in the current map at move time, so the enemy owns no map.
- An abstract `choose_direction` slot in `Character`. With one enemy type and no
  second implementation, that is premature abstraction.
- Random spawn position for the enemy. It needs "forbidden zones" (not a wall, not
  on the player, not on the stairs) and a real owner for the enemy's position — a
  separate concern. A fixed spawn proves M1; the rest is the next milestone.

**Parked (new).**
- Enemies belong to a map/floor. Today a single enemy is passed into `play` and
  carries across floors at the same coordinates. Enemies should be owned per map,
  with a valid random spawn (forbidden zones). → next milestone (before combat).
- Clear the terminal between frames — the view scrolls down instead of redrawing
  in place.

---

## v0.8 — Enemy Spawn (per-floor ownership) (2026-07-01)

**Context.** After v0.7 the enemy was an orphan. One `Enemy` was hardcoded at
`(1, 3)` in `main()`, passed into `play`, and floated across floors at the same
coordinates. The player, by contrast, was already owned by the map: the map holds
`start_position`, and `descend` drops the player onto the next map's start. This
milestone removes that asymmetry — enemies get a real owner (the floor) and a valid
*random* spawn — so combat (M2) can rest on enemies that properly exist per floor.
Combat itself stays out of scope.

**Decision.**
- New `Level` class: it owns a `Map` **plus its own** `list[Enemy]`. A level cannot
  exist without its enemies.
- `Level.get_level_object(g_map, enemy_count=1)` — a factory that **spawns the
  enemies itself** from the map. No ready-made enemy list is handed in.
- New `Map` query `get_free_map_positions()` → a `set` of spawnable tiles: `FIELD`
  tiles that are not the start position. Walls and stairs fall out on their own,
  because they are not `FIELD`.
- `Dungeon` now holds `list[Level]` instead of `list[Map]`
  (`get_current_level` / `next_level` / `is_last_level`). The ordered-index model is
  unchanged.
- `play` no longer receives an `enemy` argument; it reads the enemies from the
  current level, and `Level.move_enemies()` moves them (the owner moves its own
  enemies — tell, don't ask). The orphan `Enemy(1, 3)` in `main()` is gone.
- Tests: free-position invariants (start and stairs are never returned; every
  returned tile is movable, over 100 random maps); the level's enemy count; and
  **every spawned enemy stands on a free field**.

**Why.**
- *Ownership follows lifetime.* An enemy is born with its floor and dies with it, so
  the floor owns it. The player outlives every single floor — he walks through the
  whole dungeon — so no floor owns him; he lives above them and is only *moved* onto
  each floor's start. "On a level" is not "belongs to a level."
- *One named object beats parallel lists or a dict.* Two lists (maps + enemies)
  coupled by index can silently drift apart — a false state waiting to happen. A dict
  keeps the binding but throws away the order the `Dungeon` needs and stays an
  anonymous container. A named `Level` keeps the order, makes "a map without its
  enemies" unconstructable, and grows cleanly (treasure next) without reshaping a
  tuple.
- *Born together, never broken.* The factory spawns from *this* map's free tiles, so
  an enemy can never land on geometry it does not belong to. The broken state is not
  guarded against — it is impossible to build. Same idea as the map factory rolling
  its own stairs.
- *Collect, then choose — never roll until free.* Spawning asks the map for the set
  of free tiles and samples from it, so a full or tiny map yields "no enemy" at once
  instead of an endless retry. Same shape as the enemy's own move logic.

**Lesson.**
- *Arbitrary is not random.* `set.pop()` is documented as removing an *arbitrary*
  element, not a random one. For tuples of small ints the hash is stable, so `pop`
  returns the same order on every run — enemies spawned on identical tiles each game.
  The right tool was `random.sample`, which draws N distinct positions in one call. A
  non-promise is not a promise of randomness.
- *A false-green whispers, again.* A first spawn loop used `enumerate` and unpacked
  `(index, position)` as the enemy's `(x, y)`, so every enemy sat at `x = 0, 1, 2…`
  and `y = the whole tuple`. All tests stayed green because they only **counted**
  enemies, never checked **where** they stood. The missing mirror test — every
  spawned enemy stands on a free field — is exactly what caught it once written.
- *The IDE is not the source of truth.* An import written as `core.level` (instead of
  `game.core.level`) ran fine in PyCharm, because `game/` is marked there as a Sources
  Root. From the command line and CI it was a hard `ModuleNotFoundError` — the whole
  suite could not even be collected. Red was pushed while the IDE showed green. Ruff
  cannot catch this; only *running the tests* does.

**Rejected.**
- The map owning the live `Enemy` objects. That would put mutable gameplay state into
  core geometry. The map stays pure geometry; it only *offers* free positions.
- Two parallel lists (`list[Map]` + `list[list[Enemy]]`) coupled by index. Easy to
  desync — a false state made *possible* instead of impossible.
- A plain dict `{Map: [Enemy]}`. It keeps the binding but loses the `Dungeon`'s order
  and never grows into a real domain object.
- Handing a ready-made enemy list into the level factory. Then the spawn logic lives
  outside again — a fresh orphan — and enemies could be built on the wrong map's
  geometry.
- Fixing the player's floor-1 start in this milestone. That is a separate (player)
  concern → parked.

**Parked.**
- The player's start on floor 1 is still hardcoded `Player(1, 1)` in `main()`; it
  matches the map start only by coincidence. It should be read from the first level's
  map start, the way `descend` already does it — one source of truth. Behaviour-
  preserving today → a small `refactor/`, no version tag.
- A pre-push / CI guard that runs the tests, so the IDE can no longer wave a red push
  through as green.
- Clear the terminal between frames — the view still scrolls instead of redrawing in
  place. (carried over)
- A `Game` aggregate that holds player + dungeon and owns `play` — now designable,
  since floor ownership is clean.
- Combat / contact effect (M2): what happens when player and enemy meet.