from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
for path in [ROOT, ROOT / "packages/core/src", ROOT / "libs/shared/src"]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
