# Artifact-Driven Documentation

This project keeps the source of truth for each feature in the repository. The documents of a
feature are its artifacts. The artifacts are in `docs/artifact/`. Write the artifacts before the
code. Update the artifacts when the feature changes.

## Directory structure

    docs/artifact/
        README.md                  The index of the features.
        feat-<name>/
            README.md              The summary of the feature.
            requirements/          Required.
                README.md          The master requirement.
                req-<name>.md      One teardown requirement.
            specifications/        Required.
                README.md          The master specification.
                spec-<name>.md     One teardown specification.
            decisions/             Optional. Present only if a decision had more than one option.
                adr-<name>.md      One architecture decision record (ADR).
            tasks/                 Required.
                README.md          The implementation plan.
                task-<name>.md     One implementation task.
            changes/               Optional. Present only after a change to a feature whose code exists.
                change-<name>/
                    README.md      The summary of the change.
                    requirements/  Present if the requirements change. Same structure as above.
                    specifications/
                    decisions/
                    tasks/         Present if the change needs code.

## Artifact types

| Artifact | Content | Template |
| --- | --- | --- |
| Feature summary | The purpose and the links of the feature. | `templates/feature/README.md` |
| Master requirement | The business need. Links to the teardown requirements. | `templates/feature/requirements/README.md` |
| Teardown requirement | One requirement with its acceptance criteria. | `templates/feature/requirements/req-name.md` |
| Master specification | The solution. Links to the teardown specifications. | `templates/feature/specifications/README.md` |
| Teardown specification | One part of the solution: a contract, an interface, or a data model. | `templates/feature/specifications/spec-name.md` |
| Decision | One decision with its options and the option that you selected. | `templates/feature/decisions/adr-name.md` |
| Implementation plan | The order of the tasks. Links to the tasks. | `templates/feature/tasks/README.md` |
| Task | One unit of implementation work. | `templates/feature/tasks/task-name.md` |
| Change summary | The reason for a change to a feature whose code exists. | `templates/change/README.md` |

## Names

- Use lowercase letters, digits, and hyphens in `<name>`. Example: `feat-user-login`.
- Give each teardown artifact a short name that says its topic. Example: `req-password-rules.md`.
- Each teardown artifact links to its master. Each master lists its teardown artifacts.

## The five phases

Do the phases in order. Do not start a phase before the commit of the phase before it.
Each phase ends with a commit that contains the artifacts of that phase.

| Phase | Name | Input | Output |
| --- | --- | --- | --- |
| 1 | Requirements | The business need. | `requirements/` |
| 2 | Specifications | The requirements. | `specifications/`, and `decisions/` if a decision had more than one option. |
| 3 | Plan | The requirements and the specifications. | `tasks/README.md` and the task files. |
| 4 | Implementation | The tasks. | The code and the tests. |
| 5 | Change | A change to a feature whose code exists. | `changes/change-<name>/` |

### Phase 1: Requirements

1. Copy `templates/feature/` to `docs/artifact/feat-<name>/`.
2. Write the business need in `requirements/README.md`.
3. If the need has more than one part, write one `req-<name>.md` for each part.
4. Add the feature to `docs/artifact/README.md`.
5. Commit the artifacts.

### Phase 2: Specifications

1. Write the solution in `specifications/README.md`.
2. Write one `spec-<name>.md` for each contract, interface, or data model.
3. If a decision has more than one option, write one `decisions/adr-<name>.md`. Give the options
   and the option that you selected.
4. If the feature has no decision, delete the `decisions/` folder.
5. Make sure that each requirement has at least one specification.
6. Commit the artifacts.

### Phase 3: Plan

1. Write the order of the work in `tasks/README.md`.
2. Write one `task-<name>.md` for each unit of work. Give the requirements and the specifications
   that the task covers.
3. Commit the artifacts.

### Phase 4: Implementation

1. Do the tasks in the order of `tasks/README.md`.
2. Commit the code and the artifacts.

### Phase 5: Change

Use this phase only for a feature whose code exists in the repository. If the code does not
exist, change the artifacts in place. Then do the phases after the change again.

1. Make the folder `changes/change-<name>/`. Copy `templates/change/README.md` into it.
2. Write the reason for the change in `README.md`.
3. If the requirements change, copy `requirements/`, `specifications/`, and `tasks/` from
   `templates/feature/` into the change folder. Then do phases 1 to 4 in the change folder.
4. If only the specifications or the decisions change, copy `specifications/` and `tasks/` from
   `templates/feature/` into the change folder. Then do phases 2 to 4 in the change folder.
5. When the code of the change exists, update the master artifacts of the feature so that they show
   the current state.
