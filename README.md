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

## Commit messages

Write each commit message in the Conventional Commits format: `type(scope): subject`. The scope
is optional. A `commit-msg` git hook rejects a commit message that does not follow the format.
The hook runs with [prek](https://prek.j178.dev) and checks the message with
[convco](https://convco.github.io).

The hook configuration is `.pre-commit-config.yaml`. devenv generates this file from `devenv.nix`
and copies it into the repository. Do not edit the file by hand. Change `devenv.nix` and enter the
devenv shell again to regenerate it.

### Set up the hooks with devenv

Enter the devenv shell. The shell installs `prek` and `convco`, and installs the git hooks.

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

3. Install the git hooks from the repository root.

   ```bash
   prek install
   ```

## Read more

- [Multiple Repositories Architecture](docs/wiki/repo-arch/multiple-repositories.md).
