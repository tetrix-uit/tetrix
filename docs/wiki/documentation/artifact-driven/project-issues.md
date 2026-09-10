# Accepted Artifact Issues

The repository is the source of truth for feature artifacts. GitHub Actions makes project issues
only after an artifact pull request merges.

## Lifecycle

| Artifact change | Project result |
| --- | --- |
| Add | Make an issue with the configured first status. |
| Change | Update the existing issue and keep its status. |
| Rename | Update the existing issue identity and links. |
| Delete | Set status `Withdrawn`, then close or archive the issue. |
| Close a pull request without merge | Make no project change. |

The workflow also has a manual full scan. Use it for the first setup or for recovery.

## Factory configuration

Select the documentation, CI, and project-management adapters. Configure the target and credential
names in the selected project-management adapter. Then enable the project-issues composition.

```nix
factory = {
  domain = {
    documentation.use = "artifact-driven";
    ci-cd.provider.use = "github-actions";
    project-management.provider = {
      use = "github-projects";
      github-projects = {
        ownership = "personal";
        owner = "owner-name";
        project-number = 1;
        token-secret = "PROJECTS_TOKEN";
      };
    };
  };

  composition.artifact-driven.project-issues = {
    enable = true;
    notification = {
      uses = [ "google-chat" "telegram" ];
      google-chat.webhook-secret = "ARTIFACT_NOTIFICATION_GOOGLE_CHAT_WEBHOOK";
      telegram = {
        token-secret = "ARTIFACT_NOTIFICATION_TELEGRAM_TOKEN";
        chat-id = "-100123";
      };
    };
  };
};
```

Set `factory.composition.artifact-driven.project-issues.artifact-status` to change the first
status of an artifact type. Adapter selection alone does not enable this integration.

Set `notification.uses` to the required providers. The supported providers are `"google-chat"`,
`"slack"`, and `"telegram"`. The default is an empty list. An empty list adds no notification
files to the repository.

Use the [provider credential guide](project-issue-credentials.md) to make an incoming webhook and
add its URL as a repository secret. The notification includes added, updated, renamed, and
withdrawn artifacts. Manual scans and pull requests without artifact changes send no notification.

## GitHub Projects setup

Use the [provider credential guide](project-issue-credentials.md) to create and store the token.

1. Make a personal or organization project.
2. Add one single-select field named `Status`.
3. Add every configured artifact status to the field.
4. Add the token with the configured repository secret name.

The workflow makes repository issues. It adds an `artifact:<kind>` label to show the artifact type.
It connects child issues with the GitHub sub-issues API.

## Trello setup

Use the [provider credential guide](project-issue-credentials.md) to create and store the API key
and user token. Trello Free workspaces are supported. Custom Fields are not required.

1. Make one board.
2. Make one open list for every configured artifact status.
3. Add the API key and user token with the configured repository secret names.

To use separate planning and implementation boards, set both board IDs:

```nix
factory.domain.project-management.provider.trello = {
  board-id = "planning-board-id";
  implementation-board-id = "implementation-board-id";
};
```

The planning board contains summaries, requirements, specifications, and decisions. The
implementation board contains implementation plans and tasks. Each board needs its used status
lists and the configured withdrawn list.

The workflow keeps artifact metadata in each card description. It adds child card URLs to a
`Children` checklist on the parent card. It does not change existing Custom Fields on paid boards.
It adds an `artifact:<kind>` label to show the artifact type.

Repofactory creates missing artifact type labels. It preserves labels that do not start with
`artifact:`.

## Links

Each issue links to the current artifact, the accepted commit, and the merged pull request. The
workflow adds one managed comment to the merged pull request with all synchronized issue URLs.
If notification is enabled, the workflow sends the changes to the selected team destination after
synchronization and comment creation succeed.

Do not add issue URLs to artifact frontmatter. A provider change must not change the artifacts.

## Errors

The workflow checks the project schema before its first write. It stops with an error if a required
project, status, list, or credential does not exist.
