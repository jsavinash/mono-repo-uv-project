# 📊 Analysis

> Production-grade data analysis toolkit for the Python mono-repo.

## Features

- **IO** — Unified readers/writers for CSV, JSON, Parquet, Excel with chunked reading
- **Cleaning** — Missing value handling, outlier detection, duplicate removal, dtype coercion
- **EDA** — Data profiling, statistical tests, publication-ready visualizations
- **Feature Engineering** — Encoding, scaling, feature selection, polynomial/interaction transforms
- **Pipeline** — Composable step-chain with validation, logging & error recovery
- **Reporting** — Markdown & HTML report generation with embedded charts
- **Utils** — Structured logging, DataFrame validation decorators, timing/caching helpers

## Quick Start

```python
from analysis import AnalysisPipeline, DataProfiler, MissingValueHandler
from analysis.io import read_data

# Load data from any supported format
df = read_data("data.csv")

# Build a composable pipeline
pipeline = AnalysisPipeline(name="my-analysis")
pipeline.add_step("clean_missing", MissingValueHandler(strategy="fill_median"))
pipeline.add_step("profile", DataProfiler())

result = pipeline.run(df)
print(result)
```

## CLI

```bash
# Profile a dataset
uv run analysis-profile data.csv

# Generate an HTML report
uv run analysis-report data.csv --output report.html
```

## Architecture

```
analysis/
├── core/                # Abstract base classes, types, exceptions
├── io/                  # Readers & writers
├── cleaning/            # Data cleaning & preprocessing
├── eda/                 # Exploratory data analysis
├── feature_engineering/  # Feature transforms
├── pipeline/            # Composable pipeline engine
├── reporting/           # Report generation
└── utils/               # Logging, validation, decorators
```
