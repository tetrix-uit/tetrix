# spec-final-report-page: Display and download the final report

**Master:** [Specifications](README.md)
**Covers:** req-publish-final-report

## Description

The file `docs/reports/final-project-report.vi.md` will give site users a page for the published
final report. The page will display the static PDF and give a download fallback.

## Contract

The page will import `useBaseUrl` from `@docusaurus/useBaseUrl`. It will construct the PDF path
with `useBaseUrl("final-project-report.vi.pdf")`.

The page will use this path for both items:

- An iframe that displays the PDF.
- A download link with the `download` attribute for `final-project-report.vi.pdf`.

The iframe will have a title that identifies the final project report. The page text will tell a
site user to use the download link when the browser cannot display the PDF.

The page will not contain the generated PDF. The workflow provides the PDF in
`apps/documentation/static` before the site build.

## Errors

If the PDF is absent from the deployed site, the iframe cannot display the report. The download
link also fails. The site build must fail before deployment when the workflow cannot copy the PDF.

If a browser cannot display the PDF in the iframe, the user can use the download link. The
base-url-safe path keeps both links valid when the site base URL is not `/`.

## Validation

Build the site with `final-project-report.vi.pdf` in `apps/documentation/static`. Open the report
page from a site with the configured `/tetrix/` base URL. Check that the iframe displays the PDF.
Check that the download link downloads `final-project-report.vi.pdf`.
