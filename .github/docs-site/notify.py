"""Send one documentation site deployment message to a team webhook."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping
from typing import Any

MAX_MESSAGE_LENGTH = 3500
MAX_ATTEMPTS = 3
PROVIDERS = {"google-chat", "slack"}


def fail(message: str) -> None:
    raise RuntimeError(message)


def required(environment: Mapping[str, str], name: str) -> str:
    value = environment.get(name, "")
    if not value:
        fail(f"{name} must not be empty")
    return value


def build_message(environment: Mapping[str, str]) -> str:
    repository = required(environment, "DOCS_SITE_REPOSITORY")
    deployment_url = required(environment, "DOCS_SITE_DEPLOYMENT_URL")
    ref_name = required(environment, "DOCS_SITE_REF_NAME")
    commit_sha = required(environment, "DOCS_SITE_COMMIT_SHA")
    run_url = required(environment, "DOCS_SITE_RUN_URL")
    message = "\n".join(
        [
            f"Documentation site deployed: {repository}",
            f"URL: {deployment_url}",
            f"Source: {ref_name} @ {commit_sha[:7]}",
            f"Run: {run_url}",
        ]
    )
    if len(message) > MAX_MESSAGE_LENGTH:
        fail("The deployment notification exceeds the message size limit")
    return message


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
        fail("DOCS_SITE_NOTIFICATION_WEBHOOK must not be empty")
    request = urllib.request.Request(
        webhook,
        data=json.dumps({"text": message}, ensure_ascii=False).encode(),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "repofactory-docs-site-notification",
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
        message = build_message(os.environ)
        provider = os.environ.get("DOCS_SITE_NOTIFICATION_PROVIDER", "")
        webhook = os.environ.get("DOCS_SITE_NOTIFICATION_WEBHOOK", "")
        send_message(provider, webhook, message)
        print(f"Sent documentation site deployment notification to {provider}")
    except (OSError, RuntimeError, ValueError) as error:
        print(f"docs-site-notification: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
