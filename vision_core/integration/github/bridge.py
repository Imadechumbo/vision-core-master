from __future__ import annotations
import os
import subprocess
import time
from pathlib import Path
from typing import Callable
from vision_core.integration.contracts import GitHubIntegrationResult, PullRequestValidationResult
from vision_core.integration.github.client import GitHubApiError, GitHubClient
class GitHubBridge:
    def __init__(self, repository_root: str | Path | None = None):
        configured_root = repository_root or os.getenv("VISION_REPO_ROOT") or os.getcwd()
        self.repository_root = Path(configured_root).resolve()
        self.token = os.getenv("GITHUB_TOKEN", "").strip()
        self.repo = os.getenv("GITHUB_REPO", "").strip()
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main").strip() or "main"
        self.auto_merge = os.getenv("VISION_AUTO_MERGE", "0").strip().lower() in {"1", "true", "yes", "on"}
        self.max_api_attempts = max(1, int(os.getenv("VISION_GITHUB_MAX_RETRIES", "3").strip() or "3"))
        self.retry_sleep_ms = max(0, int(os.getenv("VISION_GITHUB_RETRY_SLEEP_MS", "150").strip() or "150"))
    def enabled(self) -> bool:
        return bool(self.token and self.repo and (self.repository_root / ".git").exists())
    def get_debug_state(self) -> dict:
        return {
            "enabled": self.enabled(),
            "repository_root": str(self.repository_root),
            "repo": self.repo,
            "base_branch": self.base_branch,
            "auto_merge": self.auto_merge,
            "max_api_attempts": self.max_api_attempts,
        }
    def publish(self, data: dict, pr_validation: PullRequestValidationResult) -> GitHubIntegrationResult:
        if not pr_validation.merge_allowed:
            return GitHubIntegrationResult(
                status="blocked",
                enabled=self.enabled(),
                reason="PR validation blocked merge/promotion",
                error_class="blocked_validation",
                metadata={"engine": "GitHubBridge", "debug": self.get_debug_state()},
            )
        if not self.enabled():
            return GitHubIntegrationResult(
                status="skipped",
                enabled=False,
                reason="GitHub integration not configured or repository root is not a git repo",
                error_class="github_not_configured",
                metadata={"engine": "GitHubBridge", "debug": self.get_debug_state()},
            )
        branch = self._safe_branch_name(data["mission_id"])
        commit_message = f"VISION CORE {data['mission_id']}: {data['mission']}"
        attempts = 0
        try:
            base_ref = self._git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip() or self.base_branch
            self._checkout_branch(branch)
            self._git("add", ".")
            client = GitHubClient(self.token, self.repo)
            if not self._has_staged_changes():
                head_sha = self._git("rev-parse", "HEAD").stdout.strip()
                pr, reused = self._api_call(lambda: client.create_or_reuse_pull_request(
                    title=commit_message,
                    head=branch,
                    base=self.base_branch,
                    body=self._build_pr_body(data, pr_validation),
                ))
                attempts = self._last_attempts
                if pr:
                    return GitHubIntegrationResult(
                        status="noop",
                        enabled=True,
                        branch=branch,
                        commit_sha=head_sha,
                        pr_number=pr.get("number"),
                        pr_url=pr.get("html_url"),
                        push_performed=False,
                        reused_pull_request=bool(reused),
                        reason="Nenhuma alteração staged; PR existente reutilizado sem duplicação.",
                        error_class="noop_no_changes",
                        attempts=attempts,
                        metadata={"engine": "GitHubBridge", "debug": self.get_debug_state(), "base_ref": base_ref},
                    )
                return GitHubIntegrationResult(
                    status="noop",
                    enabled=True,
                    branch=branch,
                    commit_sha=head_sha,
                    push_performed=False,
                    reason="Nenhuma alteração staged para commit; GitHub publish abortado com segurança.",
                    error_class="noop_no_changes",
                    attempts=attempts,
                    metadata={"engine": "GitHubBridge", "debug": self.get_debug_state(), "base_ref": base_ref},
                )
            commit_proc = self._git("commit", "-m", commit_message, check=False)
            if commit_proc.returncode != 0:
                msg = commit_proc.stderr.strip() or commit_proc.stdout.strip() or "git commit failed"
                return GitHubIntegrationResult(
                    status="error",
                    enabled=True,
                    branch=branch,
                    reason=msg,
                    error_class=self._classify_error(msg),
                    metadata={"engine": "GitHubBridge", "debug": self.get_debug_state(), "base_ref": base_ref},
                )
            commit_sha = self._git("rev-parse", "HEAD").stdout.strip()
            push_proc = self._git("push", "-u", "origin", branch, check=False)
            push_performed = push_proc.returncode == 0
            push_error = push_proc.stderr.strip() or push_proc.stdout.strip()
            pr_url = None
            pr_number = None
            auto_merge_completed = False
            auto_merge_attempted = False
            reused_pull_request = False
            error_class = ""
            if push_performed:
                pr, reused_pull_request = self._api_call(lambda: client.create_or_reuse_pull_request(
                    title=commit_message,
                    head=branch,
                    base=self.base_branch,
                    body=self._build_pr_body(data, pr_validation),
                ))
                attempts = self._last_attempts
                pr_url = pr.get("html_url") if pr else None
                pr_number = pr.get("number") if pr else None
                if self.auto_merge and pr_number:
                    auto_merge_attempted = True
                    pr_state = self._api_call(lambda: client.get_pull_request(pr_number))
                    attempts = max(attempts, self._last_attempts)
                    if pr_state.get("state") != "open":
                        error_class = "merge_blocked_remote_state"
                    else:
                        merge_result = self._api_call(lambda: client.merge_pull_request(pr_number, commit_message))
                        attempts = max(attempts, self._last_attempts)
                        auto_merge_completed = bool(merge_result.get("merged"))
                        if not auto_merge_completed:
                            error_class = "merge_not_completed"
            reason = "GitHub flow executed"
            status = "completed"
            if not push_performed:
                reason = f"git push failed: {push_error}" if push_error else "git push failed"
                status = "error"
                error_class = self._classify_error(push_error)
            return GitHubIntegrationResult(
                status=status,
                enabled=True,
                branch=branch,
                commit_sha=commit_sha,
                pr_number=pr_number,
                pr_url=pr_url,
                push_performed=push_performed,
                auto_merge_attempted=auto_merge_attempted,
                auto_merge_completed=auto_merge_completed,
                reused_pull_request=reused_pull_request,
                reason=reason,
                error_class=error_class,
                attempts=attempts,
                metadata={"engine": "GitHubBridge", "debug": self.get_debug_state(), "base_ref": base_ref},
            )
        except (RuntimeError, GitHubApiError) as exc:
            message = str(exc)
            return GitHubIntegrationResult(
                status="error",
                enabled=True,
                branch=branch,
                reason=message,
                error_class=self._classify_error(message),
                attempts=attempts or getattr(self, "_last_attempts", 0),
                metadata={"engine": "GitHubBridge", "debug": self.get_debug_state()},
            )
    def _api_call(self, operation: Callable[[], object]) -> object:
        last_error = None
        self._last_attempts = 0
        for attempt in range(1, self.max_api_attempts + 1):
            self._last_attempts = attempt
            try:
                return operation()
            except GitHubApiError as exc:
                last_error = exc
                if not self._is_retryable_error(str(exc)) or attempt >= self.max_api_attempts:
                    raise
                if self.retry_sleep_ms:
                    time.sleep(self.retry_sleep_ms / 1000.0)
        if last_error is not None:
            raise last_error
        raise GitHubApiError("Unknown GitHub API execution failure")
    def _is_retryable_error(self, message: str) -> bool:
        text = (message or "").lower()
        retryable_tokens = ["timed out", "timeout", "temporary", "temporarily", "connection reset", "502", "503", "504", "rate limit"]
        return any(token in text for token in retryable_tokens)
    def _classify_error(self, message: str) -> str:
        text = (message or "").lower()
        if not text:
            return "unknown_error"
        if "authentication" in text or "bad credentials" in text or "unauthorized" in text or "403" in text:
            return "github_auth_error"
        if "rate limit" in text:
            return "github_rate_limited"
        if "timed out" in text or "timeout" in text or "temporary" in text or "502" in text or "503" in text or "504" in text:
            return "retryable_network_error"
        if "non-fast-forward" in text or "fetch first" in text or "rejected" in text:
            return "push_rejected"
        if "nothing to commit" in text:
            return "noop_no_changes"
        if "not a git repository" in text:
            return "invalid_repository"
        if "merge conflict" in text or "conflict" in text:
            return "merge_conflict"
        return "github_runtime_error"
    def _build_pr_body(self, data: dict, pr_validation: PullRequestValidationResult) -> str:
        lines = [
            "## VISION CORE AUTO PR",
            "",
            f"MISSION: {data['mission']}",
            f"MISSION_ID: {data['mission_id']}",
            f"ROOT_CAUSE: {data['diagnosis'].root_cause}",
            f"STRATEGY: {data['diagnosis'].strategy}",
            f"VALIDATION: {data['validation'].outcome}",
            f"PASS_GOLD: {data['validation'].pass_gold}",
            f"PROMOTION_ALLOWED: {data['security'].promotion_allowed}",
            "",
            "### PR Validation",
        ]
        for item in pr_validation.checks:
            mark = "PASS" if item.passed else "BLOCK"
            lines.append(f"- {item.name}: {mark} — {item.detail}")
        return "\n".join(lines)
    def _safe_branch_name(self, mission_id: str) -> str:
        return f"vision/{mission_id}".replace(" ", "-")
    def _checkout_branch(self, branch: str) -> None:
        if self._branch_exists(branch):
            self._git("checkout", branch)
            return
        self._git("checkout", "-b", branch)
    def _branch_exists(self, branch: str) -> bool:
        probe = self._git("rev-parse", "--verify", branch, check=False)
        return probe.returncode == 0
    def _has_staged_changes(self) -> bool:
        probe = self._git("diff", "--cached", "--quiet", check=False)
        return probe.returncode == 1
    def _git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        completed = subprocess.run(
            ["git", *args],
            cwd=self.repository_root,
            text=True,
            capture_output=True,
        )
        if check and completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or f"git {' '.join(args)} failed")
        return completed
