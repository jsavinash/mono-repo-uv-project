from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
for path in [ROOT, ROOT / "packages/core/src", ROOT / "libs/shared/src"]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from core import MigrationManager, MigrationStep


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage migration plans")
    parser.add_argument("--name", default="default", help="Name for the migration plan")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output JSON path for the generated plan",
    )
    parser.add_argument(
        "--step",
        action="append",
        default=[],
        help="A migration step in the form name:operation:description",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    manager = MigrationManager("repo-cli", base_dir=Path.cwd())
    plan = manager.create_plan(args.name)

    for raw_step in args.step:
        if ":" not in raw_step:
            raise ValueError(f"Invalid step format: {raw_step}")
        name, operation, *rest = raw_step.split(":", 2)
        description = rest[0] if rest else ""
        plan.add_step(
            MigrationStep(name=name, operation=operation, description=description)
        )

    output_path = manager.build_plan_file(plan, args.output)
    print(json.dumps({"plan": plan.name, "output": str(output_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
