# Agent Guidance

Before you start work, read these pages:

- [Multiple Repositories Architecture](docs/wiki/repo-arch/multiple-repositories.md).
- [Artifact-Driven Documentation](docs/wiki/documentation/artifact-driven/README.md).
- [Domain-Driven Design](docs/wiki/design/ddd/README.md).
- [DDD in the Artifact-Driven Phases](docs/wiki/design/ddd/artifact-driven.md).

Keep the implementation artifacts and the local rules of each component in its own directory.
The directory is in `apps/`, `services/`, `libs/`, `deployment/`, or `e2e/`.

Keep the requirements, the specifications, the decisions, and the tasks of each feature in
`docs/artifact/`. Do the five phases in order. Commit at the end of each phase.

Keep the domain model in `docs/domain/`. One bounded context is one directory in `services/`.
Update the domain artifacts in the phase that owns them: the strategic design in phase 1, the
tactical design in phase 2.

## Commit Conventions

Never add "Co-Authored-By" lines to commits. Do not include this attribution in
commit messages, PR descriptions, or any git metadata.
