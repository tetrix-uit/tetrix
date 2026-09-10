# task-add-final-report-page: Add the final report page

**Plan:** [Implementation plan](README.md)
**Covers:** req-publish-final-report, spec-final-report-page

## Goal

The report source gives site users a page that displays and downloads the published PDF.

## Steps

1. Update `docs/reports/final-project-report.vi.md` as the final report page.
2. Import `useBaseUrl` from `@docusaurus/useBaseUrl`.
3. Make the PDF path with `useBaseUrl("final-project-report.vi.pdf")`.
4. Use the path in an iframe with a final project report title.
5. Add a download link for `final-project-report.vi.pdf`.
6. Tell the user to use the download link when the browser cannot display the PDF.

## Check

1. Put `final-project-report.vi.pdf` in `apps/documentation/static`.
2. Build the documentation site.
3. Open the report page with the `/tetrix/` base URL.
4. Check that the iframe displays the PDF.
5. Check that the download link downloads `final-project-report.vi.pdf`.
