# Requirements: Publish final report

## Business need

Contributors need the documentation site deployment to compile the final report with XeLaTeX and
publish its PDF. Site users need to read the published report from the documentation site.

## Scope

- In scope: Compile `docs/reports/final-project-report.vi.tex` with XeLaTeX in the documentation
  site workflow.
- In scope: Publish `final-project-report.vi.pdf` in the documentation site artifact.
- In scope: Add a documentation page that displays the published PDF in an iframe.
- Out of scope: Commit the generated PDF to the repository.
- Out of scope: Compile another LaTeX report.

## Domain

This change is a generic documentation publishing capability. It has no business domain or
bounded context.

| Subdomain | Type | Context | Actors | Events |
| --- | --- | --- | --- | --- |
| Documentation publishing | Generic | Not applicable | Contributor, site user | Final report published |

## Teardown requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| [req-build-final-report](req-build-final-report.md) | The documentation site workflow must build the final report with XeLaTeX. | Must |
| [req-publish-final-report](req-publish-final-report.md) | The documentation site must publish and display the final report PDF. | Must |

## Acceptance

A default-branch documentation site deployment builds the final report, publishes the PDF, and
gives site users a page that displays the PDF.
