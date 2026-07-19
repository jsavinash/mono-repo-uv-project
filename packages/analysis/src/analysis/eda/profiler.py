"""Data profiling — automated summary statistics, distributions, and correlations.

Produces a structured :class:`ProfileResult` dictionary that can be rendered
into reports or inspected programmatically.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from analysis.core.base import BaseAnalyzer
from analysis.core.types import CorrelationMethod, ProfileResult


class DataProfiler(BaseAnalyzer):
    """Generate a comprehensive profile of a DataFrame.

    Args:
        correlation_method: Correlation algorithm — ``"pearson"``,
            ``"spearman"``, or ``"kendall"`` (default ``"pearson"``).
        percentiles: Quantiles to include in summary stats
            (default ``[0.25, 0.5, 0.75]``).
        name: Optional analyzer name.

    Example::

        profiler = DataProfiler(correlation_method="spearman")
        profile = profiler.fit_analyze(df)
        print(profile["summary_stats"])
    """

    def __init__(
        self,
        *,
        correlation_method: CorrelationMethod = "pearson",
        percentiles: list[float] | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self._correlation_method = correlation_method
        self._percentiles = percentiles or [0.25, 0.5, 0.75]

    def fit(self, df: pd.DataFrame) -> "DataProfiler":
        """No learned state needed — returns self."""
        self._is_fitted = True
        return self

    def analyze(self, df: pd.DataFrame) -> dict[str, Any]:
        """Run the full profiling suite.

        Returns a :class:`ProfileResult` with keys:
            - ``shape``: Tuple of (rows, columns).
            - ``dtypes``: Series of column dtypes.
            - ``missing_counts``: Count of nulls per column.
            - ``missing_pct``: Percentage of nulls per column.
            - ``unique_counts``: Unique value counts per column.
            - ``summary_stats``: Descriptive statistics for numeric columns.
            - ``categorical_stats``: Value counts for categorical columns.
            - ``correlations``: Correlation matrix for numeric columns.
            - ``memory_usage``: Memory usage per column in bytes.
            - ``constant_columns``: Columns with only one unique value.
            - ``high_cardinality``: Columns with unique ratio > 0.9.
        """
        numeric_df = df.select_dtypes(include=[np.number])
        categorical_df = df.select_dtypes(include=["object", "category"])

        missing_counts = df.isnull().sum()
        unique_counts = df.nunique()

        return ProfileResult(
            shape=df.shape,
            dtypes=df.dtypes.astype(str).to_dict(),
            missing_counts=missing_counts.to_dict(),
            missing_pct=(missing_counts / len(df) * 100).round(2).to_dict(),
            unique_counts=unique_counts.to_dict(),
            summary_stats=self._summary_stats(numeric_df),
            categorical_stats=self._categorical_stats(categorical_df),
            correlations=self._correlations(numeric_df),
            memory_usage=df.memory_usage(deep=True).to_dict(),
            constant_columns=unique_counts[unique_counts <= 1].index.tolist(),
            high_cardinality=[
                col
                for col in df.columns
                if unique_counts[col] / max(len(df), 1) > 0.9
            ],
        )

    # -- Helpers ------------------------------------------------------------

    def _summary_stats(self, numeric_df: pd.DataFrame) -> dict[str, Any]:
        if numeric_df.empty:
            return {}
        desc = numeric_df.describe(percentiles=self._percentiles)
        # Add skewness and kurtosis
        desc.loc["skewness"] = numeric_df.skew()
        desc.loc["kurtosis"] = numeric_df.kurtosis()
        return desc.to_dict()

    def _categorical_stats(self, cat_df: pd.DataFrame) -> dict[str, Any]:
        if cat_df.empty:
            return {}
        stats: dict[str, Any] = {}
        for col in cat_df.columns:
            vc = cat_df[col].value_counts()
            stats[col] = {
                "top_values": vc.head(10).to_dict(),
                "unique_count": int(cat_df[col].nunique()),
                "mode": vc.index[0] if not vc.empty else None,
            }
        return stats

    def _correlations(self, numeric_df: pd.DataFrame) -> dict[str, dict[str, float]]:
        if numeric_df.shape[1] < 2:
            return {}
        corr = numeric_df.corr(method=self._correlation_method)
        return corr.to_dict()  # type: ignore[return-value]
