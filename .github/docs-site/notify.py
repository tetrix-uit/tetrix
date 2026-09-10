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
PROVIDERS = {"google-chat", "slack", "telegram"}


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
    target: str,
    message: str,
    chat_id: str = "",
    opener: Callable[..., Any] = urllib.request.urlopen,
    sleeper: Callable[[float], None] = time.sleep,
) -> None:
    if provider not in PROVIDERS:
        fail(f"Unsupported notification provider: {provider}")
    if not target:
        fail(f"{provider} notification target must not be empty")
    if provider == "telegram":
        if not chat_id:
            fail("telegram notification chat ID must not be empty")
        url = f"https://api.telegram.org/bot{target}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
    else:
        url = target
        payload = {"text": message}
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode(),
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


def configured_uses(environment: Mapping[str, str]) -> list[str]:
    uses: object
    try:
        uses = json.loads(environment.get("DOCS_SITE_NOTIFICATION_USES", ""))
    except json.JSONDecodeError:
        fail("DOCS_SITE_NOTIFICATION_USES must be a JSON list")
    if not isinstance(uses, list) or not all(isinstance(use, str) and use in PROVIDERS for use in uses):
        fail("DOCS_SITE_NOTIFICATION_USES must contain supported providers")
    if len(uses) != len(set(uses)):
        fail("DOCS_SITE_NOTIFICATION_USES must not contain duplicate providers")
    return uses


def send_all(environment: Mapping[str, str], message: str) -> None:
    failures = []
    for provider in configured_uses(environment):
        try:
            if provider == "telegram":
                send_message(provider, environment.get("DOCS_SITE_NOTIFICATION_TELEGRAM_TOKEN", ""), message, environment.get("DOCS_SITE_NOTIFICATION_TELEGRAM_CHAT_ID", ""))
            else:
                name = "DOCS_SITE_NOTIFICATION_" + provider.upper().replace("-", "_") + "_WEBHOOK"
                send_message(provider, environment.get(name, ""), message)
            print(f"Sent documentation site deployment notification to {provider}")
        except RuntimeError as error:
            print(f"docs-site-notification: {error}", file=sys.stderr)
            failures.append(provider)
    if failures:
        fail("Notification delivery failed for: " + ", ".join(failures))


def main() -> int:
    try:
        message = build_message(os.environ)
        send_all(os.environ, message)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"docs-site-notification: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
