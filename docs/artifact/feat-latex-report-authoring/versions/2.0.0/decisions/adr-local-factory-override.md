# adr-local-factory-override: Override the factory documentation files locally

**Relates to:** spec-final-report-workflow, spec-final-report-page

## Context

The factory manages the documentation workflow and the Docusaurus configuration. The final report
needs a LaTeX workflow step and a static directory. The user selects a local factory file override.

## Options

1. Use `lib.mkForce` in root `devenv.nix` to replace the two factory-managed files. Pro: The
   project can add the required behavior without a Repofactory change. Con: The project must keep
   the local replacements aligned with factory updates.
2. Change Repofactory to add report publishing support. Pro: Factory users can use the behavior.
   Con: The change affects the factory and needs its release before this project can use it.

## Decision

Use `lib.mkForce` in the root `devenv.nix` `files` configuration. Replace
`.github/workflows/docs-site.yml` and `apps/documentation/docusaurus.config.js`. This is the user
selection. It gives this project the required report publishing behavior without a Repofactory
change.

## Consequences

The project keeps the factory for all other documentation site files and options. The local
replacements must preserve the existing workflow and Docusaurus behavior. A factory update can
need a matching update to either local replacement.
