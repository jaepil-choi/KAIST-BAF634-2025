"""
qdl.dataloader

PRD v0.2-aligned, schema-agnostic DataLoader core for factors (minimal implementation).

This module currently implements `load_factors` only, following the naming
convention found under `data/factors/`:

    [<country>]_[<dataset>]_[monthly]_[<weighting>].csv

Where:
- <country> ∈ {usa, kor}
- <dataset> ∈ {all_factors, all_themes, mkt}
- frequency is fixed to `monthly`
- <weighting> ∈ {ew, vw, vw_cap}

Schema is intentionally not assumed here; CSVs are loaded as-is. Any parsing,
renaming, or dtype normalization is the responsibility of `qdl.transformer`.

Design policies (from PRD v0.2):
- Do not invent schemas or column names.
- Use absolute imports and centralized path config from `qdl.config`.
- Raise explicit errors; do not synthesize data on failure.
"""

from pathlib import Path
from typing import Literal

import pandas as pd

from qdl.config import FACTORS_PATH

Country = Literal["usa", "kor"]
DatasetKind = Literal["factor", "theme", "mkt"]
Weighting = Literal["ew", "vw", "vw_cap"]
Frequency = Literal["monthly"]


_DATASET_TOKEN_BY_KIND = {
    "factor": "all_factors",
    "theme": "all_themes",
    "mkt": "mkt",
}


def _build_factors_filename(
    *, country: Country, dataset: DatasetKind, frequency: Frequency, weighting: Weighting
) -> str:
    dataset_token = _DATASET_TOKEN_BY_KIND[dataset]
    # File names are literal with square brackets and underscores
    # Example: [usa]_[all_factors]_[monthly]_[ew].csv
    return f"[{country}]_[{dataset_token}]_[{frequency}]_[{weighting}].csv"


def load_factors(
    *,
    country: Country,
    dataset: DatasetKind,
    weighting: Weighting,
    frequency: Frequency = "monthly",
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """
    Load factors CSV from `data/factors/` based on naming convention.

    Parameters
    ----------
    country : {"usa", "kor"}
        Country code segment in file name.
    dataset : {"factor", "theme", "mkt"}
        Logical dataset kind; mapped internally to {"all_factors","all_themes","mkt"}.
    weighting : {"ew", "vw", "vw_cap"}
        Weighting scheme in file name.
    frequency : {"monthly"}, default "monthly"
        Only "monthly" is supported at the moment.
    encoding : str, default "utf-8"
        CSV file encoding.

    Returns
    -------
    pd.DataFrame
        Raw DataFrame loaded via pandas.read_csv. No schema assumptions are made.

    Raises
    ------
    FileNotFoundError
        If the composed file does not exist under `qdl.config.FACTORS_PATH`.
    ValueError
        If any of the provided parameters are invalid for the naming convention.
    """
    # Validate allowed values explicitly to provide clear error messages.
    if country not in ("usa", "kor"):
        raise ValueError("country must be one of {'usa','kor'}")
    if dataset not in _DATASET_TOKEN_BY_KIND:
        raise ValueError("dataset must be one of {'factor','theme','mkt'}")
    if frequency != "monthly":
        raise ValueError("frequency must be 'monthly'")
    if weighting not in ("ew", "vw", "vw_cap"):
        raise ValueError("weighting must be one of {'ew','vw','vw_cap'}")

    file_name = _build_factors_filename(
        country=country, dataset=dataset, frequency=frequency, weighting=weighting
    )
    file_path: Path = FACTORS_PATH / file_name

    if not file_path.exists():
        # Provide a helpful hint listing the directory contents for debugging.
        available = sorted(p.name for p in FACTORS_PATH.glob("*.csv"))
        raise FileNotFoundError(
            "Factors file not found: "
            f"{file_path} (available: {', '.join(available) if available else 'none'})"
        )

    # Schema-agnostic load. Any parsing/normalization belongs in transformer.
    df = pd.read_csv(file_path, encoding=encoding)
    return df
