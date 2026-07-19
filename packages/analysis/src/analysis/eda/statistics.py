"""Statistical hypothesis tests for exploratory analysis.

Provides wrappers around ``scipy.stats`` for normality, comparison, and
association testing with structured result dictionaries.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


class StatisticalTests:
    """Collection of statistical tests operating on pandas DataFrames.

    All methods are static / class methods — no instantiation needed,
    but you can instantiate for a consistent OO interface.

    Example::

        tests = StatisticalTests()
        result = tests.normality_test(df["price"])
        print(result["shapiro"]["p_value"])
    """

    # ------------------------------------------------------------------
    # Normality tests
    # ------------------------------------------------------------------
    @staticmethod
    def normality_test(
        series: pd.Series,  # type: ignore[type-arg]
        *,
        alpha: float = 0.05,
    ) -> dict[str, Any]:
        """Run Shapiro-Wilk, D'Agostino-Pearson, and Anderson-Darling tests.

        Args:
            series: Numeric pandas Series to test.
            alpha: Significance level for interpretation.

        Returns:
            Dictionary keyed by test name with statistic, p_value, and
            a boolean ``is_normal`` at the given alpha.
        """
        clean = series.dropna().astype(float)
        results: dict[str, Any] = {}

        # Shapiro-Wilk (limited to 5000 samples)
        sample = (
            clean.sample(min(5000, len(clean)), random_state=42)
            if len(clean) > 5000
            else clean
        )
        stat_sw, p_sw = stats.shapiro(sample)
        results["shapiro"] = {
            "statistic": float(stat_sw),
            "p_value": float(p_sw),
            "is_normal": p_sw > alpha,
        }

        # D'Agostino-Pearson (needs n >= 20)
        if len(clean) >= 20:
            stat_da, p_da = stats.normaltest(clean)
            results["dagostino"] = {
                "statistic": float(stat_da),
                "p_value": float(p_da),
                "is_normal": p_da > alpha,
            }

        # Anderson-Darling
        ad_result = stats.anderson(clean, dist="norm")
        # Use the 5% significance level index
        sig_idx = (
            list(ad_result.significance_level).index(5.0)
            if 5.0 in ad_result.significance_level
            else 2
        )
        results["anderson"] = {
            "statistic": float(ad_result.statistic),
            "critical_value_5pct": float(ad_result.critical_values[sig_idx]),
            "is_normal": ad_result.statistic < ad_result.critical_values[sig_idx],
        }

        return results

    # ------------------------------------------------------------------
    # Comparison tests (two-sample)
    # ------------------------------------------------------------------
    @staticmethod
    def two_sample_test(
        group_a: pd.Series,  # type: ignore[type-arg]
        group_b: pd.Series,  # type: ignore[type-arg]
        *,
        alpha: float = 0.05,
    ) -> dict[str, Any]:
        """Run parametric (t-test) and non-parametric (Mann-Whitney) tests.

        Args:
            group_a: First sample.
            group_b: Second sample.
            alpha: Significance level.

        Returns:
            Dictionary with t-test and Mann-Whitney results.
        """
        a, b = group_a.dropna().astype(float), group_b.dropna().astype(float)
        results: dict[str, Any] = {}

        # Independent t-test (Welch's)
        stat_t, p_t = stats.ttest_ind(a, b, equal_var=False)
        results["ttest"] = {
            "statistic": float(stat_t),
            "p_value": float(p_t),
            "significant": p_t < alpha,
        }

        # Mann-Whitney U
        stat_u, p_u = stats.mannwhitneyu(a, b, alternative="two-sided")
        results["mann_whitney"] = {
            "statistic": float(stat_u),
            "p_value": float(p_u),
            "significant": p_u < alpha,
        }

        # Effect size (Cohen's d)
        pooled_std = float(np.sqrt((a.std() ** 2 + b.std() ** 2) / 2))
        cohens_d = float((a.mean() - b.mean()) / pooled_std) if pooled_std > 0 else 0.0
        results["effect_size"] = {
            "cohens_d": cohens_d,
            "interpretation": _interpret_cohens_d(abs(cohens_d)),
        }

        return results

    # ------------------------------------------------------------------
    # ANOVA / Kruskal-Wallis (multi-group)
    # ------------------------------------------------------------------
    @staticmethod
    def multi_group_test(
        *groups: pd.Series,  # type: ignore[type-arg]
        alpha: float = 0.05,
    ) -> dict[str, Any]:
        """Run one-way ANOVA and Kruskal-Wallis tests.

        Args:
            *groups: Two or more numeric Series.
            alpha: Significance level.

        Returns:
            Dictionary with ANOVA and Kruskal-Wallis results.
        """
        clean_groups = [g.dropna().astype(float) for g in groups]
        results: dict[str, Any] = {}

        stat_f, p_f = stats.f_oneway(*clean_groups)
        results["anova"] = {
            "statistic": float(stat_f),
            "p_value": float(p_f),
            "significant": p_f < alpha,
        }

        stat_h, p_h = stats.kruskal(*clean_groups)
        results["kruskal_wallis"] = {
            "statistic": float(stat_h),
            "p_value": float(p_h),
            "significant": p_h < alpha,
        }

        return results

    # ------------------------------------------------------------------
    # Association tests (categorical)
    # ------------------------------------------------------------------
    @staticmethod
    def chi_squared_test(
        col_a: pd.Series,  # type: ignore[type-arg]
        col_b: pd.Series,  # type: ignore[type-arg]
        *,
        alpha: float = 0.05,
    ) -> dict[str, Any]:
        """Run chi-squared test of independence.

        Args:
            col_a: First categorical column.
            col_b: Second categorical column.
            alpha: Significance level.

        Returns:
            Dictionary with chi-squared statistic, p-value, degrees of
            freedom, and Cramér's V effect size.
        """
        contingency = pd.crosstab(col_a, col_b)
        chi2, p, dof, _ = stats.chi2_contingency(contingency)

        # Cramér's V
        n = contingency.sum().sum()
        min_dim = min(contingency.shape) - 1
        cramers_v = float(np.sqrt(chi2 / (n * min_dim))) if min_dim > 0 else 0.0

        return {
            "chi2": float(chi2),
            "p_value": float(p),
            "dof": int(dof),
            "significant": p < alpha,
            "cramers_v": cramers_v,
            "interpretation": _interpret_cramers_v(cramers_v),
        }

    # ------------------------------------------------------------------
    # Correlation significance
    # ------------------------------------------------------------------
    @staticmethod
    def correlation_test(
        series_a: pd.Series,  # type: ignore[type-arg]
        series_b: pd.Series,  # type: ignore[type-arg]
        *,
        method: str = "pearson",
        alpha: float = 0.05,
    ) -> dict[str, Any]:
        """Test the significance of a correlation coefficient.

        Args:
            series_a: First numeric Series.
            series_b: Second numeric Series.
            method: ``"pearson"`` or ``"spearman"``.
            alpha: Significance level.

        Returns:
            Dictionary with correlation, p-value, and significance.
        """
        a, b = series_a.dropna(), series_b.dropna()
        common = a.index.intersection(b.index)
        a, b = a.loc[common].astype(float), b.loc[common].astype(float)

        if method == "spearman":
            corr, p = stats.spearmanr(a, b)
        else:
            corr, p = stats.pearsonr(a, b)

        return {
            "correlation": float(corr),
            "p_value": float(p),
            "significant": p < alpha,
            "method": method,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _interpret_cohens_d(d: float) -> str:
    if d < 0.2:
        return "negligible"
    if d < 0.5:
        return "small"
    if d < 0.8:
        return "medium"
    return "large"


def _interpret_cramers_v(v: float) -> str:
    if v < 0.1:
        return "negligible"
    if v < 0.3:
        return "small"
    if v < 0.5:
        return "medium"
    return "large"
