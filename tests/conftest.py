from pathlib import Path
import sys


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    return start


ROOT = _find_repo_root(Path(__file__).resolve())
SERVICE_ROOT = ROOT / "apps" / "micro-services" / "item"
SERVICE_PARENT = SERVICE_ROOT.parent
for path in [
    ROOT,
    ROOT / "packages/core/src",
    ROOT / "libs/shared/src",
    SERVICE_ROOT,
    SERVICE_PARENT,
]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
