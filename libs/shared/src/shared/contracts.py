from dataclasses import dataclass


@dataclass(frozen=True)
class AppFeature:
    title: str
    description: str


@dataclass(frozen=True)
class ProductPlan:
    name: str
    price_monthly: int
    description: str
