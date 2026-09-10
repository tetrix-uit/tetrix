# Implementation plan: Publish final report

**Change:** [change-publish-final-report](../../../changes/change-publish-final-report/README.md)

## Order of work

| Step | Task | Depends on |
| --- | --- | --- |
| 1 | [task-override-docs-factory-files](task-override-docs-factory-files.md) | - |
| 2 | [task-build-and-copy-final-report](task-build-and-copy-final-report.md) | task-override-docs-factory-files |
| 3 | [task-add-final-report-page](task-add-final-report-page.md) | task-build-and-copy-final-report |
| 4 | [task-validate-final-report-publication](task-validate-final-report-publication.md) | task-build-and-copy-final-report, task-add-final-report-page |

## Definition of done

- The check of each task passes.
- The acceptance criteria of each requirement pass.
