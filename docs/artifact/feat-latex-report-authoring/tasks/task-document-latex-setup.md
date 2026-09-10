# task-document-latex-setup: Document LaTeX setup

**Plan:** [Implementation plan](README.md)
**Covers:** req-setup-guidance, req-local-compilation, spec-setup-guidance

## Goal

Project contributors can use the LaTeX setup and report compilation procedures.

## Steps

1. Add the LaTeX setup guidance to the root `README.md` file.
2. Give the `devenv shell`, `xelatex --version`, and `latexmk -xelatex report.tex` procedure.
3. Give the Debian and Ubuntu `texlive-full` and `latexmk` installation procedure.
4. Give the macOS `mactex-no-gui` installation procedure.
5. State that `mactex-no-gui` gives XeLaTeX and `latexmk`.

## Check

1. Check that the document has each required command.
2. Check that the document names Debian, Ubuntu, and macOS.
3. Check that the document states that `mactex-no-gui` gives XeLaTeX and `latexmk`.
