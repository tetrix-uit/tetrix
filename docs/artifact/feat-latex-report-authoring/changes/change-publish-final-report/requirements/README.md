# Requirements: LaTeX report authoring

**Change:** [change-publish-final-report](../../../changes/change-publish-final-report/README.md)

## Business need

Project contributors need a repeatable local environment to write and compile LaTeX reports with
XeLaTeX. They need this environment to make reports on their local computer.

Contributors also need the documentation site deployment to compile the final report with XeLaTeX
and publish its PDF. Site users need to read the published report from the documentation site.

## Scope

- In scope: A repeatable local environment for LaTeX report authoring and compilation with XeLaTeX.
- In scope: Setup guidance for contributors who use the project development environment.
- In scope: Setup guidance for contributors who do not use the project development environment.
- In scope: Compile `docs/reports/final-project-report.vi.tex` with XeLaTeX in the documentation
  site workflow.
- In scope: Publish `final-project-report.vi.pdf` in the documentation site artifact.
- In scope: Add a documentation page that displays the published PDF in an iframe.
- Out of scope: A report template or report content.
- Out of scope: A LaTeX engine other than XeLaTeX.
- Out of scope: Commit the generated PDF to the repository.
- Out of scope: Compile another LaTeX report in continuous integration.

## Domain

This feature is a generic developer-environment and documentation publishing capability. It has no
business domain or bounded context.

| Subdomain | Type | Context | Actors | Events |
| --- | --- | --- | --- | --- |
| Developer environment | Generic | Not applicable | Project contributor | LaTeX report compiled |
| Documentation publishing | Generic | Not applicable | Contributor, site user | Final report published |

## Teardown requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| [req-local-compilation](req-local-compilation.md) | The project must give contributors a repeatable local environment for XeLaTeX report compilation. | Must |
| [req-setup-guidance](req-setup-guidance.md) | The project must give contributors setup guidance for XeLaTeX report compilation. | Must |
| [req-build-final-report](req-build-final-report.md) | The documentation site workflow must build the final report with XeLaTeX. | Must |
| [req-publish-final-report](req-publish-final-report.md) | The documentation site must publish and display the final report PDF. | Must |

## Acceptance

The project gives contributors a repeatable local environment and setup guidance to write and
compile LaTeX reports with XeLaTeX. A default-branch documentation site deployment builds the final
report, publishes the PDF, and gives site users a page that displays the PDF.
