# task-add-latex-tools: Add LaTeX tools to the development environment

**Plan:** [Implementation plan](README.md)
**Covers:** req-local-compilation, spec-development-environment

## Goal

The root development environment gives XeLaTeX and `latexmk` to a project contributor.

## Steps

1. Add `pkgs.texliveFull` to the package list in the root `devenv.nix` file.

## Check

1. Run `devenv shell`.
2. Run `xelatex --version`.
3. Run `latexmk -xelatex report.tex` in a directory that contains `report.tex`.
