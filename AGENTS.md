# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project overview

py-earth is a Python implementation of Jerome Friedman's Multivariate Adaptive Regression Splines (MARS) algorithm, exposing a scikit-learn-style estimator API.

Key points:
- Library is distributed as the `pyearth` package with a main `Earth` regressor/transformer in `src/pyearth/earth.py`.
- The estimator supports dense NumPy inputs as well as pandas/patsy data structures, can handle missing predictor values when `allow_missing=True`, and is compatible with scikit-learn model patterns.

## Issue tracking

This project uses **bd (beads)** for issue tracking.
Run `bd prime` for workflow context, or install hooks (`bd hooks install`) for auto-injection.

**Quick reference:**
- `bd ready` - Find unblocked work
- `bd create "Title" --type task --priority 2` - Create issue
- `bd close <id>` - Complete work
- `bd sync` - Sync with git (run at session end)

For full workflow details: `bd prime`

## Development environment

Environment management and common workflows are defined via `pixi.toml`. The `default` environment includes the development tools (pytest, ruff, mypy, etc.), and named tasks encapsulate typical commands.

To run any task below, use:

```bash path=null start=null
pixi run <task-name>
```

### Setup / installation

- Editable install for local development:

```bash path=null start=null
pixi run build-editable
```

- Alternatively, using plain pip (outside pixi):

```bash path=null start=null
pip install -e '.[dev]'
```

### Testing

- Run the full test suite:

```bash path=null start=null
pixi run test
```

- Verbose test run:

```bash path=null start=null
pixi run test-verbose
```

- Test run with coverage and HTML report:

```bash path=null start=null
pixi run test-cov
```

- Run a single test (inside the pixi environment):

```bash path=null start=null
pixi run pytest tests/test_earth.py::test_basic
```

(pytest is configured in `pyproject.toml` to discover tests under `tests/`.)

### Linting, formatting, and type checking

- Ruff lint:

```bash path=null start=null
pixi run lint
```

- Ruff lint with autofix:

```bash path=null start=null
pixi run lint-fix
```

- Format code with Ruff:

```bash path=null start=null
pixi run format
```

- Check formatting only:

```bash path=null start=null
pixi run format-check
```

- Mypy type checking:

```bash path=null start=null
pixi run typecheck
```

- Combined check (lint + format-check + typecheck):

```bash path=null start=null
pixi run check-all
```

### Build and packaging

- Build wheels:

```bash path=null start=null
pixi run build-wheels
```

- Build sdist:

```bash path=null start=null
pixi run build-sdist
```

- Build both sdist and wheels:

```bash path=null start=null
pixi run build-all
```

### Documentation

Sphinx-based documentation lives under `doc/`. The `doc/README.md` file documents prerequisites and how to invoke `make html` directly.

- Build HTML documentation via the pixi task:

```bash path=null start=null
pixi run build-docs
```

### Cleaning

- Remove build artifacts:

```bash path=null start=null
pixi run clean
```

- Deep clean including caches and local pixi artifacts:

```bash path=null start=null
pixi run clean-all
```

## High-level architecture

### Public API surface (`pyearth`)

- Package root `src/pyearth/__init__.py` exposes the `Earth` estimator and defines the library version.
- `src/pyearth/earth.py` implements the `Earth` class, which mixes in scikit-learn's `BaseEstimator`, `RegressorMixin`, and `TransformerMixin`.
  - Provides `fit`, `predict`, `transform`, `predict_deriv`, `score`, and reporting utilities like `trace()`, `summary()`, and `summary_feature_importances()`.
  - Manages input sanitization (`_scrub` / `_scrub_x`), label extraction, handling of missing values (via `allow_missing` and `missing` masks), and mapping between original feature space and the learned basis space.

### Cython core (algorithm implementation)

The heavy numerical work lives in Cython extension modules under `src/pyearth`:

- `_basis.{pxd,pyx}`: representation of the multivariate spline basis and individual basis functions, including evaluation, pruning state, and transformation and derivative support used by `Earth.transform` / `predict_deriv`.
- `_forward.{pxd,pyx}`: forward pass of MARS. Given cleaned `(X, y, sample_weight, missing)`, incrementally builds candidate basis functions to reduce squared error, enforcing constraints such as `max_terms`, `max_degree`, and span parameters.
- `_knot_search.{pxd,pyx}`: efficient search for knot locations along each predictor, using span parameters and GCV-based criteria.
- `_pruning.{pxd,pyx}`: pruning pass that selects a subset of basis functions by minimizing a generalized cross-validation (GCV) objective and computing feature-importance metrics (`FEAT_IMP_CRITERIA`).
- `_qr.{pxd,pyx}`: QR-based least-squares routines used in the linear fitting stage.
- `_record.{pxd,pyx}`: record/trace objects for the forward and pruning passes, feeding into `EarthTrace` and the reporting helpers.
- `_util.{pxd,pyx}`: numerical utilities, including `gcv`, basis-space helpers, and small matrix operations used throughout the passes.
- `_types.{pxd,pyx}`: shared type definitions (e.g., boolean array aliases) used across the Cython modules.

`earth.py` orchestrates these pieces: it prepares clean NumPy arrays, passes them into `_forward` / `_pruning` / `_record` to build the model, and then uses `_util` and `_qr` to perform the final linear fit and compute diagnostics like `mse_`, `gcv_`, `rsq_`, and `grsq_`.

### Export and interoperability

- `src/pyearth/export.py` contains helpers for exporting fitted `Earth` models into other representations. Optional extras for export (e.g., `sympy`) are declared in `pyproject.toml` and `pixi.toml` under the `export` feature.

### Tests

The test suite under `tests/` mirrors the internal structure:

- `tests/test_earth.py`: end-to-end tests of the `Earth` estimator API (fitting, predicting, traces, missing-data behavior).
- `tests/test_forward.py`, `tests/test_pruning.py`, `tests/test_knot_search.py`, `tests/test_qr.py`: focused tests for the corresponding Cython modules.
- `tests/test_export.py`: ensures model-export utilities match expected outputs.
- Subdirectories such as `tests/basis/`, `tests/record/`, and `tests/pathological_data/` provide lower-level and edge-case coverage for basis/record behavior and difficult datasets.

### Documentation layout

- Sphinx configuration and sources live under `doc/`.
- `doc/README.md` explains how to install documentation dependencies and run `make html` to generate the docs.
