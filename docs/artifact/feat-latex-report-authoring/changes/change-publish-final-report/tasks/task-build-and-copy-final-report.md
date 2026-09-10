# task-build-and-copy-final-report: Build and copy the final report

**Plan:** [Implementation plan](README.md)
**Covers:** req-build-final-report, req-publish-final-report, spec-final-report-workflow

## Goal

The documentation workflow builds the final report with XeLaTeX and copies its PDF before the site build.

## Steps

1. Add the `xu-cheng/latex-action@v3` step to the local documentation workflow.
2. Set its root file to `docs/reports/final-project-report.vi.tex`.
3. Set `latexmk_use_xelatex` to `true`.
4. Add a copy step after the LaTeX step.
5. Make the copy step create `apps/documentation/static` when it is absent.
6. Copy `final-project-report.vi.pdf` to that static directory before `npm run build`.

## Check

1. Run the default-branch workflow with a valid report source.
2. Check that the LaTeX action uses XeLaTeX.
3. Check that the PDF exists at `apps/documentation/static/final-project-report.vi.pdf` before
   the site build.
4. Run the workflow with an invalid report source.
5. Check that the LaTeX step fails before the copy, site build, artifact upload, deployment, and
   notification steps.
