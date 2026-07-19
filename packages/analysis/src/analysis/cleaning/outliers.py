"""Outlier detection and treatment.

Supports IQR, Z-score, Modified Z-score, and Isolation Forest methods with
configurable actions: flag, remove, clip, or transform.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from analysis.core.base import BaseTransformer
from analysis.core.exceptions import ConfigurationError
from analysis.core.types import CleaningResult

_VALID_METHODS = frozenset({"iqr", "zscore", "modified_zscore", "isolation_forest"})
_VALID_ACTIONS = frozenset({"flag", "remove", "clip", "transform"})


class OutlierDetector(BaseTransformer):
    """Detect and handle outliers in numeric columns.

    Args:
        method: Detection method — ``"iqr"``, ``"zscore"``,
            ``"modified_zscore"``, or ``"isolation_forest"``.
        action: What to do with outliers — ``"flag"`` (adds boolean column),
            ``"remove"``, ``"clip"`` (winsorise), or ``"transform"`` (log1p).
        threshold: Sensitivity threshold. Meaning depends on method:
            - IQR: multiplier (default 1.5)
            - Z-score / Modified Z-score: number of σ (default 3.0)
            - Isolation Forest: contamination fraction (default 0.05)
        columns: Specific columns to check. ``None`` means all numeric columns.
        name: Optional name for the transformer.

    Example::

        detector = OutlierDetector(method="iqr", action="clip", threshold=1.5)
        clean_df = detector.fit_transform(df)
    """

    def __init__(
        self,
        *,
        method: str = "iqr",
        action: str = "remove",
        threshold: float | None = None,
        columns: list[str] | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        if method not in _VALID_METHODS:
            raise ConfigurationError(
                f"Unknown method {method!r}. Valid: {sorted(_VALID_METHODS)}"
            )
        if action not in _VALID_ACTIONS:
            raise ConfigurationError(
                f"Unknown action {action!r}. Valid: {sorted(_VALID_ACTIONS)}"
            )
        self._method = method
        self._action = action
        self._threshold = threshold or self._default_threshold(method)
        self._columns = columns
        self._bounds: dict[str, tuple[float, float]] = {}
        self._last_result: CleaningResult | None = None

    @staticmethod
    def _default_threshold(method: str) -> float:
        return {
            "iqr": 1.5,
            "zscore": 3.0,
            "modified_zscore": 3.5,
            "isolation_forest": 0.05,
        }[method]

    # -- Fit ----------------------------------------------------------------

    def fit(self, df: pd.DataFrame) -> OutlierDetector:
        """Learn bounds / parameters from the data."""
        cols = self._resolve_columns(df)
        for col in cols:
            series = df[col].dropna()
            if self._method == "iqr":
                q1, q3 = float(series.quantile(0.25)), float(series.quantile(0.75))
                iqr = q3 - q1
                self._bounds[col] = (
                    q1 - self._threshold * iqr,
                    q3 + self._threshold * iqr,
                )
            elif self._method in ("zscore", "modified_zscore"):
                if self._method == "zscore":
                    mean, std = float(series.mean()), float(series.std())
                    self._bounds[col] = (
                        mean - self._threshold * std,
                        mean + self._threshold * std,
                    )
                else:
                    median = float(series.median())
                    mad = float(np.median(np.abs(series - median)))
                    mad = mad if mad > 0 else 1e-6
                    bound = self._threshold * 1.4826 * mad
                    self._bounds[col] = (median - bound, median + bound)
            # Isolation Forest doesn't use precomputed bounds
        self._is_fitted = True
        return self

    def _resolve_columns(self, df: pd.DataFrame) -> list[str]:
        if self._columns:
            return [c for c in self._columns if c in df.columns]
        return df.select_dtypes(include=[np.number]).columns.tolist()

    # -- Transform ----------------------------------------------------------

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply outlier treatment."""
        original_shape = df.shape
        result = df.copy()
        actions: list[str] = []
        cols = self._resolve_columns(df)

        if self._method == "isolation_forest":
            result, actions = self._apply_isolation_forest(result, cols)
        else:
            for col in cols:
                if col not in self._bounds:
                    continue
                lower, upper = self._bounds[col]
                outlier_mask = (result[col] < lower) | (result[col] > upper)
                n_outliers = int(outlier_mask.sum())
                if n_outliers == 0:
                    continue

                if self._action == "flag":
                    result[f"{col}_is_outlier"] = outlier_mask
                    actions.append(f"Flagged {n_outliers} outlier(s) in '{col}'")
                elif self._action == "remove":
                    result = result[~outlier_mask].reset_index(drop=True)
                    actions.append(f"Removed {n_outliers} outlier(s) in '{col}'")
                elif self._action == "clip":
                    result[col] = result[col].clip(lower=lower, upper=upper)
                    actions.append(
                        f"Clipped {n_outliers} outlier(s) in '{col}' to [{lower:.2f}, {upper:.2f}]"
                    )
                elif self._action == "transform":
                    result[col] = np.log1p(result[col].clip(lower=0))
                    actions.append(f"Log-transformed '{col}' ({n_outliers} outlier(s))")

        self._last_result = CleaningResult(
            original_shape=original_shape,
            cleaned_shape=result.shape,
            rows_removed=original_shape[0] - result.shape[0],
            columns_modified=cols,
            actions_taken=actions,
        )
        return result

    def _apply_isolation_forest(
        self, df: pd.DataFrame, cols: list[str]
    ) -> tuple[pd.DataFrame, list[str]]:
        from sklearn.ensemble import IsolationForest

        actions: list[str] = []
        numeric_data = df[cols].dropna()
        if numeric_data.empty:
            return df, actions

        clf = IsolationForest(contamination=self._threshold, random_state=42)
        preds = clf.fit_predict(numeric_data)
        outlier_mask = pd.Series(preds == -1, index=numeric_data.index)
        n_outliers = int(outlier_mask.sum())

        if self._action == "flag":
            df["is_outlier"] = False
            df.loc[outlier_mask.index, "is_outlier"] = outlier_mask
            actions.append(f"Flagged {n_outliers} outlier(s) via Isolation Forest")
        elif self._action == "remove":
            df = df.loc[~outlier_mask.reindex(df.index, fill_value=False)].reset_index(
                drop=True
            )
            actions.append(f"Removed {n_outliers} outlier(s) via Isolation Forest")

        return df, actions

    @property
    def result(self) -> CleaningResult | None:
        """Access the result metadata from the last transform call."""
        return self._last_result
