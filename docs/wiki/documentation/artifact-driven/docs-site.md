# Documentation site

The documentation site is a website that renders the `docs/` tree of the repository. The factory
renders the site project at `apps/documentation/`. The project sets the options
`factory.composition.artifact-driven.docs-site` in `devenv.local.nix`: `enable`, `title`, `url`,
`base-url`, and `notification`. The shell renders the site project from these options.

## Run locally

Node.js 22 is not in the shell. Get it in one of two ways:

- Add `languages.javascript = { enable = true; npm.enable = true; };` to `devenv.local.nix`.
- Run the commands below with `nix shell nixpkgs#nodejs_22`.

Then run these commands:

1. `cd apps/documentation`
2. `npm ci`
3. `npm run start`

The last command starts a local server and opens the website in the browser.

## Publish

The workflow `.github/workflows/docs-site.yml` builds the website and publishes it to GitHub
Pages on each push to the default branch. One manual step remains. In the repository settings,
under Pages, set the source to "GitHub Actions". Do this step one time.

A push to another branch does not change the published website. A failed build does not change
the published website. The Actions tab shows the failed run.

## Set up deployment notifications

The workflow can send one message after GitHub Pages deploys the site. Select Google Chat or Slack
in `devenv.local.nix`:

```nix
factory.composition.artifact-driven.docs-site.notification = {
  provider = "google-chat"; # Or "slack".
  webhook-secret = "DOCS_SITE_NOTIFICATION_WEBHOOK";
};
```

The default provider is `"unset"`. This value generates no notifier or notification step.

Make an incoming webhook for the Google Chat space or Slack channel. Use the provider procedure:

- [Google Chat incoming webhooks](https://developers.google.com/workspace/chat/quickstart/webhooks)
- [Slack incoming webhooks](https://api.slack.com/messaging/webhooks)

Treat the webhook URL as a password. Store it in the GitHub Actions repository secret that the
`webhook-secret` option names:

```bash
read -rsp "Notification webhook: " DOCS_SITE_NOTIFICATION_WEBHOOK
printf '\n'
printf '%s' "$DOCS_SITE_NOTIFICATION_WEBHOOK" \
  | gh secret set DOCS_SITE_NOTIFICATION_WEBHOOK
unset DOCS_SITE_NOTIFICATION_WEBHOOK
```

The message identifies the repository, the deployed URL, the source revision, and the workflow
run. The workflow sends a message after a successful push or manual deployment. It sends no message
after a failed build or deployment.

The notifier retries a temporary delivery failure two times. If all attempts fail, the workflow
reports a failure, but GitHub Pages keeps the deployed site. A workflow rerun can send the message
again.

## Write pages that render

- A `.md` file renders as CommonMark. Put a `<name>` placeholder in backticks or in a code
  block. A bare `<name>` in prose does not render.
- Link a `README.md` file, not a folder. The link `](decisions/README.md)` opens the index page
  of the folder.
- A link to a URL path of a folder must end with `/`, for example `](decisions/)`. Without the
  `/`, the browser resolves the link in the parent folder.
- The templates under `docs/wiki/**/templates/` do not render.
