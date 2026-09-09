# Documentation website

This folder is the documentation website. It renders the `docs/` tree of the repository.

The factory owns `package.json`, `package-lock.json`, `docusaurus.config.js`, `sidebars.js`,
`site.json`, and `.gitignore`. The shell overwrites these files on each entry. Change the options
`factory.composition.artifact-driven.docs-site` in `devenv.local.nix`, not these files.

The project owns `README.md` and `src/css/custom.css`.

The guide is at [docs/wiki/documentation/artifact-driven/docs-site.md](../../docs/wiki/documentation/artifact-driven/docs-site.md).
