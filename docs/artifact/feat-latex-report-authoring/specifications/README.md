# Specifications: LaTeX report authoring

## Solution

The root development environment will include the full TeX Live distribution, which gives
XeLaTeX and `latexmk`. A contributor guide will give the commands for the development environment
and for native installation on supported operating systems.

The solution changes the root development environment and shared project documentation.

## Teardown specifications

| ID | Specification | Covers |
| --- | --- | --- |
| [spec-development-environment](spec-development-environment.md) | Add the LaTeX tools to the root development environment. | req-local-compilation |
| [spec-setup-guidance](spec-setup-guidance.md) | Give the development-environment and native setup procedures. | req-setup-guidance, req-local-compilation |

## Decisions

- [adr-full-tex-live](../decisions/adr-full-tex-live.md)
