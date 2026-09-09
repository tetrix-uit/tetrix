# Project Issue Provider Credentials

Use this procedure to add credentials for GitHub Projects or Trello. The generated workflow reads
the credentials from GitHub Actions repository secrets.

## Before you start

Treat each token as a password. Do not commit a token, display it, or put it in a command argument.
Use the silent prompts in this procedure, and remove the local variables after use.

Replace `OWNER/REPOSITORY`, `OWNER`, and `PROJECT_NUMBER` in the examples. If you configured other
secret names, replace the default names too.

## GitHub credential names

| Name | Location | Use |
| --- | --- | --- |
| `GITHUB_TOKEN` | GitHub Actions | GitHub supplies this token for repository issues and comments. Do not add this secret. |
| `GH_TOKEN` | Local shell | GitHub CLI uses this temporary variable during setup. |
| `PROJECTS_TOKEN` | Repository secret | The workflow uses this secret for GitHub Projects. |

The workflow exposes `PROJECTS_TOKEN` as `PROJECT_TOKEN` to the synchronizer. If you changed
`token-secret` in the factory configuration, use that configured repository secret name.

## Set up GitHub Projects

GitHub currently does not let fine-grained personal access tokens access Projects owned by a user
account. Use a classic personal access token for this integration.

1. Open **GitHub settings > Developer settings > Personal access tokens > Tokens (classic)**.
1. Select **Generate new token (classic)**.
1. Enter a descriptive note and select an expiration.
1. Select the `repo` and `project` scopes.
1. Select `workflow` only if this token must change files in `.github/workflows/`.
1. Generate the token.
1. Authorize the token for single sign-on if the organization requires it.
1. Read the token into a temporary variable.

```bash
read -rsp "GitHub token: " GH_TOKEN
printf '\n'
export GH_TOKEN
```

1. Check access to GitHub, the repository, and the project.

```bash
gh auth status
gh repo view OWNER/REPOSITORY
gh project view PROJECT_NUMBER --owner OWNER --format json
```

1. Add the token to the default repository secret.

```bash
printf '%s' "$GH_TOKEN" | gh secret set PROJECTS_TOKEN --repo OWNER/REPOSITORY
```

1. Check that the secret name exists.

```bash
gh secret list --repo OWNER/REPOSITORY
```

1. Remove the local variable.

```bash
unset GH_TOKEN
```

## Set up Trello

`TRELLO_API_KEY` identifies the Trello Power-Up. `TRELLO_TOKEN` authorizes the Trello user. The
generated workflow reads repository secrets with these default names.

1. Open [Trello Power-Up administration](https://trello.com/power-ups/admin).
1. Create a Power-Up, or select an existing Power-Up.
1. Open the **API Key** tab and generate an API key.
1. Replace `TRELLO_API_KEY` in the following URL with the API key.
1. Select `1day`, `30days`, or `never` for the `expiration` value.
1. Open the completed URL in a browser and authorize access.

```text
https://trello.com/1/authorize?expiration=30days&scope=read,write&response_type=token&key=TRELLO_API_KEY
```

The integration needs `read` and `write` scopes. Use a dedicated automation account if you select
`never`. Copy the user token from the authorization result.

1. Read the API key and user token into temporary variables.

```bash
read -rsp "Trello API key: " TRELLO_API_KEY
printf '\n'
export TRELLO_API_KEY
read -rsp "Trello token: " TRELLO_TOKEN
printf '\n'
export TRELLO_TOKEN
```

1. Add both values to the default repository secrets.

```bash
printf '%s' "$TRELLO_API_KEY" | gh secret set TRELLO_API_KEY --repo OWNER/REPOSITORY
printf '%s' "$TRELLO_TOKEN" | gh secret set TRELLO_TOKEN --repo OWNER/REPOSITORY
```

1. Check that both secret names exist.

```bash
gh secret list --repo OWNER/REPOSITORY
```

1. Remove the local variables.

```bash
unset TRELLO_API_KEY TRELLO_TOKEN
```

## Check the workflow

Run the manual full scan after you configure the provider target and its repository secrets.

1. Start the generated workflow.

```bash
gh workflow run accepted-artifact-issues.yml --repo OWNER/REPOSITORY
```

1. Get the identifier of the latest manual run.

```bash
RUN_ID="$(gh run list --workflow accepted-artifact-issues.yml --repo OWNER/REPOSITORY \
  --event workflow_dispatch --limit 1 --json databaseId --jq '.[0].databaseId')"
```

1. Watch the run and check its result.

```bash
gh run watch "$RUN_ID" --repo OWNER/REPOSITORY --exit-status
```

## Rotate or revoke credentials

Create a replacement token before an expiring token stops. Write the replacement to the same
repository secret name. GitHub Actions uses the new value on the next run.

Revoke an unused or exposed GitHub token in **GitHub settings > Developer settings > Personal
access tokens**. Revoke an unused or exposed Trello token in the Trello account applications page.
Then replace the repository secret if the integration must continue.

## References

- [GitHub: Managing personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [GitHub: Automating Projects with Actions](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions)
- [GitHub CLI: `gh auth login`](https://cli.github.com/manual/gh_auth_login)
- [Trello: Authorization](https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/)
