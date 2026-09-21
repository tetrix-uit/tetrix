# Requirements: Tetrix falling-block game

**Change:** [change-initial](../../../changes/change-initial/README.md)

## Business need

Players need the Tetrix falling-block game in apps/tetrix. They need falling blocks, player
movement, rotation, line clearing, square display, and higher speed after each cleared line. They
need this game to play and enjoy the falling-block challenge.

## Scope

- In scope: A bordered game well.
- In scope: Falling block shapes.
- In scope: Timed falling, left/right/down movement, and quit on demand.
- In scope: Clearing of full rows with rows above that fall down.
- In scope: Square border and square blocks.
- In scope: Rotation of the falling block.
- In scope: Higher falling speed after each cleared line.
- Out of scope: Sound.
- Out of scope: Score storage.
- Out of scope: Menus.
- Out of scope: Network play.

## Domain

| Subdomain | Type | Context | Actors | Events |
| --- | --- | --- | --- | --- |
| Tetrix gameplay | Core | context-tetrix-gameplay | Player | Falling block landed, Full row cleared, Falling speed increased |

## Teardown requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| [req-screen](req-screen.md) | The game must draw the bordered game well. | Must |
| [req-blocks](req-blocks.md) | The game must draw the falling block shapes. | Must |
| [req-falling](req-falling.md) | The game must fall on a timer, move on player demand, and quit on demand. | Must |
| [req-line-clear](req-line-clear.md) | The game must remove full rows and move rows above down. | Must |
| [req-square-ui](req-square-ui.md) | The game must draw the border and the blocks with square cells. | Must |
| [req-rotate](req-rotate.md) | The game must rotate the falling block on player demand. | Must |
| [req-speedup](req-speedup.md) | The game must increase the falling speed after each cleared line. | Must |

## Acceptance

The game draws the bordered well and the falling blocks with a square display. It moves and
rotates blocks on player demand, clears full rows, and falls faster after each cleared line.
