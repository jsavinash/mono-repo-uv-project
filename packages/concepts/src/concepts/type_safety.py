from abc import ABC, abstractmethod
from typing import Protocol, override, runtime_checkable


# 1. THE PROTOCOL: Defines what behavior is expected (Structural)
@runtime_checkable
class PaymentProcessor(Protocol):
    def process(self, amount: float) -> str: ...


# 2. THE ABC: Defines shared implementation/structure (Nominal)
class BaseProcessor(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def process(self, amount: float) -> str:
        pass


# 3. CONCRETE IMPLEMENTATION: Inherits from ABC, satisfies Protocol
class StripeProcessor(BaseProcessor):
    @override
    def process(self, amount: float) -> str:
        return f"Processing ${amount} via Stripe with {self.api_key}"


class PayPalProcessor(BaseProcessor):
    @override
    def process(self, amount: float) -> str:
        return f"Processing ${amount} via PayPal with {self.api_key}"


# 4. USAGE: Function accepts the Protocol, not the ABC
def checkout(processor: BaseProcessor, amount: float) -> None:
    print(processor.process(amount))


# Valid usage
stripe = StripeProcessor("sk_123")
paypal = PayPalProcessor("pp_456")

checkout(stripe, 100.0)
checkout(paypal, 50.0)
