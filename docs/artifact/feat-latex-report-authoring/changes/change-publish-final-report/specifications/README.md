# Specifications: Publish final report

## Solution

The root `devenv.nix` file will use `lib.mkForce` in `files` to replace two factory-managed
files. The local workflow will build the final report before it builds the documentation site.
The local Docusaurus configuration will copy `apps/documentation/static` into the Pages artifact.

The workflow will copy the generated PDF to that static directory. The report page will use a
base-url-safe PDF path in its iframe and download link.

## Teardown specifications

| ID | Specification | Covers |
| --- | --- | --- |
| [spec-final-report-workflow](spec-final-report-workflow.md) | Build and copy the final report in the Pages workflow. | req-build-final-report, req-publish-final-report |
| [spec-final-report-page](spec-final-report-page.md) | Display and download the static final report PDF. | req-publish-final-report |

## Decisions

- [adr-local-factory-override](../decisions/adr-local-factory-override.md)
