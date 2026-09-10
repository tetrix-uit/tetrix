# task-validate-final-report-publication: Validate final report publication

**Plan:** [Implementation plan](README.md)
**Covers:** req-build-final-report, req-publish-final-report, spec-final-report-workflow, spec-final-report-page

## Goal

The workflow and site output contain a usable final report PDF.

## Steps

1. Run the default-branch workflow with the valid final report source.
2. Inspect the uploaded Pages artifact.
3. Check the deployed report page.
4. Run the workflow with a LaTeX error in the report source.
5. Check the workflow failure point and the absence of a new Pages artifact.

## Check

1. Check that the Pages artifact root contains `final-project-report.vi.pdf`.
2. Check that the deployed page iframe and download link use the `/tetrix/` base URL.
3. Check that the deployed iframe displays the PDF.
4. Check that the download link downloads `final-project-report.vi.pdf`.
5. Check that the invalid-source workflow fails before artifact upload and deployment.
