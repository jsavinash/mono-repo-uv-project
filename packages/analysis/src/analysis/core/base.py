"""Abstract base classes that define the contract for all analysis components."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class BaseAnalyzer(ABC):
    """Abstract base class for all analyzers.

    An analyzer inspects data and produces insights without modifying it.
    Subclasses must implement ``fit`` and ``analyze``.

    Example::

        class MyAnalyzer(BaseAnalyzer):
            def fit(self, df: pd.DataFrame) -> "MyAnalyzer":
                self._stats = df.describe()
                return self

            def analyze(self, df: pd.DataFrame) -> dict[str, Any]:
                return {"stats": self._stats}
    """

    def __init__(self, name: str | None = None) -> None:
        self.name: str = name or self.__class__.__name__
        self._is_fitted: bool = False

    @abstractmethod
    def fit(self, df: pd.DataFrame) -> BaseAnalyzer:
        """Learn parameters from the data.

        Args:
            df: Input DataFrame to learn from.

        Returns:
            self, for method chaining.
        """

    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> dict[str, Any]:
        """Run the analysis and return results.

        Args:
            df: Input DataFrame to analyze.

        Returns:
            Dictionary of analysis results.
        """

    def fit_analyze(self, df: pd.DataFrame) -> dict[str, Any]:
        """Convenience method: fit then analyze in one call.

        Args:
            df: Input DataFrame.

        Returns:
            Dictionary of analysis results.
        """
        self.fit(df)
        return self.analyze(df)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"


class BaseTransformer(ABC):
    """Abstract base class for all data transformers.

    A transformer modifies data (e.g., cleaning, encoding, scaling).
    Subclasses must implement ``fit`` and ``transform``.
    """

    def __init__(self, name: str | None = None) -> None:
        self.name: str = name or self.__class__.__name__
        self._is_fitted: bool = False

    @abstractmethod
    def fit(self, df: pd.DataFrame) -> BaseTransformer:
        """Learn parameters from the data.

        Args:
            df: Input DataFrame to learn from.

        Returns:
            self, for method chaining.
        """

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the transformation to the data.

        Args:
            df: Input DataFrame to transform.

        Returns:
            Transformed DataFrame.
        """

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convenience method: fit then transform in one call.

        Args:
            df: Input DataFrame.

        Returns:
            Transformed DataFrame.
        """
        self.fit(df)
        return self.transform(df)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"


class BasePipeline(ABC):
    """Abstract base class for composable analysis pipelines.

    A pipeline chains multiple steps and executes them sequentially.
    """

    def __init__(self, name: str | None = None) -> None:
        self.name: str = name or self.__class__.__name__
        self._steps: list[tuple[str, BaseAnalyzer | BaseTransformer]] = []

    @abstractmethod
    def add_step(
        self,
        name: str,
        step: BaseAnalyzer | BaseTransformer,
    ) -> BasePipeline:
        """Add a named step to the pipeline.

        Args:
            name: Unique step identifier.
            step: An analyzer or transformer instance.

        Returns:
            self, for method chaining.
        """

    @abstractmethod
    def run(self, df: pd.DataFrame) -> dict[str, Any]:
        """Execute the full pipeline on the given DataFrame.

        Args:
            df: Input DataFrame.

        Returns:
            Dictionary containing results from each step.
        """

    def __len__(self) -> int:
        return len(self._steps)

    def __repr__(self) -> str:
        step_names = [name for name, _ in self._steps]
        return f"{self.__class__.__name__}(name={self.name!r}, steps={step_names})"
