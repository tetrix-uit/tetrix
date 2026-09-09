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
| `ARTIFACT_NOTIFICATION_WEBHOOK` | Repository secret | The workflow sends accepted artifact summaries to this webhook. |

The workflow exposes `PROJECTS_TOKEN` as `PROJECT_TOKEN` to the synchronizer. If you changed
`token-secret` in the factory configuration, use that configured repository secret name.

## Set up GitHub Projects

GitHub currently does not let fine-grained personal access tokens access Projects owned by a user
account. Use a classic personal access token for this integration.

1. Open **GitHub settings > Developer settings > Personal access tokens > Tokens (classic)**.
2. Select **Generate new token (classic)**.
3. Enter a descriptive note and select an expiration.
4. Select the `repo` and `project` scopes.
5. Select `workflow` only if this token must change files in `.github/workflows/`.
6. Generate the token.
7. Authorize the token for single sign-on if the organization requires it.
8. Read the token into a temporary variable.

   ```bash
   read -rsp "GitHub token: " GH_TOKEN
   printf '\n'
   export GH_TOKEN
   ```

9. Check access to GitHub, the repository, and the project.

   ```bash
   gh auth status
   gh repo view OWNER/REPOSITORY
   gh project view PROJECT_NUMBER --owner OWNER --format json
   ```

10. Add the token to the default repository secret.

    ```bash
    printf '%s' "$GH_TOKEN" | gh secret set PROJECTS_TOKEN --repo OWNER/REPOSITORY
    ```

11. Check that the secret name exists.

    ```bash
    gh secret list --repo OWNER/REPOSITORY
    ```

12. Remove the local variable.

    ```bash
    unset GH_TOKEN
    ```

## Set up Trello

`TRELLO_API_KEY` identifies the Trello Power-Up. `TRELLO_TOKEN` authorizes the Trello user. The
generated workflow reads repository secrets with these default names.

1. Open [Trello Power-Up administration](https://trello.com/power-ups/admin).
2. Create a Power-Up, or select an existing Power-Up.
3. Open the **API Key** tab and generate an API key.
4. Replace `TRELLO_API_KEY` in the following URL with the API key.
5. Select `1day`, `30days`, or `never` for the `expiration` value.
6. Open the completed URL in a browser and authorize access.

   ```text
   https://trello.com/1/authorize?expiration=30days&scope=read,write&response_type=token&key=TRELLO_API_KEY
   ```

   The integration needs `read` and `write` scopes. Use a dedicated automation account if you
   select `never`. Copy the user token from the authorization result.

7. Read the API key and user token into temporary variables.

   ```bash
   read -rsp "Trello API key: " TRELLO_API_KEY
   printf '\n'
   export TRELLO_API_KEY
   read -rsp "Trello token: " TRELLO_TOKEN
   printf '\n'
   export TRELLO_TOKEN
   ```

8. Add both values to the default repository secrets.

   ```bash
   printf '%s' "$TRELLO_API_KEY" | gh secret set TRELLO_API_KEY --repo OWNER/REPOSITORY
   printf '%s' "$TRELLO_TOKEN" | gh secret set TRELLO_TOKEN --repo OWNER/REPOSITORY
   ```

9. Check that both secret names exist.

   ```bash
   gh secret list --repo OWNER/REPOSITORY
   ```

10. Remove the local variables.

   ```bash
   unset TRELLO_API_KEY TRELLO_TOKEN
   ```

## Set up an acceptance notification

Select one notification provider in the Factory configuration:

```nix
factory.composition.artifact-driven.project-issues.notification = {
  provider = "google-chat"; # Or "slack".
  webhook-secret = "ARTIFACT_NOTIFICATION_WEBHOOK";
};
```

### Make a Google Chat webhook

1. Open the Google Chat space that must receive the messages.
2. Open **Apps and integrations** from the space menu.
3. Add a webhook and give it a descriptive name.
4. Copy the webhook URL.

For detailed instructions, refer to the
[Google Chat incoming webhook guide](https://developers.google.com/workspace/chat/quickstart/webhooks).
Your Google Workspace administrator must permit incoming webhooks.

### Make a Slack webhook

1. Make or open a Slack app for the workspace.
2. Activate **Incoming Webhooks**.
3. Select **Add New Webhook to Workspace**.
4. Select the channel that must receive the messages.
5. Copy the webhook URL.

For detailed instructions, refer to the
[Slack incoming webhook guide](https://api.slack.com/messaging/webhooks).

### Store the webhook

Treat the webhook URL as a password. Read it with a silent prompt:

```bash
read -rsp "Notification webhook: " ARTIFACT_NOTIFICATION_WEBHOOK
printf '\n'
```

Add the value to the configured repository secret:

```bash
printf '%s' "$ARTIFACT_NOTIFICATION_WEBHOOK" \
  | gh secret set ARTIFACT_NOTIFICATION_WEBHOOK --repo OWNER/REPOSITORY
```

Check the secret name, and then remove the local variable:

```bash
gh secret list --repo OWNER/REPOSITORY
unset ARTIFACT_NOTIFICATION_WEBHOOK
```

The next merged pull request with a supported artifact change tests delivery. A manual workflow
run synchronizes artifacts but does not send a notification.

## Check the workflow

Run the manual full scan after you configure the provider target and its repository secrets.

1. Start the generated workflow.

   ```bash
   gh workflow run accepted-artifact-issues.yml --repo OWNER/REPOSITORY
   ```

2. Get the identifier of the latest manual run.

   ```bash
   RUN_ID="$(gh run list --workflow accepted-artifact-issues.yml --repo OWNER/REPOSITORY \
     --event workflow_dispatch --limit 1 --json databaseId --jq '.[0].databaseId')"
   ```

3. Watch the run and check its result.

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
- [Google Chat: Send messages with incoming webhooks](https://developers.google.com/workspace/chat/quickstart/webhooks)
- [Slack: Sending messages using incoming webhooks](https://api.slack.com/messaging/webhooks)
