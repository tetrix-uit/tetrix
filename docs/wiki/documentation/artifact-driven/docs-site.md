# Documentation site

The documentation site is a website that renders the `docs/` tree of the repository. The factory
renders the site project at `apps/documentation/`. The project sets the options
`factory.composition.artifact-driven.docs-site` in `devenv.local.nix`: `enable`, `title`, `url`,
`base-url`, `target`, `azure-static-web-app.api-token-secret`,
`azure-static-web-app.deploy-tool`, and `notification`. The shell renders the site project from these options.

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

The factory renders one CI pipeline for the selected CI provider. The provider `github-actions`
renders `.github/workflows/docs-site.yml`. The provider `azure-pipelines` renders
`azure-pipelines/docs-site.yml`. Each pipeline builds the website and publishes it to the
selected target on each push to the default branch.

The option `target` selects the hosting service. It accepts `github-pages` or
`azure-static-web-app`. The default is `github-pages`. The site uses exactly one target.
With no `target` value, the factory publishes the website to GitHub Pages.

With `target = "github-pages"`, each pipeline publishes the website to GitHub
Pages. One manual step remains. In the repository settings,
under Pages, set the source to "GitHub Actions". Do this step one time.

A push to another branch does not change the published website. A failed build does not change
the published website. The Actions tab shows the failed run for `github-actions`. The pipeline
run shows the failed run for `azure-pipelines`.

## Publish to Azure Static Web Apps

Set the target in `devenv.local.nix`:

```nix
factory.composition.artifact-driven.docs-site.target = "azure-static-web-app";
```

The option `azure-static-web-app.api-token-secret` names the secret that holds the Static Web
App deployment token. The default is `DOCS_SITE_AZURE_STATIC_WEB_APP_TOKEN`. The workflow
reads it from `${{ secrets.DOCS_SITE_AZURE_STATIC_WEB_APP_TOKEN }}`. The Azure pipeline
reads it from the secret variable `$(DOCS_SITE_AZURE_STATIC_WEB_APP_TOKEN)`. Use a custom
name only when the secret uses that name.

Make these four manual steps outside the factory:

1. Create one Static Web App resource in Azure for the site.
2. Copy the deployment token of that resource.
3. Store the token as a GitHub secret or as an Azure secret variable with the configured
   secret name. Mark the Azure variable as secret.
4. Set the docs-site `url` and `base-url` options to the Static Web App address.

The factory cannot create the resource and cannot read the token. The generated pipeline
builds the site with `npm run build` and uploads `apps/documentation/build` with
`skip_app_build: true`. It never builds the site a second time.

### Select the deploy tool

The option `azure-static-web-app.deploy-tool` selects the mechanism that uploads the Static
Web App. It accepts `official-task` or `swa-cli`. The default is `official-task`.

```nix
factory.composition.artifact-driven.docs-site.azure-static-web-app.deploy-tool = "swa-cli";
```

- `official-task` uses the official action or task. This value gives the version 6.1.0 behavior.
- `swa-cli` installs the factory-owned Static Web Apps CLI. It then deploys with the CLI.

The factory pins the CLI version `2.0.10`. The installation command is
`npm install --global @azure/static-web-apps-cli@2.0.10`. The deploy command is
`swa deploy ./build --deployment-token "$SWA_CLI_DEPLOYMENT_TOKEN" --env production`. The
command runs from `apps/documentation` and uploads `apps/documentation/build`. The command
does not run `swa build`. A project cannot set or change the CLI version.

The GitHub workflow keeps the npm cache of `actions/setup-node@v4`. The Azure pipeline sets
`npm_config_cache` to `$(Pipeline.Workspace)/.npm`. It also adds a `Cache@2` task. The cache
key is `"npm" | "$(Agent.OS)" | "swa-cli-2.0.10" | apps/documentation/package-lock.json`. The
key contains the CLI version. A factory update with a new pin uses a new cache.

Both values deploy the same build output to the same Static Web App. The deployment
notifications do not change.

## Set up Azure Pipelines

Select the CI provider in `devenv.local.nix`:

```nix
factory.domain.ci-cd.provider.use = "azure-pipelines";
```

Create the pipeline in Azure DevOps from `azure-pipelines/docs-site.yml`. The pipeline starts on
each push to the default branch when the push changes `docs/**`, `apps/documentation/**`,
`azure-pipelines/docs-site.yml`, or a configured `workflow.watch-paths` value. You can also
start a manual run for setup and recovery.

Store the GitHub token as a secret variable with the name `DOCS_SITE_GITHUB_TOKEN`. Mark the
variable as secret. The publish step uses this variable to publish the build output to GitHub
Pages. Store each notification secret as a secret variable with the same name. Mark each variable
as secret. The Telegram chat ID stays a plain variable.

