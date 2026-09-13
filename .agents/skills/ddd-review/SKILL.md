---
name: ddd-review
description: Review DDD artifacts, bounded context canvases, aggregate invariants, and artifact links. Use for "DDD review", "bounded context canvas", "aggregate invariants", or "DDD artifact links".
---

# DDD review

## When to use

Use this skill to review existing DDD artifacts in a project.

Do not write or change an artifact. Do not select a domain model or make a domain decision.

## Read first

Read these files before the review:

- The DDD guide in `docs/wiki/design/ddd/README.md`.
- The DDD phase mapping in `docs/wiki/design/ddd/artifact-driven.md`.
- The selected repository architecture guide in `docs/wiki/repo-arch/`.
- The domain artifacts in `docs/domain/` that are in scope.
- The feature artifacts in `docs/artifact/` that are in scope: the change under review and
  `versions/<current>/` of its feature.

## Procedure

1. Identify the selected repository architecture from its guide.
2. List the domain and feature artifacts that are in scope.
3. Read the selected artifacts and their links.
4. Apply the checks in this skill only to the artifacts in scope.
5. Report each finding with the format in this skill.
6. Report that no finding exists when all checks pass.

## Checks

### Strategic checks

- Check that each context canvas has its strategic fields.
- Check that a `**Component:**` path is under `services/` for the multiple repository architecture.
- Check that a `**Component:**` path is under `src/` for the single repository architecture.
- Check that each context-map relationship uses a valid DDD contract.
- Check that the glossary gives one meaning for one term in one context.

### Tactical checks

- Check that each aggregate canvas belongs to an existing context.
- Check that each invariant defines a consistency boundary.
- Check that an aggregate references another aggregate by identity only.
- Check that a cross-aggregate state change uses a domain event and a policy.

### Feature-artifact checks

- Check that each named context and aggregate exists in the domain model.
- Check that a requirement artifact has only a `**Context:**` link.
- Check that a specification artifact has an `**Aggregate:**` link only when it changes an aggregate.
- Check that each task has one `**Context:**` link.
- Check that the task order puts an upstream context before a downstream context.

## Report

Report each finding in this format:

```text
Artifact: <path>
Failed rule: <rule>
Evidence: <fact from the artifact>
Owner: <requirement expert or solution expert>
```

Set `Owner: requirement expert` for a phase 1 finding.

Set `Owner: solution expert` for a phase 2 or phase 3 finding.

## Rules

- Review only. Do not change an artifact.
- Do not choose a domain model or make a domain decision.
- Do not move phase ownership.
- The requirement expert owns phase 1.
- The solution expert owns phases 2, 3, and 5.
