# task-override-docs-factory-files: Override the documentation factory files

**Plan:** [Implementation plan](README.md)
**Covers:** spec-final-report-workflow, adr-local-factory-override

## Goal

The root development environment replaces the factory workflow and Docusaurus configuration with
local files.

## Steps

1. Add `lib.mkForce` entries to the root `devenv.nix` `files` configuration.
2. Replace `.github/workflows/docs-site.yml` with the current factory workflow content.
3. Replace `apps/documentation/docusaurus.config.js` with the current factory configuration content.
4. Add `staticDirectories: ["static"]` to the Docusaurus replacement.
5. Keep all other factory workflow and Docusaurus behavior.

## Check

1. Check that both required paths have `lib.mkForce` entries in `devenv.nix`.
2. Check that the local workflow keeps the required factory jobs, permissions, concurrency rule,
   and notification.
3. Run the documentation build with a file in `apps/documentation/static`.
4. Check that the build copies the file to the site output root.
