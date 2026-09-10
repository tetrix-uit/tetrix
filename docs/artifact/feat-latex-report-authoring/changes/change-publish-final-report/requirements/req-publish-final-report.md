# req-publish-final-report: Publish and display the final report

**Master:** [Requirements](README.md)
**Priority:** Must
**Context:** Not applicable

## Statement

The documentation site must publish `final-project-report.vi.pdf` and display it on a
documentation page.

## Acceptance criteria

- Given the workflow builds the final report, when it builds the documentation site, then the site
  artifact contains `final-project-report.vi.pdf`.
- Given a site user opens the final-report page, when the PDF is available, then the page displays
  the PDF in an iframe.

## Notes

The published PDF path is `final-project-report.vi.pdf` at the documentation site static root.
