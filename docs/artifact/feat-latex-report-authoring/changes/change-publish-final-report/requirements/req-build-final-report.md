# req-build-final-report: Build the final report

**Master:** [Requirements](README.md)
**Priority:** Must
**Context:** Not applicable

## Statement

The documentation site workflow must compile `docs/reports/final-project-report.vi.tex` with
XeLaTeX.

## Acceptance criteria

- Given the default-branch documentation site workflow runs, when the report source is valid, then
  the workflow creates `final-project-report.vi.pdf`.
- Given the report source has a XeLaTeX error, when the workflow runs, then the workflow fails
  before it publishes the documentation site artifact.

## Notes

The generated PDF is a workflow output. The repository does not store the generated PDF.
