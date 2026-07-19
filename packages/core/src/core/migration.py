from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class MigrationStep:
    """Represents a single database migration operation."""

    name: str
    operation: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MigrationPlan:
    """A simple, serializable plan of migration steps."""

    name: str
    steps: list[MigrationStep] = field(default_factory=list)

    def add_step(self, step: MigrationStep) -> None:
        self.steps.append(step)


class MigrationManager:
    """A lightweight migration manager for repository-level workflows.

    The implementation is intentionally dependency-light so it can be used by
    services that need a predictable migration interface without pulling in a
    full migration framework.
    """

    def __init__(self, plan_name: str, base_dir: str | Path | None = None) -> None:
        self.plan_name = plan_name
        self.base_dir = Path(base_dir or ".").resolve()
        self._plans: dict[str, MigrationPlan] = {}

    def create_plan(self, name: str) -> MigrationPlan:
        plan = MigrationPlan(name=name)
        self._plans[name] = plan
        return plan

    def register_plan(self, plan: MigrationPlan) -> None:
        self._plans[plan.name] = plan

    def get_plan(self, name: str) -> MigrationPlan:
        return self._plans[name]

    def list_plans(self) -> list[str]:
        return sorted(self._plans)

    def build_plan_file(
        self, plan: MigrationPlan, output_path: str | Path | None = None
    ) -> Path:
        target = Path(output_path or self.base_dir / f"{plan.name}.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "name": plan.name,
            "steps": [
                {
                    "name": step.name,
                    "operation": step.operation,
                    "description": step.description,
                    "metadata": step.metadata,
                }
                for step in plan.steps
            ],
        }
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return target

    def apply_plan(self, plan: MigrationPlan) -> list[MigrationStep]:
        return list(plan.steps)

    def describe(self, plan: MigrationPlan) -> str:
        if not plan.steps:
            return f"Plan '{plan.name}' has no steps."

        details = [f"Plan '{plan.name}':"]
        for step in plan.steps:
            details.append(f"- {step.name}: {step.operation}")
        return "\n".join(details)
