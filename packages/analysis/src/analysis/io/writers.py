"""Unified data writers with format auto-selection.

Each writer wraps pandas export with directory creation, overwrite protection,
and optional compression.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from analysis.core.exceptions import ConfigurationError, DataIOError

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
_WRITER_REGISTRY: dict[str, type["_BaseWriter"]] = {}


def _register(ext: str):  # noqa: ANN202
    def decorator(cls: type[_BaseWriter]) -> type[_BaseWriter]:
        _WRITER_REGISTRY[ext] = cls
        return cls

    return decorator


# ---------------------------------------------------------------------------
# Base writer
# ---------------------------------------------------------------------------
class _BaseWriter:
    """Internal base for all format-specific writers."""

    def __init__(self, *, overwrite: bool = False, **kwargs: Any) -> None:
        self._overwrite = overwrite
        self._options = kwargs

    def _ensure_directory(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

    def _check_overwrite(self, path: Path) -> None:
        if path.exists() and not self._overwrite:
            raise DataIOError(
                f"File already exists: {path}. Set overwrite=True to replace it."
            )

    def write(self, df: pd.DataFrame, path: Path) -> Path:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Concrete writers
# ---------------------------------------------------------------------------
@_register(".csv")
class CSVWriter(_BaseWriter):
    """Write DataFrames to CSV.

    Args:
        index: Whether to write the row index (default ``False``).
        encoding: File encoding (default ``"utf-8"``).
        overwrite: Allow overwriting existing files.
        **kwargs: Extra keyword arguments forwarded to :meth:`DataFrame.to_csv`.
    """

    def __init__(
        self,
        *,
        index: bool = False,
        encoding: str = "utf-8",
        overwrite: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(overwrite=overwrite, **kwargs)
        self._index = index
        self._encoding = encoding

    def write(self, df: pd.DataFrame, path: Path) -> Path:
        self._ensure_directory(path)
        self._check_overwrite(path)
        try:
            df.to_csv(path, index=self._index, encoding=self._encoding, **self._options)
        except Exception as exc:
            raise DataIOError(f"Failed to write CSV {path}: {exc}") from exc
        return path


@_register(".json")
class JSONWriter(_BaseWriter):
    """Write DataFrames to JSON.

    Args:
        orient: JSON orientation (default ``"records"``).
        lines: If ``True``, write newline-delimited JSON.
        overwrite: Allow overwriting existing files.
        **kwargs: Extra keyword arguments forwarded to :meth:`DataFrame.to_json`.
    """

    def __init__(
        self,
        *,
        orient: str = "records",
        lines: bool = False,
        overwrite: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(overwrite=overwrite, **kwargs)
        self._orient = orient
        self._lines = lines

    def write(self, df: pd.DataFrame, path: Path) -> Path:
        self._ensure_directory(path)
        self._check_overwrite(path)
        try:
            df.to_json(path, orient=self._orient, lines=self._lines, **self._options)
        except Exception as exc:
            raise DataIOError(f"Failed to write JSON {path}: {exc}") from exc
        return path


@_register(".parquet")
class ParquetWriter(_BaseWriter):
    """Write DataFrames to Parquet.

    Args:
        compression: Compression codec (default ``"snappy"``).
        overwrite: Allow overwriting existing files.
        **kwargs: Extra keyword arguments forwarded to :meth:`DataFrame.to_parquet`.
    """

    def __init__(
        self,
        *,
        compression: str = "snappy",
        overwrite: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(overwrite=overwrite, **kwargs)
        self._compression = compression

    def write(self, df: pd.DataFrame, path: Path) -> Path:
        self._ensure_directory(path)
        self._check_overwrite(path)
        try:
            df.to_parquet(path, compression=self._compression, **self._options)
        except Exception as exc:
            raise DataIOError(f"Failed to write Parquet {path}: {exc}") from exc
        return path


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------
def write_data(
    df: pd.DataFrame,
    path: str | Path,
    *,
    writer: _BaseWriter | None = None,
    overwrite: bool = False,
    **kwargs: Any,
) -> Path:
    """Write *df* to *path*, auto-detecting the format by extension.

    Args:
        df: DataFrame to write.
        path: Output file path.
        writer: Optional pre-configured writer instance.
        overwrite: Allow overwriting existing files (default ``False``).
        **kwargs: Forwarded to the auto-selected writer constructor.

    Returns:
        The resolved output path.

    Raises:
        ConfigurationError: If the file extension is not supported.
        DataIOError: If the write fails.
    """
    path = Path(path)
    if writer is not None:
        return writer.write(df, path)

    ext = path.suffix.lower()
    writer_cls = _WRITER_REGISTRY.get(ext)
    if writer_cls is None:
        supported = ", ".join(sorted(_WRITER_REGISTRY))
        raise ConfigurationError(
            f"Unsupported file extension {ext!r}. Supported: {supported}"
        )
    return writer_cls(overwrite=overwrite, **kwargs).write(df, path)
