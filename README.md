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
is optional. Enter the devenv shell before you commit. The shell installs a `commit-msg` git hook
with `prek`. The hook rejects a commit message that does not follow the format.

## Read more

- [Multiple Repositories Architecture](docs/wiki/repo-arch/multiple-repositories.md).
