# adr-aggregate-pattern: Implementation pattern of the Tetrix aggregates

**Relates to:** spec-board, spec-blocks, spec-game-loop, spec-line-clear, spec-rotate, spec-speedup
**Context:** context-tetrix-gameplay

## Context

The gameplay is a Core subdomain with true invariants: the well border,
the collision rule, the full-row rule, and the speedup rule. The state is
small: one 20 by 15 grid and one 4 by 4 shape. The game needs two
aggregates, agg-board and agg-falling-piece, with clear transaction
boundaries.

## Options

1. Domain model with small aggregates. Pro: enforces true invariants in the
   roots; fits the Core type per the pattern table. Con: more design work
   than a script for such a small game.
2. Transaction script over the grid. Pro: less code; direct port of the
   lecturer baseline. Con: spreads the full-row and collision rules across
   free functions with no enforced boundary; weak fit for a Core subdomain.
3. Event-sourced domain model. Pro: full history of each move and clear.
   Con: excess storage and replay work; the history has no business value.

## Decision

Option 1. The two aggregates use the Domain model pattern. agg-board owns
the well, the stacked cells, the clear step, and the delay. agg-falling-piece
owns the shape, the place, the move, and the turn. Policies connect them
with events.

## Consequences

- The collision and full-row rules live in the aggregate roots. Tests check
  them as contracts.
- The code stays close to the baseline functions, but each function maps to
  one aggregate command.
- Phase 3 splits tasks by aggregate and keeps upstream policy order.
