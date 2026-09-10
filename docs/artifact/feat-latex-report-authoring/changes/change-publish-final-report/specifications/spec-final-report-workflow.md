# spec-final-report-workflow: Build and copy the final report

**Master:** [Specifications](README.md)
**Covers:** req-build-final-report, req-publish-final-report

## Description

The root `devenv.nix` file will locally replace the factory-managed documentation workflow and
Docusaurus configuration. The replacement will keep the factory workflow behavior and add the
final report build and copy steps.

## Contract

The root `devenv.nix` file will set both file contents with `lib.mkForce` in the `files`
configuration:

| Factory-managed file | Required local replacement |
| --- | --- |
| `.github/workflows/docs-site.yml` | A documentation site workflow with the contract below. |
| `apps/documentation/docusaurus.config.js` | The factory configuration with `staticDirectories: ["static"]`. |

The local workflow will preserve the existing workflow name, default-branch build condition,
Node.js setup, `npm ci`, Pages artifact upload, Pages deployment, concurrency rule, permissions,
and deployment notification behavior.

The `build` job will run these steps in this order after repository checkout and before `npm run
build`:

1. Run `xu-cheng/latex-action@v3` with `root_file:
   docs/reports/final-project-report.vi.tex` and `latexmk_use_xelatex: true`.
2. Copy `docs/reports/final-project-report.vi.pdf` to
   `apps/documentation/static/final-project-report.vi.pdf`.
3. Run `npm run build` in `apps/documentation`.

The copy step will create `apps/documentation/static` when the directory does not exist. The
uploaded Pages artifact will remain `apps/documentation/build`.

The workflow trigger paths will include these paths:

- `docs/**`
- `apps/documentation/**`
- `devenv.nix`
- `.github/workflows/docs-site.yml`

The Docusaurus replacement will keep all other current configuration behavior. It will add only
the `static` directory to the static directory list. Therefore, the site build will copy
`apps/documentation/static/final-project-report.vi.pdf` to the root of the Pages artifact.

## Errors

If the LaTeX action cannot compile the report, the build job fails. The workflow does not run the
copy, site build, artifact upload, deployment, or notification steps.

If the generated PDF is not at the required source path, the copy step fails. The workflow does
not build or publish a site artifact.

If `npm run build` fails, the workflow does not upload or deploy the Pages artifact. The previous
Pages deployment remains available.

## Validation

Run the workflow on the default branch with a valid report source. Check that the LaTeX action
uses XeLaTeX. Check that the Pages artifact contains `final-project-report.vi.pdf` at its root.

Make the report source invalid and run the workflow. Check that the LaTeX action fails before the
artifact upload step.

Run the documentation build with the copied PDF. Check that the built site contains
`final-project-report.vi.pdf` at its root.
