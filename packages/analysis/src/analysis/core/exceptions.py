"""Custom exception hierarchy for the analysis package.

All analysis-specific exceptions inherit from :class:`AnalysisError` so callers
can catch the broad category or handle fine-grained error types individually.
"""

from __future__ import annotations


class AnalysisError(Exception):
    """Base exception for all analysis-related errors."""

    def __init__(self, message: str, *, details: dict[str, object] | None = None) -> None:
        self.details = details or {}
        super().__init__(message)


class DataValidationError(AnalysisError):
    """Raised when input data fails validation checks.

    Examples:
        - Required columns are missing
        - DataFrame is empty
        - Column dtypes do not match the expected schema
    """


class PipelineError(AnalysisError):
    """Raised when a pipeline encounters an error during execution.

    Attributes:
        step_name: The name of the step that failed.
    """

    def __init__(
        self,
        message: str,
        *,
        step_name: str | None = None,
        details: dict[str, object] | None = None,
    ) -> None:
        self.step_name = step_name
        super().__init__(message, details=details)

    def __str__(self) -> str:
        prefix = f"[step={self.step_name}] " if self.step_name else ""
        return f"{prefix}{super().__str__()}"


class DataIOError(AnalysisError):
    """Raised when a read or write operation fails.

    Examples:
        - File not found
        - Unsupported file format
        - Permission denied
    """


class ConfigurationError(AnalysisError):
    """Raised when configuration or parameters are invalid.

    Examples:
        - Unknown strategy name
        - Mutually exclusive options provided together
    """
