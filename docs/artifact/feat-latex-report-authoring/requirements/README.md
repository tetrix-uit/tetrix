# Requirements: LaTeX report authoring

## Business need

Project contributors need a repeatable local environment to write and compile LaTeX reports with
XeLaTeX. They need this environment to make reports on their local computer.

## Scope

- In scope: A repeatable local environment for LaTeX report authoring and compilation with XeLaTeX.
- In scope: Setup guidance for contributors who use the project development environment.
- In scope: Setup guidance for contributors who do not use the project development environment.
- Out of scope: A report template or report content.
- Out of scope: Report compilation in continuous integration.
- Out of scope: A LaTeX engine other than XeLaTeX.

## Domain

This feature is a generic developer-environment capability. It has no business domain or bounded context.

| Subdomain | Type | Context | Actors | Events |
| --- | --- | --- | --- | --- |
| Developer environment | Generic | Not applicable | Project contributor | LaTeX report compiled |

## Teardown requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| [req-local-compilation](req-local-compilation.md) | The project must give contributors a repeatable local environment for XeLaTeX report compilation. | Must |
| [req-setup-guidance](req-setup-guidance.md) | The project must give contributors setup guidance for XeLaTeX report compilation. | Must |

## Acceptance

The project gives contributors a repeatable local environment and setup guidance to write and
compile LaTeX reports with XeLaTeX.
