"""Duplicate detection and removal."""

from __future__ import annotations

import pandas as pd

from analysis.core.base import BaseTransformer
from analysis.core.types import CleaningResult


class DuplicateHandler(BaseTransformer):
    """Detect and remove duplicate rows.

    Args:
        subset: Column names to consider for identifying duplicates.
            ``None`` means all columns.
        keep: Which duplicates to keep — ``"first"``, ``"last"``, or
            ``False`` (drop all duplicates).
        name: Optional transformer name.

    Example::

        handler = DuplicateHandler(subset=["email"], keep="first")
        clean_df = handler.fit_transform(df)
    """

    def __init__(
        self,
        *,
        subset: list[str] | None = None,
        keep: str | bool = "first",
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self._subset = subset
        self._keep = keep
        self._duplicate_count: int = 0
        self._last_result: CleaningResult | None = None

    def fit(self, df: pd.DataFrame) -> DuplicateHandler:
        """Count duplicates (no learned state needed)."""
        self._duplicate_count = int(
            df.duplicated(subset=self._subset, keep=self._keep).sum()
        )
        self._is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows."""
        original_shape = df.shape
        result = df.drop_duplicates(subset=self._subset, keep=self._keep).reset_index(
            drop=True
        )

        rows_removed = original_shape[0] - result.shape[0]
        self._last_result = CleaningResult(
            original_shape=original_shape,
            cleaned_shape=result.shape,
            rows_removed=rows_removed,
            columns_modified=self._subset or list(df.columns),
            actions_taken=[f"Removed {rows_removed} duplicate row(s)"]
            if rows_removed
            else [],
        )
        return result

    @property
    def duplicate_count(self) -> int:
        """Number of duplicate rows found during ``fit``."""
        return self._duplicate_count

    @property
    def result(self) -> CleaningResult | None:
        return self._last_result
