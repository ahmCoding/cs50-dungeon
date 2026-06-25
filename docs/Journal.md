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

*Next entry: `v0.5` — event-driven input (`RawTerminalInput`). Added on its own
branch when the milestone is done.*