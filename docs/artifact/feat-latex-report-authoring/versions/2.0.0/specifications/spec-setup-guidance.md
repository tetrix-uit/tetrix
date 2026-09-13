# spec-setup-guidance: Give LaTeX setup guidance

**Master:** [Specifications](README.md)
**Covers:** req-setup-guidance, req-local-compilation

## Description

The root `README.md` file will give one procedure for the development environment and one
procedure for native installation.

## Contract

The root `README.md` file will give these procedures and commands:

| Method | Required content |
| --- | --- |
| Project development environment | Run `devenv shell`. Run `xelatex --version`. Run `latexmk -xelatex report.tex`. |
| Debian or Ubuntu native installation | Install `texlive-full` and `latexmk`. |
| macOS native installation | Install `mactex-no-gui`. State that it gives XeLaTeX and `latexmk`. |

The Debian and Ubuntu procedure will use this command:

```bash
sudo apt install texlive-full latexmk
```

The macOS procedure will use this command:

```bash
brew install --cask mactex-no-gui
```

Each procedure will tell the contributor to run `xelatex --version` to check the XeLaTeX
installation. Each procedure will tell the contributor to run `latexmk -xelatex report.tex`
in the directory that contains `report.tex`.

## Errors

If `xelatex --version` fails, the contributor must install the tools for the selected method
before the contributor compiles the report.
