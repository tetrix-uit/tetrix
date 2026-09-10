# Project

This repository is the root of a project that uses the multiple repositories architecture.
The project has many components. Each component is an application, a service, a library, or a
deployment configuration. The project also has one shared end-to-end test repository.

## Directories

- `apps/` contains the frontend applications.
- `services/` contains the server-side services.
- `libs/` contains the shared libraries and the public libraries.
- `deployment/` contains the deployment configuration.
- `e2e/` contains the shared end-to-end tests.
- `docs/` contains the shared project knowledge and the governance documents.

## Git hooks

Two git hooks run with [prek](https://prek.j178.dev):

- The `commit-msg` hook checks the commit message with [convco](https://convco.github.io). Write
  each commit message in the Conventional Commits format: `type(scope): subject`. The scope is
  optional. The hook rejects a commit message that does not follow the format.
- The `pre-commit` hook checks the staged markdown files with
  [markdownlint](https://github.com/igorshubovych/markdownlint-cli). The rules are in
  `.markdownlint.yaml`: lines wrap at 100 columns, and inline HTML is allowed. The hook skips the
  templates in `docs/`, the `CLAUDE.md` include stub, and the agent harness directories that
  devenv generates.

The hook configuration is `.pre-commit-config.yaml`. devenv generates this file and
`.markdownlint.yaml` from `devenv.nix` and copies them into the repository. Do not edit these
files by hand. Change `devenv.nix` and enter the devenv shell again to regenerate them.

### Set up the hooks with devenv

Enter the devenv shell. The shell installs `prek`, `convco`, and `markdownlint`, and installs the
git hooks.

```bash
devenv shell
```

### Set up the hooks without devenv

1. Install `prek`. Use one of these commands, or see the
   [installation page](https://prek.j178.dev/installation) for more options.

   ```bash
   uv tool install prek
   brew install prek
   curl --proto '=https' --tlsv1.2 -LsSf https://github.com/j178/prek/releases/latest/download/prek-installer.sh | sh
   ```

2. Install `convco` and make sure that it is on your `PATH`. Use one of these commands, or download
   a binary from the [releases page](https://github.com/convco/convco/releases).

   ```bash
   cargo install convco
   brew install convco
   ```

3. Install `markdownlint-cli` and make sure that `markdownlint` is on your `PATH`. Use one of
   these commands.

   ```bash
   npm install --global markdownlint-cli
   brew install markdownlint-cli
   ```

4. Install the git hooks from the repository root.

   ```bash
   prek install
   ```

## LaTeX reports

Use XeLaTeX to write and compile LaTeX reports. Run the compile command in the directory that
contains `report.tex`.

### Set up LaTeX with devenv

1. Enter the devenv shell.

   ```bash
   devenv shell
   ```

1. Check the XeLaTeX installation.

   ```bash
   xelatex --version
   ```

1. Compile a report with XeLaTeX.

   ```bash
   latexmk -xelatex report.tex
   ```

The devenv shell includes the full TeX Live distribution and `latexmk`.

### Set up LaTeX without devenv

#### Debian or Ubuntu

1. Install the full TeX Live distribution and `latexmk`.

   ```bash
   sudo apt install texlive-full latexmk
   ```

1. Check the XeLaTeX installation.

   ```bash
   xelatex --version
   ```

#### macOS

1. Install MacTeX without the graphical applications.

   ```bash
   brew install --cask mactex-no-gui
   ```

`mactex-no-gui` includes XeLaTeX and `latexmk`.

1. Check the XeLaTeX installation.

   ```bash
   xelatex --version
   ```

After you install the tools, compile a report with XeLaTeX.

```bash
latexmk -xelatex report.tex
```

## Read more

- [Multiple Repositories Architecture](docs/wiki/repo-arch/multiple-repositories.md).
