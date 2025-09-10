"""
qdl.validator

Validator implementation for comparing user-calculated factor returns to
reference/canonical factor returns loaded via the DataLoader.

Design principles (per PRD v0.2):
- Do not assume schemas. Callers must explicitly provide join keys (`on`) and a
  numeric value column name (`value_col`).
- No silent defaults. Raise clear errors when alignment fails or types are
  incompatible.
- Keep the core independent of I/O. Plotting is optional and returns a
  Matplotlib Figure without side effects.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

try:  # Optional: used only for typing the figure return
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - plotting is optional
    Figure = Any  # type: ignore
    plt = None  # type: ignore


@dataclass
class ValidationReport:
    """Result of a factor validation run.

    Fields are intentionally simple and serializable, except for `figure` which
    is optional and may be a Matplotlib Figure when plotting is requested.
    """

    mse: float
    rmse: float
    mae: float
    corr: Optional[float]
    ic: Optional[float]
    n_obs: int
    date_start: Optional[pd.Timestamp]
    date_end: Optional[pd.Timestamp]
    pass_thresholds: Optional[bool]
    thresholds: Optional[Dict[str, float]]
    diagnostics: Dict[str, Any]
    figure: Optional[Figure] = None


def _ensure_required_columns(df: pd.DataFrame, required: List[str], *, frame_name: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{frame_name} missing required columns: {missing}")


def _coerce_numeric(series: pd.Series, *, name: str) -> pd.Series:
    coerced = pd.to_numeric(series, errors="coerce")
    if coerced.isna().all():
        raise ValueError(f"Column '{name}' contains no numeric values after coercion")
    return coerced


def _pick_time_key(on: List[str], merged: pd.DataFrame) -> Optional[str]:
    for candidate in ("date", "time", "month", "dt"):  # common names, not a hard default
        if candidate in on and candidate in merged.columns:
            return candidate
    # Fallback: first datetime-like key among `on`
    for key in on:
        if key in merged.columns and pd.api.types.is_datetime64_any_dtype(merged[key]):
            return key
    return None


def _compute_metrics(aligned: pd.DataFrame) -> Tuple[float, float, float, Optional[float], Optional[float]]:
    diff = aligned["user_value"] - aligned["ref_value"]
    mse = float(np.mean(np.square(diff)))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(diff)))

    # Pearson correlation (guard against constant series)
    if aligned["user_value"].nunique(dropna=True) > 1 and aligned["ref_value"].nunique(dropna=True) > 1:
        corr = float(aligned["user_value"].corr(aligned["ref_value"], method="pearson"))
    else:
        corr = None

    # Information Coefficient (rank correlation). Use rank+pearson to avoid scipy dependency.
    if aligned["user_value"].notna().any() and aligned["ref_value"].notna().any():
        user_rank = aligned["user_value"].rank(method="average")
        ref_rank = aligned["ref_value"].rank(method="average")
        if user_rank.nunique(dropna=True) > 1 and ref_rank.nunique(dropna=True) > 1:
            ic = float(user_rank.corr(ref_rank, method="pearson"))
        else:
            ic = None
    else:
        ic = None

    return mse, rmse, mae, corr, ic


def _evaluate_thresholds(
    *,
    mse: float,
    rmse: float,
    mae: float,
    corr: Optional[float],
    ic: Optional[float],
    thresholds: Optional[Dict[str, float]],
) -> Optional[bool]:
    if not thresholds:
        return None

    rules: List[Tuple[str, bool]] = []
    if "mse_max" in thresholds:
        rules.append(("mse_max", mse <= float(thresholds["mse_max"])) )
    if "rmse_max" in thresholds:
        rules.append(("rmse_max", rmse <= float(thresholds["rmse_max"])) )
    if "mae_max" in thresholds:
        rules.append(("mae_max", mae <= float(thresholds["mae_max"])) )
    if "corr_min" in thresholds and corr is not None:
        rules.append(("corr_min", corr >= float(thresholds["corr_min"])) )
    if "ic_min" in thresholds and ic is not None:
        rules.append(("ic_min", ic >= float(thresholds["ic_min"])) )

    # If a correlation threshold is specified but corr/ic is None, treat as failure
    if ("corr_min" in (thresholds or {})) and corr is None:
        rules.append(("corr_min", False))
    if ("ic_min" in (thresholds or {})) and ic is None:
        rules.append(("ic_min", False))

    if not rules:
        return None

    return all(ok for _, ok in rules)


def _maybe_plot(
    aligned: pd.DataFrame,
    *,
    time_key: Optional[str],
    title: str,
) -> Optional[Figure]:
    if plt is None:
        return None

    plot_df = aligned.copy()
    x = plot_df[time_key] if (time_key is not None and time_key in plot_df.columns) else plot_df.index

    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, gridspec_kw={"height_ratios": [2.0, 1.0]})
    ax_top.plot(x, plot_df["ref_value"], label="reference", color="#1f77b4")
    ax_top.plot(x, plot_df["user_value"], label="user", color="#ff7f0e", alpha=0.85)
    ax_top.set_ylabel("value")
    ax_top.legend(loc="best")
    ax_top.grid(True, alpha=0.3)
    ax_top.set_title(title)

    err = plot_df["user_value"] - plot_df["ref_value"]
    ax_bottom.plot(x, err, label="error (user - ref)", color="#d62728")
    ax_bottom.axhline(0.0, color="black", linewidth=0.8, alpha=0.6)
    ax_bottom.set_ylabel("error")
    ax_bottom.grid(True, alpha=0.3)

    if time_key is not None:
        ax_bottom.set_xlabel(time_key)
    else:
        ax_bottom.set_xlabel("index")

    fig.tight_layout()
    return fig


def validate_factor(
    *,
    user: pd.DataFrame,
    reference: pd.DataFrame,
    on: List[str],
    value_col: str,
    thresholds: Optional[Dict[str, float]] = None,
    return_plot: bool = True,
    plot_title: Optional[str] = None,
    sort_by_time: bool = True,
) -> ValidationReport:
    """Validate a user-generated factor series against a reference series.

    Parameters
    ----------
    user : pd.DataFrame
        User-provided factor returns. Must include all `on` keys and `value_col`.
    reference : pd.DataFrame
        Reference factor returns. Must include all `on` keys and `value_col`.
    on : list[str]
        Explicit join keys for alignment (e.g., ["date"] or ["date","name"]).
    value_col : str
        Column name containing numeric values to compare.
    thresholds : dict, optional
        Rules like {"mse_max": 1e-6, "corr_min": 0.99}. If provided, the
        `pass_thresholds` field will report whether all constraints are met.
    return_plot : bool, default True
        When True and Matplotlib is available, return a Figure overlaying
        reference vs user and the error series.
    plot_title : str, optional
        Title for the plot figure. If None, a default is composed.
    sort_by_time : bool, default True
        If a time-like key exists among `on`, sort by it before plotting.
    """

    if not on:
        raise ValueError("'on' must be a non-empty list of join key names")
    if not isinstance(value_col, str) or not value_col:
        raise ValueError("'value_col' must be a non-empty string")

    _ensure_required_columns(user, on + [value_col], frame_name="user")
    _ensure_required_columns(reference, on + [value_col], frame_name="reference")

    user_work = user[on + [value_col]].copy()
    ref_work = reference[on + [value_col]].copy()

    # Coerce to numeric (report NA drops in diagnostics)
    user_work[value_col] = _coerce_numeric(user_work[value_col], name=value_col)
    ref_work[value_col] = _coerce_numeric(ref_work[value_col], name=value_col)

    # Align on explicit keys
    left = user_work.rename(columns={value_col: "user_value"})
    right = ref_work.rename(columns={value_col: "ref_value"})
    aligned = pd.merge(left, right, on=on, how="inner")
    if aligned.empty:
        raise ValueError("Alignment produced zero rows; check 'on' keys and overlapping periods/universe")

    # Drop rows with NA in either value
    pre_drop = len(aligned)
    aligned = aligned.dropna(subset=["user_value", "ref_value"]).copy()
    if aligned.empty:
        raise ValueError("After dropping NA values, no overlapping observations remain for comparison")

    time_key = _pick_time_key(on, aligned)
    if sort_by_time and time_key is not None:
        aligned = aligned.sort_values(by=time_key)

    mse, rmse, mae, corr, ic = _compute_metrics(aligned)

    # Populate diagnostics
    diagnostics: Dict[str, Any] = {
        "user_rows": int(len(user)),
        "reference_rows": int(len(reference)),
        "aligned_rows_before_dropna": int(pre_drop),
        "aligned_rows": int(len(aligned)),
        "join_keys": list(on),
        "value_col": value_col,
    }

    # Date range if a time key is present
    if time_key is not None:
        try:
            date_start = pd.to_datetime(aligned[time_key]).min()
            date_end = pd.to_datetime(aligned[time_key]).max()
        except Exception:
            date_start = None
            date_end = None
    else:
        date_start = None
        date_end = None

    pass_thresholds = _evaluate_thresholds(
        mse=mse, rmse=rmse, mae=mae, corr=corr, ic=ic, thresholds=thresholds
    )

    figure: Optional[Figure] = None
    if return_plot:
        title = plot_title or "Factor validation: user vs reference"
        figure = _maybe_plot(aligned, time_key=time_key, title=title)

    return ValidationReport(
        mse=mse,
        rmse=rmse,
        mae=mae,
        corr=corr,
        ic=ic,
        n_obs=int(len(aligned)),
        date_start=date_start,
        date_end=date_end,
        pass_thresholds=pass_thresholds,
        thresholds=thresholds,
        diagnostics=diagnostics,
        figure=figure,
    )

