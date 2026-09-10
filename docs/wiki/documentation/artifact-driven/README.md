# Artifact-Driven Documentation

This project keeps the source of truth for each feature in the repository. The documents of a
feature are its artifacts. The artifacts are in `docs/artifact/`. Write the artifacts before the
code. Each unit of work on a feature is a change. When the code of a change exists, the change gets
a version. A version holds the full state of the feature.

## Directory structure

    docs/artifact/
        README.md                       The index of the features.
        feat-<name>/
            README.md                   The feature summary. Names the current version.
            changes/                    Required. One folder for each change.
                change-initial/         Required. The first build of the feature.
                    README.md           The change summary. From none, To 1.0.0.
                    requirements/       Required in change-initial.
                        README.md       The master requirement.
                        req-<name>.md   One teardown requirement.
                    specifications/     Required in change-initial.
                        README.md       The master specification.
                        spec-<name>.md  One teardown specification.
                    decisions/          Optional. Present only if a decision had more than one option.
                        adr-<name>.md   One architecture decision record (ADR).
                    tasks/              Required in change-initial.
                        README.md       The implementation plan.
                        task-<name>.md  One implementation task.
                change-<name>/          One folder for each later change.
                    README.md           The change summary. From, To, Type, Reason.
                    requirements/       Present only if a requirement changes.
                    specifications/     Present only if a specification changes.
                    decisions/          Present only if a decision changes.
                    tasks/              Present only if the change needs code.
            versions/                   Present after the first phase 5.
                <major>.<minor>.<patch>/
                    requirements/       The full requirements at this version.
                    specifications/     The full specifications at this version.
                    decisions/          The full decisions at this version. Absent if none.

A feature has no root `requirements/`, `specifications/`, `decisions/`, or `tasks/` folder. A
version folder has no `tasks/` folder and no `README.md`. The `versions/` folder has no
`README.md`.

## Artifact types

| Artifact | Content | Template |
| --- | --- | --- |
| Feature summary | The purpose of the feature, the current version, and one table row for each version. | `templates/feature/README.md` |
| Change summary | The reason for a change, the version before, the version after, and the type. | `templates/change/README.md` |
| Master requirement | The business need. Links to the teardown requirements. | `templates/change/requirements/README.md` |
| Teardown requirement | One requirement with its acceptance criteria. | `templates/change/requirements/req-name.md` |
| Master specification | The solution. Links to the teardown specifications. | `templates/change/specifications/README.md` |
| Teardown specification | One part of the solution: a contract, an interface, or a data model. | `templates/change/specifications/spec-name.md` |
| Decision | One decision with its options and the option that you selected. | `templates/change/decisions/adr-name.md` |
| Implementation plan | The order of the tasks. Links to the tasks. | `templates/change/tasks/README.md` |
| Task | One unit of implementation work. | `templates/change/tasks/task-name.md` |
| Version | A copy of the requirements, the specifications, and the decisions at one version. | None. Phase 5 makes it by copy. |

## Names

- Use lowercase letters, digits, and hyphens in `<name>`. Example: `feat-user-login`.
- Give each teardown artifact a short name that says its topic. Example: `req-password-rules.md`.
- Each teardown artifact links to its master. Each master lists its teardown artifacts.
- The first change of a feature is `change-initial`. Each later change is `change-<name>`.
- A version is `<major>.<minor>.<patch>`. Each part is a decimal number without a leading zero.
  The first version of a feature is `1.0.0`.
- The change README gives the version before the change in `**From:**` and the version after the
  change in `**To:**`. The first change has `**From:** none` and `**To:** 1.0.0`.
- The `**Type:**` line of the change README gives the next version:

| Type | Meaning | To |
| --- | --- | --- |
| Requirements | A requirement is added, changed, or removed. | `major+1.0.0` |
| Specifications | Only a specification changes. No requirement changes. | `major.minor+1.0` |
| Decisions | Only a decision changes. No requirement changes. | `major.minor+1.0` |
| Correction | An artifact text is corrected. No requirement, no specification contract, and no decision changes. | `major.minor.patch+1` |

A `**Type:**` line can name two types, for example `Specifications, Decisions`. The first type
gives the bump. The type `Requirements` is always the first when present. The type of
`change-initial` is `Requirements`.

## Where to read

| Need | Read |
| --- | --- |
| The current state of a feature | `versions/<current>/`, where `<current>` is the version in the feature README. |
| The reason for a change | `changes/change-<name>/README.md`. |
| The work of a change | `changes/change-<name>/tasks/`. |
| The artifacts that a change touched | `changes/change-<name>/`. Do not read a change to learn the full state. |
| The history of a feature | The `## Versions` table of the feature README. |

## The five phases

