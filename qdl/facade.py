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

    def load(
        self,
        domain: Literal["factors"],
        /,
        *,
        country: Literal["usa", "kor"],
        dataset: Literal["factor", "theme", "mkt"],
        weighting: Literal["ew", "vw", "vw_cap"],
        frequency: Literal["monthly"] = "monthly",
        encoding: str = "utf-8",
    ) -> pd.DataFrame:
        """
        Load datasets by domain.

        Currently supports only domain="factors" and delegates to dataloader.load_factors.
        """
        if domain != "factors":
            raise NotImplementedError("Only domain='factors' is supported by the facade at this stage")
        return self._loader.load_factors(
            country=country,
            dataset=dataset,
            weighting=weighting,
            frequency=frequency,
            encoding=encoding,
        )

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
            Parameters forwarded to self.load(domain='factors', **params) when reference_df is not provided.
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
            ref = self.load("factors", **reference_load_params)
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
