# req-line-clear: Remove full rows

**Master:** [Requirements](README.md)
**Priority:** Must
**Context:** context-tetrix-gameplay

## Statement

The game must remove each full row when a block lands and move each row above down.

## Acceptance criteria

- Given one full row after a block lands, when the game updates the well, then the full row
  disappears and each row above moves down by one row.
- Given two full rows after a block lands, when the game updates the well, then both full rows
  disappear and each row above moves down by two rows.

## Notes

The lecturer baseline lacks the removeLine function. This requirement restores that behavior.
Phase 4 owner: SV2.
