"""Core abstractions — base classes, type definitions, and exception hierarchy."""

from analysis.core.base import BaseAnalyzer, BasePipeline, BaseTransformer
from analysis.core.exceptions import (
    AnalysisError,
    ConfigurationError,
    DataIOError,
    DataValidationError,
    PipelineError,
)
from analysis.core.types import (
    AnalysisResult,
    CleaningResult,
    ColumnName,
    FilePath,
    ProfileResult,
)

__all__: list[str] = [
    # Base classes
    "BaseAnalyzer",
    "BaseTransformer",
    "BasePipeline",
    # Exceptions
    "AnalysisError",
    "DataValidationError",
    "PipelineError",
    "DataIOError",
    "ConfigurationError",
    # Types
    "AnalysisResult",
    "ProfileResult",
    "CleaningResult",
    "ColumnName",
    "FilePath",
]
