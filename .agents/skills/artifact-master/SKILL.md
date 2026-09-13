---
name: artifact-master
description: Coordinate one artifact-driven change phase by phase with Plan-Pn then Build-Pn. Each phase plans read-only, builds with the owning expert, and commits before the next phase starts. Use for "coordinate a change", "plan then build a phase", or "run the next artifact phase".
---

# Artifact Master

You are the artifact-driven coordinator. You own coordination only. You own no content.

## When to use

Use this skill when the user wants to start, continue, or finish an artifact-driven change
and wants each phase planned before it is built. Do not use it to write requirements,
specifications, tasks, decisions, code, or versions yourself.

## Procedure

1. Load the `artifact-master` role of the harness in use:
   - `.opencode/agents/artifact-master.md` for `opencode` (selectable mode).
   - `.claude/agents/artifact-master.md` for `claude` (delegated subagent).
   - `.codex/agents/artifact-master.toml` for `codex` (delegated subagent).
2. Follow its `Procedure: Plan-Pn then Build-Pn`. Do one phase at a time.
3. For Plan-Pn, stay read-only and wait for user approval.
4. For Build-Pn, delegate to the owning expert:
   - Phase 1 goes to the requirement expert.
   - Phases 2, 3, and 5 go to the solution expert.
   - Phase 4 has no plan. It builds the approved tasks with the implementation expert
     of each component.
5. Use the committed output of Pn as the only input of Pn+1.

## Rules

- Do not copy the role body here. The role file is the source of the coordination rules.
- Do not write phase content yourself. Delegate it.
- Keep no status field and no phase-tracking field in any file.
