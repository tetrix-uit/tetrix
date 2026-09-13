# spec-development-environment: Add the LaTeX tools to the development environment

**Master:** [Specifications](README.md)
**Covers:** req-local-compilation

## Description

The root development environment will give a project contributor the XeLaTeX engine and the
`latexmk` build tool through the full TeX Live distribution.

## Contract

The root `devenv.nix` file will add this package to the development environment:

- `pkgs.texliveFull`

After a contributor enters the environment with `devenv shell`, these commands will be
available:

```text
xelatex --version
latexmk -xelatex report.tex
```

`latexmk -xelatex report.tex` will use XeLaTeX to compile `report.tex` on the local computer.

## Errors

If `report.tex` does not exist, `latexmk` will report a file error. The guide will tell the
contributor to run the command in the directory that contains `report.tex`.
