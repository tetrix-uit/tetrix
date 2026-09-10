# Specifications: LaTeX report authoring

**Change:** [change-publish-final-report](../../../changes/change-publish-final-report/README.md)

## Solution

The root development environment includes the full TeX Live distribution, which gives XeLaTeX and
`latexmk`. A contributor guide gives the commands for the development environment and for native
installation on supported operating systems.

The root `devenv.nix` file will use `lib.mkForce` in `files` to replace two factory-managed
files. The local workflow will build the final report before it builds the documentation site.
The local Docusaurus configuration will copy `apps/documentation/static` into the Pages artifact.

The workflow will copy the generated PDF to that static directory. The report page will use a
base-url-safe PDF path in its iframe and download link.

The solution changes the root development environment, the documentation site workflow, the
documentation site configuration, and shared project documentation.

## Teardown specifications

| ID | Specification | Covers |
| --- | --- | --- |
| [spec-development-environment](spec-development-environment.md) | Add the LaTeX tools to the root development environment. | req-local-compilation |
| [spec-setup-guidance](spec-setup-guidance.md) | Give the development-environment and native setup procedures. | req-setup-guidance, req-local-compilation |
| [spec-final-report-workflow](spec-final-report-workflow.md) | Build and copy the final report in the Pages workflow. | req-build-final-report, req-publish-final-report |
| [spec-final-report-page](spec-final-report-page.md) | Display and download the static final report PDF. | req-publish-final-report |

## Decisions

- [adr-full-tex-live](../decisions/adr-full-tex-live.md)
- [adr-local-factory-override](../decisions/adr-local-factory-override.md)
