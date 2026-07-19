"""Unified data readers with auto-detection by file extension.

Each reader wraps pandas I/O with sensible defaults, validation, and
support for chunked reading of large files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from analysis.core.exceptions import ConfigurationError, DataIOError

# ---------------------------------------------------------------------------
# Registry of extension → reader class
# ---------------------------------------------------------------------------
_EXTENSION_REGISTRY: dict[str, type[_BaseReader]] = {}


def _register(ext: str):
    """Class decorator that registers a reader for a file extension."""

    def decorator(cls: type[_BaseReader]) -> type[_BaseReader]:
        _EXTENSION_REGISTRY[ext] = cls
        return cls

    return decorator


# ---------------------------------------------------------------------------
# Base reader
# ---------------------------------------------------------------------------
class _BaseReader:
    """Internal base for all format-specific readers."""

    def __init__(self, **kwargs: Any) -> None:
        self._options = kwargs

    def read(self, path: Path) -> pd.DataFrame:
        """Read a file and return a DataFrame.

        Args:
            path: Absolute or relative path to the data file.

        Returns:
            Loaded DataFrame.

        Raises:
            DataIOError: If the file cannot be read.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Concrete readers
# ---------------------------------------------------------------------------
@_register(".csv")
class CSVReader(_BaseReader):
    """Read CSV files with configurable delimiter, encoding, and chunk size.

    Args:
        delimiter: Column separator (default ``","``).
        encoding: File encoding (default ``"utf-8"``).
        chunk_size: If set, return the *concatenation* of chunks of this size.
            Useful for memory-constrained environments.
        **kwargs: Extra keyword arguments forwarded to :func:`pandas.read_csv`.
    """

    def __init__(
        self,
        *,
        delimiter: str = ",",
        encoding: str = "utf-8",
        chunk_size: int | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._delimiter = delimiter
        self._encoding = encoding
        self._chunk_size = chunk_size

    def read(self, path: Path) -> pd.DataFrame:
        try:
            if self._chunk_size:
                chunks = pd.read_csv(
                    path,
                    sep=self._delimiter,
                    encoding=self._encoding,
                    chunksize=self._chunk_size,
                    **self._options,
                )
                return pd.concat(chunks, ignore_index=True)
            return pd.read_csv(
                path,
                sep=self._delimiter,
                encoding=self._encoding,
                **self._options,
            )
        except FileNotFoundError as exc:
            raise DataIOError(f"File not found: {path}") from exc
        except Exception as exc:
            raise DataIOError(f"Failed to read CSV {path}: {exc}") from exc


@_register(".json")
class JSONReader(_BaseReader):
    """Read JSON files (records, lines, or nested).

    Args:
        orient: JSON orientation (default ``"records"``).
        lines: If ``True``, read newline-delimited JSON.
        **kwargs: Extra keyword arguments forwarded to :func:`pandas.read_json`.
    """

    def __init__(
        self,
        *,
        orient: str = "records",
        lines: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._orient = orient
        self._lines = lines

    def read(self, path: Path) -> pd.DataFrame:
        try:
            return pd.read_json(
                path,
                orient=self._orient,
                lines=self._lines,
                **self._options,
            )
        except FileNotFoundError as exc:
            raise DataIOError(f"File not found: {path}") from exc
        except Exception as exc:
            raise DataIOError(f"Failed to read JSON {path}: {exc}") from exc


@_register(".parquet")
class ParquetReader(_BaseReader):
    """Read Apache Parquet files.

    Args:
        columns: Optional list of columns to read (pushdown projection).
        **kwargs: Extra keyword arguments forwarded to :func:`pandas.read_parquet`.
    """

    def __init__(self, *, columns: list[str] | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._columns = columns

    def read(self, path: Path) -> pd.DataFrame:
        try:
            return pd.read_parquet(path, columns=self._columns, **self._options)
        except FileNotFoundError as exc:
            raise DataIOError(f"File not found: {path}") from exc
        except Exception as exc:
            raise DataIOError(f"Failed to read Parquet {path}: {exc}") from exc


@_register(".xlsx")
@_register(".xls")
class ExcelReader(_BaseReader):
    """Read Excel workbooks (.xlsx / .xls).

    Args:
        sheet_name: Sheet to read (default ``0``, the first sheet).
        **kwargs: Extra keyword arguments forwarded to :func:`pandas.read_excel`.
    """

    def __init__(self, *, sheet_name: str | int = 0, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._sheet_name = sheet_name

    def read(self, path: Path) -> pd.DataFrame:
        try:
            return pd.read_excel(
                path,
                sheet_name=self._sheet_name,
                **self._options,
            )
        except FileNotFoundError as exc:
            raise DataIOError(f"File not found: {path}") from exc
        except Exception as exc:
            raise DataIOError(f"Failed to read Excel {path}: {exc}") from exc


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------
def read_data(
    path: str | Path,
    *,
    reader: _BaseReader | None = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """Read data from *path*, auto-detecting the format by extension.

    Args:
        path: File path to read.
        reader: Optional pre-configured reader instance. If not provided,
            the reader is selected from the extension registry.
        **kwargs: Forwarded to the auto-selected reader constructor.

    Returns:
        Loaded DataFrame.

    Raises:
        ConfigurationError: If the file extension is not supported.
        DataIOError: If the file cannot be read.

    Example::

        df = read_data("sales.csv")
        df = read_data("events.json", lines=True)
        df = read_data("warehouse.parquet", columns=["id", "value"])
    """
    path = Path(path)
    if reader is not None:
        return reader.read(path)

    ext = path.suffix.lower()
    reader_cls = _EXTENSION_REGISTRY.get(ext)
    if reader_cls is None:
        supported = ", ".join(sorted(_EXTENSION_REGISTRY))
        raise ConfigurationError(
            f"Unsupported file extension {ext!r}. Supported: {supported}"
        )
    return reader_cls(**kwargs).read(path)
