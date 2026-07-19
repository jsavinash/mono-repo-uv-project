import json
from pathlib import Path
import subprocess
import sys

from core import MigrationManager, MigrationStep


def test_create_and_apply_plan(tmp_path: Path) -> None:
    manager = MigrationManager("demo", base_dir=tmp_path)
    plan = manager.create_plan("demo-plan")
    plan.add_step(
        MigrationStep(
            name="create-users",
            operation="create_table",
            description="create users table",
        )
    )
    plan.add_step(
        MigrationStep(
            name="seed-users", operation="insert", description="seed user data"
        )
    )

    assert manager.list_plans() == ["demo-plan"]
    applied_steps = manager.apply_plan(plan)
    assert [step.name for step in applied_steps] == ["create-users", "seed-users"]

    output_path = manager.build_plan_file(plan)
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert output_path.exists()
    assert payload["name"] == "demo-plan"
    assert payload["steps"][0]["name"] == "create-users"


def test_describe_plan() -> None:
    manager = MigrationManager("demo")
    plan = manager.create_plan("empty-plan")

    assert manager.describe(plan) == "Plan 'empty-plan' has no steps."


def test_migration_cli_generates_plan(tmp_path: Path) -> None:
    output_path = tmp_path / "plan.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "cli.src.cli.migrations",
            "--name",
            "cli-plan",
            "--output",
            str(output_path),
            "--step",
            "create-users:create_table:create users table",
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "cli-plan" in completed.stdout
    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["name"] == "cli-plan"
    assert payload["steps"][0]["name"] == "create-users"
