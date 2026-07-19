"""Shared type aliases, NewTypes, and TypedDict definitions for the analysis package."""

from __future__ import annotations

from pathlib import Path
from typing import Any, NewType, TypeAlias

import numpy as np
import numpy.typing as npt
import pandas as pd

# ---------------------------------------------------------------------------
# Core pandas / numpy aliases
# ---------------------------------------------------------------------------
DataFrame: TypeAlias = pd.DataFrame
Series: TypeAlias = pd.Series  # type: ignore[type-arg]
ArrayLike: TypeAlias = npt.NDArray[np.floating[Any]]

# ---------------------------------------------------------------------------
# Semantic NewTypes for stronger typing at call sites
# ---------------------------------------------------------------------------
ColumnName = NewType("ColumnName", str)
FilePath = NewType("FilePath", Path)

# ---------------------------------------------------------------------------
# Strategy literals
# ---------------------------------------------------------------------------
MissingStrategy: TypeAlias = str  # "drop" | "fill_mean" | "fill_median" | "fill_mode" | "fill_constant" | "interpolate"

OutlierMethod: TypeAlias = (
    str  # "iqr" | "zscore" | "modified_zscore" | "isolation_forest"
)

OutlierAction: TypeAlias = str  # "flag" | "remove" | "clip" | "transform"

EncodingStrategy: TypeAlias = str  # "label" | "onehot" | "ordinal" | "target"

ScalingMethod: TypeAlias = str  # "standard" | "minmax" | "robust" | "log"

SelectionMethod: TypeAlias = (
    str  # "variance" | "correlation" | "mutual_info" | "importance"
)

CorrelationMethod: TypeAlias = str  # "pearson" | "spearman" | "kendall"


# ---------------------------------------------------------------------------
# Result TypedDicts
# ---------------------------------------------------------------------------
class AnalysisResult(dict[str, Any]):
    """Generic result container returned by analyzers and pipelines."""


class ProfileResult(dict[str, Any]):
    """Result container for data profiling.

    Expected keys:
        shape, dtypes, missing_counts, missing_pct,
        unique_counts, summary_stats, correlations
    """


class CleaningResult(dict[str, Any]):
    """Result container for cleaning operations.

    Expected keys:
        original_shape, cleaned_shape, rows_removed,
        columns_modified, actions_taken
    """
