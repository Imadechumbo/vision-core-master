from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(slots=True)
class ValidationGateStatus:
    name: str
    passed: bool
    detail: str = ""


@dataclass(slots=True)
class PullRequestValidationResult:
    mission_id: str
    status: str
    merge_allowed: bool
    checks: list[ValidationGateStatus] = field(default_factory=list)
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data


@dataclass(slots=True)
class GitHubIntegrationResult:
    status: str
    enabled: bool
    branch: str | None = None
    commit_sha: str | None = None
    pr_number: int | None = None
    pr_url: str | None = None
    push_performed: bool = False
    auto_merge_attempted: bool = False
    auto_merge_completed: bool = False
    reason: str = ""
    error_class: str = ""
    attempts: int = 0
    reused_pull_request: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CodexExportResult:
    status: str
    bundle_path: str | None = None
    files_exported: int = 0
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class IntegrationResult:
    mission_id: str
    status: str
    codex: CodexExportResult
    pr_validation: PullRequestValidationResult
    github: GitHubIntegrationResult
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "status": self.status,
            "codex": self.codex.to_dict(),
            "pr_validation": self.pr_validation.to_dict(),
            "github": self.github.to_dict(),
            "metadata": self.metadata,
        }
