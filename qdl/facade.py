"""
qdl.facade

Minimal facade exposing only load and validate_factor per PRD v0.2.

- Transform and preprocessing are internal concerns handled by underlying modules.
- Facade orchestrates dataloader and validator without assuming schemas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

import pandas as pd

from qdl import dataloader as _dataloader  # absolute import per project policy
from qdl import validator as _validator    # validator API expected to be defined later


class QDL:
    """
    Facade for end users. Exposes only load and validate_factor.

    Notes
    -----
    - This class delegates to qdl.dataloader and qdl.validator.
    - No schema assumptions are made here; callers must provide keys explicitly
      or rely on later config-driven resolution when available.
    """

    def __init__(self, *, loader: Any = None, validator: Any = None) -> None:
        # Allow dependency injection for tests/extensibility
        self._loader = loader or _dataloader
        self._validator = validator or _validator

    def load_factors(
        self,
        *,
        country: Literal["usa", "kor"],
        dataset: Literal["factor", "theme", "mkt"],
        weighting: Literal["ew", "vw", "vw_cap"],
        frequency: Literal["monthly"] = "monthly",
        encoding: str = "utf-8",
        columns: Optional[List[str]] = None,
        strict: bool = True,
    ) -> pd.DataFrame:
        """
        Load factor datasets (CSV) via the public API.

        Delegates to dataloader.load_factors.
        """
        df = self._loader.load_factors(
            country=country,
            dataset=dataset,
            weighting=weighting,
            frequency=frequency,
            encoding=encoding,
        )
        if columns is None:
            return df

        missing = [c for c in columns if c not in df.columns]
        if missing and strict:
            raise KeyError(f"Requested columns not found: {missing}")

        present_in_order = [c for c in columns if c in df.columns]
        return df[present_in_order]

    def load_chars(
        self,
        *,
        country: Literal["usa", "kor"],
        vintage: Literal["1972-", "2000-", "2020-"],
        columns: Optional[List[str]] = None,
        engine: str = "pyarrow",
        strict: bool = True,
    ) -> pd.DataFrame:
        """
        Load JKP characteristics datasets (Parquet) via the public API.

        Constructs the filename from (vintage, country) and delegates to dataloader.load_chars.
        """
        file_name = f"jkp_{vintage}_{country}.parquet"
        if columns is None or strict:
            # Strict mode (or no projection): delegate directly; underlying reader will raise on missing columns
            return self._loader.load_chars(
                file_name=file_name,
                columns=columns,
                engine=engine,
            )

        # Non-strict with projection: try pushdown first; if it fails, load all and filter intersection
        try:
            return self._loader.load_chars(
                file_name=file_name,
                columns=columns,
                engine=engine,
            )
        except (KeyError, ValueError):
            df_all = self._loader.load_chars(
                file_name=file_name,
                columns=None,
                engine=engine,
            )
            present_in_order = [c for c in columns if c in df_all.columns]
            return df_all[present_in_order]

    def validate_factor(
        self,
        *,
        user_df: pd.DataFrame,
        reference_df: Optional[pd.DataFrame] = None,
        on: Optional[List[str]] = None,
        value_col: Optional[str] = None,
        reference_load_params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Validate a user-generated factor series against a reference.

        Parameters
        ----------
        user_df : pd.DataFrame
            User-provided factor data.
        reference_df : pd.DataFrame, optional
            Reference factor data. If not provided, it will be loaded using reference_load_params.
        on : list[str]
            Join keys for alignment (e.g., [time, series-id]). Required (no PRD default).
        value_col : str
            Name of the numeric value column to compare. Required (no PRD default).
        reference_load_params : dict, optional
            Parameters forwarded to self.load_factors(**params) when reference_df is not provided.
        kwargs : Any
            Forwarded to the underlying validator implementation (e.g., thresholds).
        """
        if on is None or value_col is None:
            raise ValueError("validate_factor requires explicit 'on' and 'value_col' arguments")

        if reference_df is None:
            if not reference_load_params:
                raise ValueError(
                    "reference_df is None and reference_load_params not provided; cannot load reference"
                )
            ref = self.load_factors(**reference_load_params)
        else:
            ref = reference_df

        # Delegate to validator; assumes a compatible API exists.
        return self._validator.validate_factor(
            user=user_df,
            reference=ref,
            on=on,
            value_col=value_col,
            **kwargs,
        )
