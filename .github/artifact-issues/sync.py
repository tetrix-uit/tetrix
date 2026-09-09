"""Synchronize accepted artifact files to GitHub Projects or Trello."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ARTIFACT_ROOT = Path("docs/artifact")
MANAGED_COMMENT = "<!-- repofactory:accepted-artifact-issues -->"
LABEL_PREFIX = "artifact:"
ARTIFACT_KINDS = (
    "feature-summary", "master-requirement", "requirement", "master-specification",
    "specification", "decision", "implementation-plan", "task", "change-summary",
)
GITHUB_LABEL_COLORS = {
    kind: color for kind, color in zip(ARTIFACT_KINDS, (
        "1f6feb", "8250df", "a371f7", "bf8700", "d4a72c",
        "cf222e", "1a7f37", "0969da", "57606a",
    ))
}
TRELLO_LABEL_COLORS = {
    kind: color for kind, color in zip(ARTIFACT_KINDS, (
        "blue", "purple", "orange", "yellow", "red",
        "green", "sky", "pink", "lime",
    ))
}
IMPLEMENTATION_KINDS = {"implementation-plan", "task"}


def type_label(kind: str) -> str:
    return LABEL_PREFIX + kind


def issue_label_names(issue: dict[str, Any], kind: str) -> list[str]:
    existing = [label["name"] if isinstance(label, dict) else label for label in issue.get("labels", [])]
    return [name for name in existing if not name.startswith(LABEL_PREFIX)] + [type_label(kind)]


@dataclass(frozen=True)
class Artifact:
    path: str
    kind: str
    parent: str | None
    feature: str


@dataclass
class IssueRef:
    id: Any
    url: str
    created: bool
    body: str = ""


def fail(message: str) -> None:
    raise RuntimeError(message)


def artifact_marker(repository: str, path: str) -> str:
    return f"<!-- repofactory:artifact:{repository}:{path} -->"


def is_feature_markdown(path: str) -> bool:
    parts = Path(path).as_posix().split("/")
    return (
        len(parts) >= 4
        and parts[:2] == ["docs", "artifact"]
        and parts[2].startswith("feat-")
        and path.endswith(".md")
    )


def _standard_artifact(prefix: list[str], rest: list[str], full_path: str) -> Artifact | None:
    feature = prefix[2]
    feature_root = "/".join(prefix)
    parent_root = feature_root + "/README.md"
    if rest == ["README.md"]:
        return Artifact(full_path, "feature-summary", None, feature)
    if rest == ["requirements", "README.md"]:
        return Artifact(full_path, "master-requirement", parent_root, feature)
    if len(rest) == 2 and rest[0] == "requirements" and rest[1].startswith("req-"):
        return Artifact(full_path, "requirement", feature_root + "/requirements/README.md", feature)
    if rest == ["specifications", "README.md"]:
        return Artifact(full_path, "master-specification", parent_root, feature)
    if len(rest) == 2 and rest[0] == "specifications" and rest[1].startswith("spec-"):
        return Artifact(full_path, "specification", feature_root + "/specifications/README.md", feature)
    if len(rest) == 2 and rest[0] == "decisions" and rest[1].startswith("adr-"):
        related = related_specification(Path(full_path))
        return Artifact(full_path, "decision", feature_root + f"/specifications/{related}.md", feature)
    if rest == ["tasks", "README.md"]:
        return Artifact(full_path, "implementation-plan", parent_root, feature)
    if len(rest) == 2 and rest[0] == "tasks" and rest[1].startswith("task-"):
        return Artifact(full_path, "task", feature_root + "/tasks/README.md", feature)
    return None


def classify_artifact(path: str) -> Artifact | None:
    clean = Path(path).as_posix()
    parts = clean.split("/")
    if len(parts) < 4 or parts[:2] != ["docs", "artifact"]:
        return None
    if not parts[2].startswith("feat-") or not clean.endswith(".md"):
        return None
    feature_prefix = parts[:3]
    rest = parts[3:]
    direct = _standard_artifact(feature_prefix, rest, clean)
    if direct is not None:
        return direct
    if len(rest) < 3 or rest[0] != "changes" or not rest[1].startswith("change-"):
        return None
    change_root = "/".join(feature_prefix + rest[:2])
    change_rest = rest[2:]
    if change_rest == ["README.md"]:
        return Artifact(clean, "change-summary", "/".join(feature_prefix) + "/README.md", parts[2])
    nested = _standard_artifact(feature_prefix, change_rest, clean)
    if nested is None:
        return None
    parent = nested.parent
    feature_root = "/".join(feature_prefix)
    if change_rest in (["requirements", "README.md"], ["specifications", "README.md"], ["tasks", "README.md"]):
        parent = change_root + "/README.md"
    elif parent is not None:
        parent = parent.replace(feature_root, change_root, 1)
    return Artifact(clean, nested.kind, parent, nested.feature)


def related_specification(path: Path) -> str:
    if not path.exists():
        return ""
    match = re.search(r"^\*\*Relates to:\*\*\s+([^\s,]+)", path.read_text(), re.MULTILINE)
    if not match:
        fail(f"Decision {path.as_posix()} must have one Relates to specification")
    name = match.group(1).removesuffix(".md")
    if not name.startswith("spec-"):
        fail(f"Decision {path.as_posix()} has an invalid Relates to value: {name}")
    return name


def artifact_title(path: str) -> str:
    source = Path(path)
    if source.exists():
        for line in source.read_text().splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return source.stem


def artifact_body(
    artifact: Artifact,
    repository: str,
    server_url: str,
    default_branch: str,
    commit_sha: str,
    pull_request_url: str,
    parent_url: str = "",
) -> str:
    quoted_path = urllib.parse.quote(artifact.path, safe="/")
    current = f"{server_url}/{repository}/blob/{default_branch}/{quoted_path}"
    immutable = f"{server_url}/{repository}/blob/{commit_sha}/{quoted_path}"
    lines = [
        "This issue represents one accepted artifact.",
        "",
        f"- Artifact: [`{artifact.path}`]({current})",
        f"- Accepted version: [{commit_sha[:12]}]({immutable})",
        f"- Artifact type: `{artifact.kind}`",
        f"- Feature: `{artifact.feature}`",
    ]
    if pull_request_url:
        lines.append(f"- Accepted by: {pull_request_url}")
    if artifact.parent:
        parent_text = f"`{artifact.parent}`"
        if parent_url:
            parent_text = f"[{parent_text}]({parent_url})"
        lines.append(f"- Parent artifact: {parent_text}")
    lines.extend(["", artifact_marker(repository, artifact.path)])
    return "\n".join(lines)


class JsonApi:
    def request(
        self,
        method: str,
        url: str,
        token: str = "",
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        request_headers = {"Accept": "application/json", "User-Agent": "repofactory-artifact-issues"}
        if token:
            request_headers["Authorization"] = f"Bearer {token}"
        if headers:
            request_headers.update(headers)
        payload = None
        if data is not None:
            payload = json.dumps(data).encode()
            request_headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=payload, headers=request_headers, method=method)
        try:
            with urllib.request.urlopen(request) as response:
                content = response.read()
                return json.loads(content) if content else None
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            fail(f"{method} {url} failed with HTTP {error.code}: {detail}")


class GitHubAdapter:
    def __init__(self, config: dict[str, Any], repository: str, api: JsonApi):
        self.config = config
        self.repository = repository
        self.api = api
        self.api_url = os.environ.get("GITHUB_API_URL", "https://api.github.com")
        self.repo_token = os.environ.get("GITHUB_TOKEN", "")
        self.project_token = os.environ.get("PROJECT_TOKEN", "")
        self.issues: dict[str, dict[str, Any]] = {}
        self.project_id = ""
        self.status_field_id = ""
        self.status_options: dict[str, str] = {}
        self.labels: set[str] = set()

    def rest(self, method: str, path: str, data: dict[str, Any] | None = None) -> Any:
        return self.api.request(
            method,
            self.api_url + path,
            self.repo_token,
            data,
            {"X-GitHub-Api-Version": "2022-11-28"},
        )

    def graphql(self, query: str, variables: dict[str, Any]) -> Any:
        result = self.api.request(
            "POST", self.api_url + "/graphql", self.project_token, {"query": query, "variables": variables}
        )
        if result.get("errors"):
            fail("GitHub GraphQL failed: " + json.dumps(result["errors"]))
        return result["data"]

    def preflight(self, statuses: dict[str, str]) -> None:
        if not self.repo_token or not self.project_token:
            fail("GITHUB_TOKEN and PROJECT_TOKEN must not be empty")
        owner_field = "user" if self.config["ownership"] == "personal" else "organization"
        query = f"""
          query($owner:String!, $number:Int!) {{
            {owner_field}(login:$owner) {{
              projectV2(number:$number) {{
                id
                fields(first:100) {{ nodes {{
                  ... on ProjectV2SingleSelectField {{ id name options {{ id name }} }}
                }} }}
              }}
            }}
          }}
        """
        data = self.graphql(query, {"owner": self.config["owner"], "number": self.config["projectNumber"]})
        owner = data.get(owner_field)
        project = owner and owner.get("projectV2")
        if not project:
            fail("The configured GitHub Project does not exist or is not accessible")
        fields = [field for field in project["fields"]["nodes"] if field and field.get("name") == "Status"]
        if len(fields) != 1:
            fail("The GitHub Project must have one single-select field named Status")
        self.project_id = project["id"]
        self.status_field_id = fields[0]["id"]
        self.status_options = {option["name"]: option["id"] for option in fields[0]["options"]}
        missing = sorted(set(statuses.values()) - set(self.status_options))
        if missing:
            fail("The GitHub Project is missing Status options: " + ", ".join(missing))
        page = 1
        while True:
            batch = self.rest("GET", f"/repos/{self.repository}/labels?per_page=100&page={page}")
            self.labels.update(label["name"] for label in batch)
            if len(batch) < 100:
                break
            page += 1
        for kind, color in GITHUB_LABEL_COLORS.items():
            name = type_label(kind)
            if name not in self.labels:
                self.rest("POST", f"/repos/{self.repository}/labels", {
                    "name": name, "color": color, "description": f"Repofactory artifact type: {kind}",
                })
                self.labels.add(name)
        page = 1
        marker_pattern = re.compile(r"<!-- repofactory:artifact:[^:]+/[^:]+:(.+) -->")
        while True:
            batch = self.rest("GET", f"/repos/{self.repository}/issues?state=all&per_page=100&page={page}")
            if not batch:
                break
            for issue in batch:
                if "pull_request" in issue:
                    continue
                match = marker_pattern.search(issue.get("body") or "")
                if match:
                    path = match.group(1)
                    if path in self.issues:
                        fail(f"Two GitHub issues have the artifact marker for {path}")
                    self.issues[path] = issue
            if len(batch) < 100:
                break
            page += 1

    def _set_project_status(self, issue: dict[str, Any], status: str) -> None:
        add = """
          mutation($project:ID!, $content:ID!) {
            addProjectV2ItemById(input:{projectId:$project, contentId:$content}) { item { id } }
          }
        """
        data = self.graphql(add, {"project": self.project_id, "content": issue["node_id"]})
        item_id = data["addProjectV2ItemById"]["item"]["id"]
        update = """
          mutation($project:ID!, $item:ID!, $field:ID!, $option:String!) {
            updateProjectV2ItemFieldValue(input:{
              projectId:$project, itemId:$item, fieldId:$field,
              value:{singleSelectOptionId:$option}
            }) { projectV2Item { id } }
          }
        """
        self.graphql(
            update,
            {
                "project": self.project_id,
                "item": item_id,
                "field": self.status_field_id,
                "option": self.status_options[status],
            },
        )

    def lookup(self, path: str) -> IssueRef | None:
        issue = self.issues.get(path)
        if issue is None:
            return None
        return IssueRef(issue["id"], issue["html_url"], False, issue.get("body") or "")

    def upsert(
        self,
        artifact: Artifact,
        title: str,
        body: str,
        status: str,
        old_path: str = "",
        withdrawn: bool = False,
    ) -> IssueRef:
        issue = self.issues.get(old_path or artifact.path) or self.issues.get(artifact.path)
        created = issue is None
        was_closed = bool(issue and issue.get("state") == "closed")
        state = "closed" if withdrawn else "open"
        labels = issue_label_names(issue or {}, artifact.kind)
        if created:
            issue = self.rest(
                "POST", f"/repos/{self.repository}/issues", {"title": title, "body": body, "labels": labels}
            )
        else:
            issue = self.rest(
                "PATCH",
                f"/repos/{self.repository}/issues/{issue['number']}",
                {"title": title, "body": body, "state": state, "labels": labels},
            )
        if old_path and old_path != artifact.path:
            self.issues.pop(old_path, None)
        self.issues[artifact.path] = issue
        if created or withdrawn or was_closed:
            self._set_project_status(issue, status)
        return IssueRef(issue["id"], issue["html_url"], created, issue.get("body") or "")

    def link(self, parent: IssueRef, child: IssueRef) -> None:
        parent_number = int(parent.url.rstrip("/").split("/")[-1])
        subissues = self.rest(
            "GET", f"/repos/{self.repository}/issues/{parent_number}/sub_issues?per_page=100"
        )
        if not any(issue["id"] == child.id for issue in subissues):
            self.rest(
                "POST",
                f"/repos/{self.repository}/issues/{parent_number}/sub_issues",
                {"sub_issue_id": child.id},
            )


class TrelloAdapter:
    def __init__(self, config: dict[str, Any], repository: str, api: JsonApi):
        self.config = config
        self.repository = repository
        self.api = api
        self.key = os.environ.get("TRELLO_API_KEY", "")
        self.token = os.environ.get("TRELLO_TOKEN", "")
        self.base = "https://api.trello.com/1"
        self.cards: dict[str, dict[str, Any]] = {}
        self.boards: dict[str, dict[str, Any]] = {}

    def board_for(self, kind: str) -> str:
        implementation = self.config.get("implementationBoardId", "")
        if implementation and kind in IMPLEMENTATION_KINDS:
            return implementation
        return self.config["boardId"]

    def call(self, method: str, path: str, data: dict[str, Any] | None = None) -> Any:
        separator = "&" if "?" in path else "?"
        url = f"{self.base}{path}{separator}" + urllib.parse.urlencode({"key": self.key, "token": self.token})
        return self.api.request(method, url, data=data)

    def preflight(self, statuses: dict[str, str]) -> None:
        if not self.key or not self.token:
            fail("TRELLO_API_KEY and TRELLO_TOKEN must not be empty")
        marker_prefix = re.escape(f"<!-- repofactory:artifact:{self.repository}:")
        marker_pattern = re.compile(marker_prefix + r"(.+) -->")
        board_kinds: dict[str, set[str]] = {}
        for kind in ARTIFACT_KINDS:
            board_kinds.setdefault(self.board_for(kind), set()).add(kind)
        for board, kinds in board_kinds.items():
            context = {"lists": {}, "labels": {}}
            self.boards[board] = context
            lists = self.call("GET", f"/boards/{board}/lists?filter=all")
            by_name: dict[str, list[str]] = {}
            for item in lists:
                if not item.get("closed"):
                    by_name.setdefault(item["name"], []).append(item["id"])
            required = {statuses[kind] for kind in kinds if kind in statuses} | {statuses["withdrawn"]}
            missing = []
            for status in required:
                matches = by_name.get(status, [])
                if len(matches) != 1:
                    missing.append(status)
                else:
                    context["lists"][status] = matches[0]
            if missing:
                fail(f"The Trello board {board} needs one open list for each status: " + ", ".join(sorted(missing)))
            board_labels = self.call("GET", f"/boards/{board}/labels?limit=1000&fields=id,name,color")
            by_label: dict[str, list[dict[str, Any]]] = {}
            for label in board_labels:
                if label.get("name", "").startswith(LABEL_PREFIX):
                    by_label.setdefault(label["name"], []).append(label)
            for name, matches in by_label.items():
                if len(matches) > 1:
                    fail(f"The Trello board {board} has duplicate managed labels named {name}")
                context["labels"][name] = matches[0]
            for kind in kinds:
                name = type_label(kind)
                matches = by_label.get(name, [])
                context["labels"][name] = matches[0] if matches else self.call(
                    "POST", "/labels", {"name": name, "color": TRELLO_LABEL_COLORS[kind], "idBoard": board}
                )
            cards = self.call("GET", f"/boards/{board}/cards?filter=all&fields=id,name,desc,url,shortUrl,closed,idLabels,idBoard")
            for card in cards:
                card.setdefault("idBoard", board)
                match = marker_pattern.search(card.get("desc") or "")
                if match:
                    path = match.group(1)
                    if path in self.cards:
                        fail(f"Two Trello cards have the artifact marker for {path}")
                    self.cards[path] = card

    def lookup(self, path: str) -> IssueRef | None:
        card = self.cards.get(path)
        if card is None:
            return None
        return IssueRef(card["id"], card.get("shortUrl") or card["url"], False, card.get("desc") or "")

    def upsert(
        self,
        artifact: Artifact,
        title: str,
        body: str,
        status: str,
        old_path: str = "",
        withdrawn: bool = False,
    ) -> IssueRef:
        card = self.cards.get(old_path or artifact.path) or self.cards.get(artifact.path)
        created = card is None
        was_closed = bool(card and card.get("closed"))
        board = self.board_for(artifact.kind)
        context = self.boards[board]
        moving = bool(card and card.get("idBoard") != board)
        payload = {"name": title, "desc": body, "closed": withdrawn}
        if created or withdrawn or was_closed or moving:
            payload["idList"] = context["lists"][status]
        if moving:
            payload["idBoard"] = board
        if created:
            card = self.call("POST", "/cards", payload)
        else:
            card = self.call("PUT", f"/cards/{card['id']}", payload)
        wanted = context["labels"][type_label(artifact.kind)]["id"]
        managed = {
            label["id"]
            for board_context in self.boards.values()
            for label in board_context["labels"].values()
        }
        current = set(card.get("idLabels", []))
        for label_id in sorted((current & managed) - {wanted}):
            self.call("DELETE", f"/cards/{card['id']}/idLabels/{label_id}")
        if wanted not in current:
            self.call("POST", f"/cards/{card['id']}/idLabels", {"value": wanted})
        card["idLabels"] = sorted((current - managed) | {wanted})
        card["idBoard"] = board
        if old_path and old_path != artifact.path:
            self.cards.pop(old_path, None)
        self.cards[artifact.path] = card
        return IssueRef(card["id"], card.get("shortUrl") or card["url"], created, card.get("desc") or body)

    def link(self, parent: IssueRef, child: IssueRef) -> None:
        checklists = self.call("GET", f"/cards/{parent.id}/checklists?checkItems=all")
        checklist = next((item for item in checklists if item["name"] == "Children"), None)
        if checklist is None:
            checklist = self.call("POST", f"/cards/{parent.id}/checklists", {"name": "Children"})
            checklist["checkItems"] = []
        if not any(child.url in item["name"] for item in checklist.get("checkItems", [])):
            self.call(
                "POST",
                f"/checklists/{checklist['id']}/checkItems",
                {"name": f"{child.url}", "pos": "bottom"},
            )


class Synchronizer:
    def __init__(
        self,
        config: dict[str, Any],
        event: dict[str, Any],
        api: JsonApi | None = None,
        adapter: Any | None = None,
    ):
        self.config = config
        self.event = event
        self.repository = os.environ["GITHUB_REPOSITORY"]
        self.server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        repository_data = event.get("repository", {})
        self.default_branch = repository_data.get("default_branch", "main")
        pull_request = event.get("pull_request") or {}
        self.commit_sha = pull_request.get("merge_commit_sha") or os.environ.get("GITHUB_SHA", self.default_branch)
        self.pull_request_url = pull_request.get("html_url", "")
        self.statuses = config["statuses"]
        api = api or JsonApi()
        if adapter is not None:
            self.adapter = adapter
        elif config["provider"] == "github-projects":
            self.adapter = GitHubAdapter(config["githubProjects"], self.repository, api)
        elif config["provider"] == "trello":
            self.adapter = TrelloAdapter(config["trello"], self.repository, api)
        else:
            fail(f"Unsupported provider: {config['provider']}")
        self.refs: dict[str, IssueRef] = {}
        self.results: list[tuple[str, str]] = []

    def make_body(self, artifact: Artifact, parent: IssueRef | None = None) -> str:
        return artifact_body(
            artifact,
            self.repository,
            self.server_url,
            self.default_branch,
            self.commit_sha,
            self.pull_request_url,
            parent.url if parent else "",
        )

    def sync_path(self, path: str, old_path: str = "", ensure_only: bool = False) -> IssueRef | None:
        artifact = classify_artifact(path)
        if artifact is None:
            return None
        if path in self.refs:
            return self.refs[path]
        if ensure_only:
            existing = self.adapter.lookup(path)
            if existing is not None:
                self.refs[path] = existing
                return existing
        parent = None
        if artifact.parent:
            parent = self.sync_path(artifact.parent, ensure_only=True)
            if parent is None:
                fail(f"Parent artifact is not supported: {artifact.parent}")
        title = artifact_title(path)
        status = self.statuses[artifact.kind]
        ref = self.adapter.upsert(artifact, title, self.make_body(artifact, parent), status, old_path)
        self.refs[path] = ref
        if parent:
            self.adapter.link(parent, ref)
        self.results.append((path, ref.url))
        return ref

    def withdraw_path(self, path: str) -> IssueRef | None:
        artifact = classify_artifact(path)
        if artifact is None:
            return None
        parent = self.adapter.lookup(artifact.parent) if artifact.parent else None
        title = f"{artifact_title(path)} [Withdrawn]"
        ref = self.adapter.upsert(
            artifact,
            title,
            self.make_body(artifact, parent),
            self.statuses["withdrawn"],
            withdrawn=True,
        )
        self.results.append((path, ref.url))
        return ref

    def changed_files(self) -> list[dict[str, Any]]:
        pull_request = self.event.get("pull_request")
        if not pull_request:
            return [
                {"filename": path.as_posix(), "status": "modified"}
                for path in sorted(ARTIFACT_ROOT.glob("feat-*/**/*.md"))
            ]
        api = self.adapter.api
        api_url = os.environ.get("GITHUB_API_URL", "https://api.github.com")
        token = os.environ.get("GITHUB_TOKEN", "")
        number = pull_request["number"]
        files: list[dict[str, Any]] = []
        page = 1
        while True:
            batch = api.request(
                "GET",
                f"{api_url}/repos/{self.repository}/pulls/{number}/files?per_page=100&page={page}",
                token,
                headers={"X-GitHub-Api-Version": "2022-11-28"},
            )
            files.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return files

    def run(self) -> None:
        changes = self.changed_files()
        unsupported = sorted(
            {
                path
                for item in changes
                for path in (item.get("filename", ""), item.get("previous_filename", ""))
                if is_feature_markdown(path) and classify_artifact(path) is None
            }
        )
        if unsupported:
            fail("Unsupported feature artifact paths: " + ", ".join(unsupported))
        relevant = [
            item
            for item in changes
            if classify_artifact(item["filename"]) is not None
            or classify_artifact(item.get("previous_filename", "")) is not None
        ]
        if not relevant:
            print("No accepted feature artifacts need synchronization")
            return
        self.adapter.preflight(self.statuses)
        for item in sorted(relevant, key=lambda value: value["filename"].count("/")):
            status = item["status"]
            if status == "removed":
                self.withdraw_path(item["filename"])
            elif status == "renamed":
                self.sync_path(item["filename"], item.get("previous_filename", ""))
            else:
                self.sync_path(item["filename"])
        if self.pull_request_url and self.results:
            self.comment_on_pull_request()

    def comment_on_pull_request(self) -> None:
        number = self.event["pull_request"]["number"]
        lines = [MANAGED_COMMENT, "Accepted artifact issues:", ""]
        lines.extend(f"- [`{path}`]({url})" for path, url in sorted(set(self.results)))
        body = "\n".join(lines)
        api_url = os.environ.get("GITHUB_API_URL", "https://api.github.com")
        token = os.environ["GITHUB_TOKEN"]
        comments = self.adapter.api.request(
            "GET", f"{api_url}/repos/{self.repository}/issues/{number}/comments?per_page=100", token
        )
        managed = next((comment for comment in comments if MANAGED_COMMENT in (comment.get("body") or "")), None)
        if managed:
            self.adapter.api.request(
                "PATCH", f"{api_url}/repos/{self.repository}/issues/comments/{managed['id']}", token, {"body": body}
            )
        else:
            self.adapter.api.request(
                "POST", f"{api_url}/repos/{self.repository}/issues/{number}/comments", token, {"body": body}
            )


def main() -> int:
    try:
        script_dir = Path(__file__).resolve().parent
        config_path = Path(os.environ.get("ARTIFACT_ISSUES_CONFIG", script_dir / "config.json"))
        event_path = Path(os.environ["GITHUB_EVENT_PATH"])
        config = json.loads(config_path.read_text())
        event = json.loads(event_path.read_text())
        pull_request = event.get("pull_request")
        if pull_request and not pull_request.get("merged"):
            print("The pull request did not merge; no artifact issue will change")
            return 0
        Synchronizer(config, event).run()
    except (KeyError, OSError, RuntimeError, ValueError) as error:
        print(f"accepted-artifact-issues: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
