"""Publication-ready visualizations for exploratory data analysis.

All plotting functions return ``matplotlib.figure.Figure`` objects for
composability and support export to PNG, SVG, and PDF.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Use non-interactive backend by default for server/pipeline usage
matplotlib.use("Agg")


class Visualizer:
    """Create publication-quality EDA visualizations.

    Args:
        style: Seaborn style preset (default ``"whitegrid"``).
        palette: Color palette name (default ``"viridis"``).
        figsize: Default figure size (default ``(10, 6)``).
        dpi: Resolution for saved figures (default ``150``).

    Example::

        viz = Visualizer(style="darkgrid", palette="coolwarm")
        fig = viz.distribution_plot(df, column="price")
        viz.save(fig, "price_distribution.png")
    """

    def __init__(
        self,
        *,
        style: str = "whitegrid",
        palette: str = "viridis",
        figsize: tuple[int, int] = (10, 6),
        dpi: int = 150,
    ) -> None:
        self._style = style
        self._palette = palette
        self._figsize = figsize
        self._dpi = dpi
        sns.set_style(style)
        sns.set_palette(palette)

    # ------------------------------------------------------------------
    # Distribution plots
    # ------------------------------------------------------------------
    def distribution_plot(
        self,
        df: pd.DataFrame,
        column: str,
        *,
        kind: str = "hist",
        bins: int = 30,
        kde: bool = True,
        title: str | None = None,
    ) -> plt.Figure:
        """Plot the distribution of a single column.

        Args:
            df: Input DataFrame.
            column: Column to visualise.
            kind: ``"hist"``, ``"kde"``, or ``"box"``.
            bins: Number of histogram bins.
            kde: Overlay KDE curve on histogram.
            title: Custom title.

        Returns:
            Matplotlib Figure.
        """
        fig, ax = plt.subplots(figsize=self._figsize)
        data = df[column].dropna()

        if kind == "hist":
            sns.histplot(data, bins=bins, kde=kde, ax=ax)
        elif kind == "kde":
            sns.kdeplot(data, fill=True, ax=ax)
        elif kind == "box":
            sns.boxplot(x=data, ax=ax)

        ax.set_title(
            title or f"Distribution of {column}", fontsize=14, fontweight="bold"
        )
        ax.set_xlabel(column)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Correlation heatmap
    # ------------------------------------------------------------------
    def correlation_heatmap(
        self,
        df: pd.DataFrame,
        *,
        method: str = "pearson",
        annot: bool = True,
        mask_upper: bool = True,
        title: str | None = None,
    ) -> plt.Figure:
        """Plot a correlation heatmap for numeric columns.

        Args:
            df: Input DataFrame.
            method: Correlation method.
            annot: Annotate cells with values.
            mask_upper: Hide upper triangle for readability.
            title: Custom title.

        Returns:
            Matplotlib Figure.
        """
        numeric_df = df.select_dtypes(include=[np.number])
        corr = numeric_df.corr(method=method)

        mask = None
        if mask_upper:
            mask = np.triu(np.ones_like(corr, dtype=bool))

        size = max(8, len(corr.columns))
        fig, ax = plt.subplots(figsize=(size, size))
        sns.heatmap(
            corr,
            mask=mask,
            annot=annot,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=0.5,
            ax=ax,
        )
        ax.set_title(title or "Correlation Heatmap", fontsize=14, fontweight="bold")
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Missing value heatmap
    # ------------------------------------------------------------------
    def missing_value_plot(
        self,
        df: pd.DataFrame,
        *,
        title: str | None = None,
    ) -> plt.Figure:
        """Visualize missing value patterns as a heatmap.

        Args:
            df: Input DataFrame.
            title: Custom title.

        Returns:
            Matplotlib Figure.
        """
        fig, ax = plt.subplots(figsize=self._figsize)
        sns.heatmap(
            df.isnull(),
            cbar=True,
            cmap="YlOrRd",
            yticklabels=False,
            ax=ax,
        )
        ax.set_title(title or "Missing Value Pattern", fontsize=14, fontweight="bold")
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Pair plot
    # ------------------------------------------------------------------
    def pair_plot(
        self,
        df: pd.DataFrame,
        *,
        columns: list[str] | None = None,
        hue: str | None = None,
        max_columns: int = 6,
    ) -> plt.Figure:
        """Generate a pair plot for numeric columns.

        Args:
            df: Input DataFrame.
            columns: Specific columns (default: first *max_columns* numeric).
            hue: Categorical column for colouring.
            max_columns: Maximum number of columns to include.

        Returns:
            Matplotlib Figure.
        """
        if columns is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            columns = numeric_cols[:max_columns]

        plot_df = df[columns + ([hue] if hue and hue not in columns else [])].dropna()
        grid = sns.pairplot(plot_df, hue=hue, diag_kind="kde", plot_kws={"alpha": 0.6})
        grid.figure.suptitle("Pair Plot", y=1.02, fontsize=14, fontweight="bold")
        return grid.figure

    # ------------------------------------------------------------------
    # Box / violin comparison
    # ------------------------------------------------------------------
    def comparison_plot(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        *,
        kind: str = "box",
        title: str | None = None,
    ) -> plt.Figure:
        """Compare distributions across categories.

        Args:
            df: Input DataFrame.
            x: Categorical column.
            y: Numeric column.
            kind: ``"box"`` or ``"violin"``.
            title: Custom title.

        Returns:
            Matplotlib Figure.
        """
        fig, ax = plt.subplots(figsize=self._figsize)
        plot_fn = sns.boxplot if kind == "box" else sns.violinplot
        plot_fn(data=df, x=x, y=y, ax=ax)
        ax.set_title(title or f"{y} by {x}", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Save helper
    # ------------------------------------------------------------------
    def save(
        self,
        fig: plt.Figure,
        path: str | Path,
        *,
        dpi: int | None = None,
        close: bool = True,
    ) -> Path:
        """Save a figure to disk.

        Args:
            fig: Matplotlib Figure.
            path: Output file path (supports .png, .svg, .pdf).
            dpi: Override default DPI.
            close: Close the figure after saving.

        Returns:
            Resolved output path.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=dpi or self._dpi, bbox_inches="tight")
        if close:
            plt.close(fig)
        return path
