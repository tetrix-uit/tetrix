"""Send one accepted artifact summary to a team webhook."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

MAX_MESSAGE_LENGTH = 3500
MAX_ATTEMPTS = 3
PROVIDERS = {"google-chat", "slack"}
CHANGES = {"added", "updated", "renamed", "withdrawn"}


def fail(message: str) -> None:
    raise RuntimeError(message)


def load_result(path: str) -> dict[str, Any]:
    if not path:
        fail("ARTIFACT_ISSUES_RESULT must identify the synchronization result")
    result = json.loads(Path(path).read_text())
    if not isinstance(result, dict):
        fail("The synchronization result must be a JSON object")
    repository = result.get("repository")
    pull_request = result.get("pullRequest")
    artifacts = result.get("artifacts")
    if not isinstance(repository, str) or not repository:
        fail("The synchronization result needs a repository")
    if not isinstance(pull_request, dict) or not isinstance(artifacts, list):
        fail("The synchronization result needs pullRequest and artifacts values")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            fail("Each artifact result must be a JSON object")
        if artifact.get("change") not in CHANGES:
            fail("Each artifact result needs a supported change")
        if not isinstance(artifact.get("path"), str) or not artifact["path"]:
            fail("Each artifact result needs a path")
        if not isinstance(artifact.get("url"), str) or not artifact["url"]:
            fail("Each artifact result needs a tracker URL")
        if artifact["change"] == "renamed" and not artifact.get("previousPath"):
            fail("Each renamed artifact result needs a previousPath")
    return result


def artifact_line(artifact: dict[str, str]) -> str:
    path = artifact["path"]
    if artifact["change"] == "renamed":
        path = f"{artifact['previousPath']} -> {path}"
    return f"- {artifact['change'].upper()}: {path} — {artifact['url']}"


def build_message(result: dict[str, Any]) -> str | None:
    artifacts = result["artifacts"]
    if not artifacts:
        return None
    pull_request = result["pullRequest"]
    number = pull_request.get("number", 0)
    title = str(pull_request.get("title", ""))
    if len(title) > 200:
        title = title[:199] + "…"
    url = str(pull_request.get("url", ""))
    prefix = [f"Accepted artifact changes: {result['repository']}#{number}"]
    if title:
        prefix.append(title)
    if url:
        prefix.append(url)
    lines = [artifact_line(artifact) for artifact in artifacts]
    for count in range(len(lines), -1, -1):
        parts = prefix + lines[:count]
        omitted = len(lines) - count
        if omitted:
            parts.append(f"... {omitted} more artifact changes. See the pull request for all changes.")
        message = "\n".join(parts)
        if len(message) <= MAX_MESSAGE_LENGTH:
            return message
    fail("The acceptance notification header exceeds the message size limit")


def send_message(
    provider: str,
    webhook: str,
    message: str,
    opener: Callable[..., Any] = urllib.request.urlopen,
    sleeper: Callable[[float], None] = time.sleep,
) -> None:
    if provider not in PROVIDERS:
        fail(f"Unsupported notification provider: {provider}")
    if not webhook:
        fail("ARTIFACT_NOTIFICATION_WEBHOOK must not be empty")
    request = urllib.request.Request(
        webhook,
        data=json.dumps({"text": message}, ensure_ascii=False).encode(),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "repofactory-artifact-notification",
        },
        method="POST",
    )
    for attempt in range(MAX_ATTEMPTS):
        retryable = False
        status = 0
        try:
            with opener(request, timeout=15) as response:
                status = getattr(response, "status", None)
                if status is None:
                    status = response.getcode()
            if 200 <= status < 300:
                return
            retryable = status == 429 or status >= 500
        except urllib.error.HTTPError as error:
            status = error.code
            retryable = status == 429 or status >= 500
        except (OSError, urllib.error.URLError):
            retryable = True
        if retryable and attempt + 1 < MAX_ATTEMPTS:
            sleeper(attempt + 1)
            continue
        if status:
            fail(f"{provider} notification failed with HTTP {status}")
        fail(f"{provider} notification failed because of a network error")


def main() -> int:
    try:
        result = load_result(os.environ.get("ARTIFACT_ISSUES_RESULT", ""))
        message = build_message(result)
        if message is None:
            print("No accepted artifact changes need notification")
            return 0
        provider = os.environ.get("ARTIFACT_NOTIFICATION_PROVIDER", "")
        send_message(provider, os.environ.get("ARTIFACT_NOTIFICATION_WEBHOOK", ""), message)
        print(f"Sent accepted artifact notification to {provider}")
    except (OSError, RuntimeError, ValueError) as error:
        print(f"accepted-artifact-notification: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