Do the phases in order. Do not start a phase before the commit of the phase before it.
Each phase ends with a commit that contains the artifacts of that phase. Phases 1 to 4 happen in
the change folder. The steps are the same for `change-initial` and for a later change.

| Phase | Name | Input | Output |
| --- | --- | --- | --- |
| 1 | Requirements | The business need, or the reason for a change. | `changes/change-<name>/README.md`, and `requirements/` if a requirement changes. |
| 2 | Specifications | The requirements. | `specifications/`, and `decisions/` if a decision had more than one option. |
| 3 | Plan | The requirements and the specifications. | `tasks/README.md` and the task files. |
| 4 | Implementation | The tasks. | The code and the tests. |
| 5 | Version | A change whose code exists. | `versions/<version>/` and the updated feature README. |

### Phase 1: Requirements

1. For a new feature, make the folder `docs/artifact/feat-<name>/`. Copy
   `templates/feature/README.md` into it. Write the summary.
2. Make the folder `changes/change-<name>/`. The first change is `change-initial`. Copy
   `templates/change/README.md` into it.
3. Write `**From:**`, `**To:**`, `**Type:**`, and the reason in the change README. Get `**To:**`
   from the table in [Names](#names).
4. If the type includes Requirements, make `requirements/` in the change:
   - For `change-initial`, copy `templates/change/requirements/`.
   - For a later change, copy the files that change from `versions/<from>/requirements/`. Copy
     the master `README.md` if the list of requirements changes.
5. Write the business need in `requirements/README.md`. Write one `req-<name>.md` for each
   requirement that the change adds or changes.
6. For a new feature, add the feature to `docs/artifact/README.md`.
7. Commit the artifacts.

### Phase 2: Specifications

1. If a specification changes, make `specifications/` in the change:
   - For `change-initial`, copy `templates/change/specifications/`.
   - For a later change, copy the files that change from `versions/<from>/specifications/`.
     Copy the master `README.md` if the list of specifications changes.
2. Write the solution in `specifications/README.md`. Write one `spec-<name>.md` for each
   contract, interface, or data model that the change adds or changes.
3. If a decision has more than one option, make `decisions/` in the change:
   - For a new decision, copy `templates/change/decisions/adr-name.md` to `adr-<name>.md`.
   - For a changed decision, copy the file from `versions/<from>/decisions/`.
   Give the options and the option that you selected.
4. Make sure that each requirement of the feature has at least one specification.
5. Commit the artifacts.

### Phase 3: Plan

1. If the change needs code, make `tasks/` in the change. Copy `templates/change/tasks/` into it.
2. Write the order of the work in `tasks/README.md`.
3. Write one `task-<name>.md` for each unit of work. Give the requirements and the specifications
   that the task covers.
4. Commit the artifacts.

### Phase 4: Implementation

1. Do the tasks in the order of `tasks/README.md`.
2. If an artifact of the change has an error, correct it in place in the change.
3. Commit the code and the artifacts.

### Phase 5: Version

Do this phase only when the code of the change exists. Copy and delete only. Do not edit a file
under `versions/`.

1. Make the folder `versions/<to>/`. `<to>` is the `**To:**` of the change README.
2. Copy the content of `versions/<from>/` into it. For `change-initial`, there is nothing to copy.
3. Copy the `requirements/`, `specifications/`, and `decisions/` folders of the change over it. A
   file with the same path replaces the file in the copy.
4. Delete the paths listed under `## Removed artifacts` of the change README.
5. Update the feature README: `**Current version:**`, `## Current artifacts`, and the row of the
   change in the `## Versions` table.
6. Commit the version and the feature README.

## Rules for the artifacts of a change

- Each file in `requirements/`, `specifications/`, or `decisions/` of a change is the full
  replacement file of one artifact. It has the same filename as the artifact that it replaces in
  `versions/<from>/`. A new filename is a new artifact.
- A change holds only the artifacts that change. Do not copy an artifact that does not change.
- When the list of teardown artifacts of a folder changes, the change holds the master `README.md`
  of that folder. The master lists every teardown artifact at the new version.
- A master README in a change has the line
  `**Change:** [<change name>](../../../changes/change-<name>/README.md)` under its title. The
  long relative path resolves from the change folder and from the version folder after the copy
  of phase 5.
- A change that removes an artifact lists each path under `## Removed artifacts` in the change
  README. Each path is relative to the version folder. Example: `specifications/spec-old-api.md`.
- Correct an error in a change in place, before its phase 5. Do not make a second change for it.
- A correction to a file under `versions/` is a new change and a new version.
- Tasks exist only in a change. A version has no tasks.
- No artifact records a status or a phase-tracking field. A version number is not a status.
