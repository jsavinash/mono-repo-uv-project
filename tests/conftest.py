"""Root-level test configuration for the monorepo."""

from pathlib import Path
import sys


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    return start


ROOT = _find_repo_root(Path(__file__).resolve())

# Add key package paths so root-level tests can import workspace packages
for path in [
    ROOT,
    ROOT / "libs/shared/src",
]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
