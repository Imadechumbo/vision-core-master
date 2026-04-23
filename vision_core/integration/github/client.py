from __future__ import annotations

import json
import urllib.parse
import urllib.request


class GitHubApiError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}"

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict | list:
        url = f"{self.base_url}{path}"
        body = None
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except Exception as exc:  # pragma: no cover - external network path
            raise GitHubApiError(str(exc)) from exc

    def create_pull_request(self, title: str, head: str, base: str, body: str) -> dict:
        return self._request("POST", "/pulls", {"title": title, "head": head, "base": base, "body": body})

    def find_open_pull_request(self, head: str, base: str) -> dict | None:
        query = urllib.parse.urlencode({"state": "open", "head": f"{self.repo.split('/')[0]}:{head}", "base": base})
        result = self._request("GET", f"/pulls?{query}")
        if isinstance(result, list) and result:
            return result[0]
        return None

    def create_or_reuse_pull_request(self, title: str, head: str, base: str, body: str) -> tuple[dict, bool]:
        existing = self.find_open_pull_request(head=head, base=base)
        if existing is not None:
            return existing, True
        return self.create_pull_request(title=title, head=head, base=base, body=body), False

    def get_pull_request(self, pr_number: int) -> dict:
        return self._request("GET", f"/pulls/{pr_number}")

    def merge_pull_request(self, pr_number: int, commit_title: str) -> dict:
        return self._request("PUT", f"/pulls/{pr_number}/merge", {"merge_method": "squash", "commit_title": commit_title})
