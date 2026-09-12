from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class CheckResult:
    # The verdict on one check, with enough detail to act on it.
    name: str
    passed: bool
    message: str = "" # for humans
    detail: Mapping[str, object] = field(default_factory=dict) # for validation.json

    def as_json(self) -> dict[str, object]:
        # The validation.json record: passed alongside the detail fields.
        record: dict[str, object] = {"passed": self.passed, **self.detail}
        if not self.passed:
            record["message"] = self.message
        return record
