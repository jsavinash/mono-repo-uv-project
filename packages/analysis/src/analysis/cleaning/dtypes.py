"""Data type coercion and schema enforcement.

Ensures DataFrame columns conform to an expected schema, with automatic
coercion and rich error reporting for failures.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.core.base import BaseTransformer
from analysis.core.exceptions import DataValidationError
from analysis.core.types import CleaningResult


class TypeCoercer(BaseTransformer):
    """Enforce a dtype schema on a DataFrame.

    Args:
        schema: Mapping of column name → expected dtype string
            (e.g. ``{"age": "int64", "price": "float64", "date": "datetime64[ns]"}``).
        errors: How to handle coercion failures — ``"raise"`` or ``"coerce"``
            (set failing values to ``NaN``).
        name: Optional transformer name.

    Example::

        coercer = TypeCoercer(schema={"price": "float64", "qty": "int64"})
        df = coercer.fit_transform(df)
    """

    def __init__(
        self,
        *,
        schema: dict[str, str],
        errors: str = "coerce",
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self._schema = schema
        self._errors = errors
        self._coercion_report: dict[str, dict[str, Any]] = {}
        self._last_result: CleaningResult | None = None

    def fit(self, df: pd.DataFrame) -> TypeCoercer:
        """Validate that all schema columns exist in the DataFrame."""
        missing = set(self._schema) - set(df.columns)
        if missing:
            raise DataValidationError(
                f"Schema columns not found in DataFrame: {sorted(missing)}",
                details={"missing_columns": sorted(missing)},
            )
        self._is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply dtype coercion to all schema columns."""
        original_shape = df.shape
        result = df.copy()
        actions: list[str] = []
        self._coercion_report = {}

        for col, target_dtype in self._schema.items():
            if col not in result.columns:
                continue

            current_dtype = str(result[col].dtype)
            if current_dtype == target_dtype:
                continue

            try:
                if "datetime" in target_dtype:
                    result[col] = pd.to_datetime(result[col], errors=self._errors)
                elif "int" in target_dtype or "float" in target_dtype:
                    result[col] = pd.to_numeric(result[col], errors=self._errors)
                    if "int" in target_dtype and result[col].isnull().any():
                        # Can't cast to int with NaN — use nullable Int
                        result[col] = result[col].astype("Int64")
                    else:
                        result[col] = result[col].astype(target_dtype)
                elif target_dtype in ("str", "string", "object"):
                    result[col] = result[col].astype(str)
                elif target_dtype == "category":
                    result[col] = result[col].astype("category")
                elif target_dtype == "bool":
                    result[col] = result[col].astype(bool)
                else:
                    result[col] = result[col].astype(target_dtype)

                nulls_after = int(result[col].isnull().sum()) - int(
                    df[col].isnull().sum()
                )
                self._coercion_report[col] = {
                    "from": current_dtype,
                    "to": target_dtype,
                    "coercion_nulls_introduced": max(0, nulls_after),
                    "success": True,
                }
                actions.append(f"Coerced '{col}' from {current_dtype} → {target_dtype}")

            except (ValueError, TypeError) as exc:
                if self._errors == "raise":
                    raise DataValidationError(
                        f"Cannot coerce column '{col}' from {current_dtype} to {target_dtype}: {exc}",
                        details={
                            "column": col,
                            "from": current_dtype,
                            "to": target_dtype,
                        },
                    ) from exc
                self._coercion_report[col] = {
                    "from": current_dtype,
                    "to": target_dtype,
                    "success": False,
                    "error": str(exc),
                }
                actions.append(f"Failed to coerce '{col}': {exc}")

        self._last_result = CleaningResult(
            original_shape=original_shape,
            cleaned_shape=result.shape,
            rows_removed=0,
            columns_modified=list(self._schema.keys()),
            actions_taken=actions,
        )
        return result

    @property
    def coercion_report(self) -> dict[str, dict[str, Any]]:
        """Detailed report of coercion outcomes per column."""
        return self._coercion_report

    @property
    def result(self) -> CleaningResult | None:
        return self._last_result
