# adr-full-tex-live: Use the full TeX Live distribution

**Relates to:** spec-development-environment

## Context

The development environment needs XeLaTeX and the LaTeX packages that reports can need.
The user selects the full TeX Live distribution.

## Options

1. Use `pkgs.texliveFull`. Pro: It gives XeLaTeX and the full TeX Live package set. Con: It
   uses more disk space and download time.
2. Use a selected TeX Live package set. Pro: It uses less disk space and download time. Con:
   A report can need a package that the environment does not have.

## Decision

Use `pkgs.texliveFull`. This is the explicit user selection. It gives a repeatable environment
with the full TeX Live package set.

## Consequences

Contributors can compile reports that need TeX Live packages without adding packages to the
development environment. The first environment download can use more time and disk space.
