"""Missing value handling with pluggable strategies.

Supports per-column strategy overrides and threshold-based dropping.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.core.base import BaseTransformer
from analysis.core.exceptions import ConfigurationError
from analysis.core.types import CleaningResult

_VALID_STRATEGIES = frozenset(
    {"drop", "fill_mean", "fill_median", "fill_mode", "fill_constant", "interpolate"}
)


class MissingValueHandler(BaseTransformer):
    """Handle missing values using a configurable strategy.

    Args:
        strategy: Default strategy for all columns. One of:
            ``"drop"``, ``"fill_mean"``, ``"fill_median"``, ``"fill_mode"``,
            ``"fill_constant"``, ``"interpolate"``.
        fill_value: Value used when ``strategy="fill_constant"``.
        column_strategies: Per-column strategy overrides, e.g.
            ``{"age": "fill_median", "name": "fill_constant"}``.
        row_threshold: Drop rows with more than this fraction of nulls (0.0–1.0).
        column_threshold: Drop columns with more than this fraction of nulls (0.0–1.0).

    Example::

        handler = MissingValueHandler(
            strategy="fill_median",
            column_strategies={"category": "fill_mode"},
            column_threshold=0.5,
        )
        clean_df = handler.fit_transform(df)
    """

    def __init__(
        self,
        *,
        strategy: str = "fill_median",
        fill_value: Any = None,
        column_strategies: dict[str, str] | None = None,
        row_threshold: float | None = None,
        column_threshold: float | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        if strategy not in _VALID_STRATEGIES:
            raise ConfigurationError(
                f"Unknown strategy {strategy!r}. Valid: {sorted(_VALID_STRATEGIES)}"
            )
        self._strategy = strategy
        self._fill_value = fill_value
        self._column_strategies = column_strategies or {}
        self._row_threshold = row_threshold
        self._column_threshold = column_threshold
        self._fill_values: dict[str, Any] = {}
        self._last_result: CleaningResult | None = None

    # -- Fit ----------------------------------------------------------------

    def fit(self, df: pd.DataFrame) -> "MissingValueHandler":
        """Learn fill values from the data (mean, median, mode per column)."""
        for col in df.columns:
            strategy = self._column_strategies.get(col, self._strategy)
            self._fill_values[col] = self._compute_fill(df[col], strategy)
        self._is_fitted = True
        return self

    def _compute_fill(self, series: pd.Series, strategy: str) -> Any:  # type: ignore[type-arg]
        if strategy == "fill_mean":
            return series.mean() if pd.api.types.is_numeric_dtype(series) else series.mode().iloc[0] if not series.mode().empty else None
        if strategy == "fill_median":
            return series.median() if pd.api.types.is_numeric_dtype(series) else series.mode().iloc[0] if not series.mode().empty else None
        if strategy == "fill_mode":
            mode = series.mode()
            return mode.iloc[0] if not mode.empty else None
        if strategy == "fill_constant":
            return self._fill_value
        return None  # strategies that don't need a precomputed value

    # -- Transform ----------------------------------------------------------

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the missing-value strategy to produce a cleaned DataFrame."""
        original_shape = df.shape
        result = df.copy()
        actions: list[str] = []

        # 1. Drop columns above threshold
        if self._column_threshold is not None:
            col_null_pct = result.isnull().mean()
            drop_cols = col_null_pct[col_null_pct > self._column_threshold].index.tolist()
            if drop_cols:
                result = result.drop(columns=drop_cols)
                actions.append(f"Dropped {len(drop_cols)} column(s) above {self._column_threshold:.0%} null threshold")

        # 2. Drop rows above threshold
        if self._row_threshold is not None:
            row_null_pct = result.isnull().mean(axis=1)
            mask = row_null_pct <= self._row_threshold
            dropped = int((~mask).sum())
            result = result.loc[mask].reset_index(drop=True)
            if dropped:
                actions.append(f"Dropped {dropped} row(s) above {self._row_threshold:.0%} null threshold")

        # 3. Apply per-column strategies
        for col in result.columns:
            if not result[col].isnull().any():
                continue
            strategy = self._column_strategies.get(col, self._strategy)
            if strategy == "drop":
                before = len(result)
                result = result.dropna(subset=[col]).reset_index(drop=True)
                actions.append(f"Dropped {before - len(result)} row(s) with null in '{col}'")
            elif strategy == "interpolate":
                result[col] = result[col].interpolate()
                actions.append(f"Interpolated nulls in '{col}'")
            elif strategy.startswith("fill_"):
                fill = self._fill_values.get(col)
                if fill is not None:
                    result[col] = result[col].fillna(fill)
                    actions.append(f"Filled nulls in '{col}' with {fill!r}")

        self._last_result = CleaningResult(
            original_shape=original_shape,
            cleaned_shape=result.shape,
            rows_removed=original_shape[0] - result.shape[0],
            columns_modified=list(result.columns),
            actions_taken=actions,
        )
        return result

    @property
    def result(self) -> CleaningResult | None:
        """Access the result metadata from the last transform call."""
        return self._last_result
