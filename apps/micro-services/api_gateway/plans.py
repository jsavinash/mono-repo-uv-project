from pathlib import Path
import sys

from fastapi import APIRouter

sys.path.append(str(Path(__file__).resolve().parents[2] / "libs/shared/src"))

from shared.contracts import ProductPlan

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("/")
def list_plans() -> list[ProductPlan]:
    return [
        ProductPlan(name="Starter", price_monthly=19, description="For solo builders"),
        ProductPlan(name="Scale", price_monthly=79, description="For growing teams"),
    ]