One manual step remains. In the repository settings, under Pages, set the source to "GitHub
Actions". Do this step one time. The factory cannot do this step.

## Publish generated assets

Use typed options to add generated files to the site. Do not replace `docusaurus.config.js` or
`.github/workflows/docs-site.yml`. You do not need a `docusaurus.config.local.js` file.

`static-directories` contains paths relative to `apps/documentation/`. The factory adds each
`workflow.watch-paths` value after its default watch paths.

The build workflow has three step lists:

| Option | Position |
| --- | --- |
| `workflow.build.before-node-setup` | After checkout and before Node.js setup. |
| `workflow.build.before-site-build` | After `npm ci` and before `npm run build`. |
| `workflow.build.after-site-build` | After `npm run build` and before publication. |

A step supports `name`, `uses`, `with`, `run`, `env`, and `working-directory`. Set one of `uses`
or `run`. A run step uses `apps/documentation/` as its default working directory. Azure
Pipelines runs the same steps in the same order with the same values.

This example builds a LaTeX manual from one service. It copies the PDF into a static directory.
Docusaurus then adds the PDF to the website build.

```nix
factory.composition.artifact-driven.docs-site = {
  static-directories = [ "static" ];

  workflow = {
    watch-paths = [ "services/manual/docs/**" ];

    build.before-node-setup = [
      {
        name = "Build the manual PDF";
        uses = "xu-cheng/latex-action@v4";
        "with" = {
          root_file = "manual.tex";
          working_directory = "services/manual/docs";
          latexmk_use_xelatex = true;
        };
      }
    ];

    build.before-site-build = [
      {
        name = "Copy the manual PDF";
        run = ''
          mkdir -p static/manual
          cp "$PDF_SOURCE" static/manual/manual.pdf
        '';
        env.PDF_SOURCE = "../../services/manual/docs/manual.pdf";
        working-directory = "apps/documentation";
      }
    ];

    build.after-site-build = [
      {
        name = "Check the published manual PDF";
        run = "test -f build/manual/manual.pdf";
      }
    ];
  };
};
```

The published file URL is `<base-url>/manual/manual.pdf`. A failed custom step stops the build and
prevents a deployment.

## Set up deployment notifications

The workflow can send one message to each selected provider after the selected target deploys the site.

```nix
factory.composition.artifact-driven.docs-site.notification = {
  uses = [ "google-chat" "telegram" ];
  google-chat.webhook-secret = "DOCS_SITE_NOTIFICATION_GOOGLE_CHAT_WEBHOOK";
  telegram = {
    token-secret = "DOCS_SITE_NOTIFICATION_TELEGRAM_TOKEN";
    chat-id = "-100123";
  };
};
```

The default is an empty `uses` list. This list generates no notifier or notification step.

Make an incoming webhook for the Google Chat space or Slack channel. Use a bot token and chat ID
for Telegram. Use the provider procedure:

- [Google Chat incoming webhooks](https://developers.google.com/workspace/chat/quickstart/webhooks)
- [Slack incoming webhooks](https://api.slack.com/messaging/webhooks)
- [Telegram Bot API](https://core.telegram.org/bots/api#sendmessage)

Treat a webhook URL or a bot token as a password. Store each value in its configured GitHub
Actions repository secret. When the CI provider is `azure-pipelines`, store each value as an
Azure secret variable with the same name and mark it as secret.

```bash
read -rsp "Google Chat webhook: " DOCS_SITE_NOTIFICATION_GOOGLE_CHAT_WEBHOOK
printf '\n'
printf '%s' "$DOCS_SITE_NOTIFICATION_GOOGLE_CHAT_WEBHOOK" \
  | gh secret set DOCS_SITE_NOTIFICATION_GOOGLE_CHAT_WEBHOOK
unset DOCS_SITE_NOTIFICATION_GOOGLE_CHAT_WEBHOOK
```

The message identifies the repository, the deployed URL, the source revision, and the workflow
run. The workflow sends a message after a successful push or manual deployment. It sends no message
after a failed build or deployment.

The notifier retries a temporary delivery failure two times. If all attempts fail, the workflow
reports a failure, but the deployed site stays available. A workflow rerun can send the message
again.

## Write pages that render

- A `.md` file renders as CommonMark. Put a `<name>` placeholder in backticks or in a code
  block. A bare `<name>` in prose does not render.
- Link a `README.md` file, not a folder. The link `](decisions/README.md)` opens the index page
  of the folder.
- A link to a URL path of a folder must end with `/`, for example `](decisions/)`. Without the
  `/`, the browser resolves the link in the parent folder.
- The templates under `docs/wiki/**/templates/` do not render.
- A version folder `versions/<version>/` has no README. The site generates an index page for it
  and shows the version number as the label. Do not link to the version folder itself: the site
  builder reads `versions/1.0.0/` as a file with the extension `.0`. Link to a file in the folder.
