"""
qdl.facade

Minimal facade exposing only load and validate_factor per PRD v0.2.

- Transform and preprocessing are internal concerns handled by underlying modules.
- Facade orchestrates dataloader and validator without assuming schemas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

import pandas as pd

from qdl import dataloader as _dataloader  # absolute import per project policy
from qdl import validator as _validator    # validator API expected to be defined later
from qdl import transformer as _transformer


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

    def load_factor_dataset(
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
        Load the raw long-form factor dataset (CSV) via the public API.

        Delegates to dataloader.load_factors.

        Notes
        -----
        - Returns long-form data.
        - Regardless of the requested `columns`, the composite identifier ["date","name"]
          is always included to support downstream operations.
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

        # Always include composite identifier keys for factors
        required_keys = ["date", "name"]
        requested_with_required = list(dict.fromkeys([*columns, *required_keys]))

        missing = [c for c in requested_with_required if c not in df.columns]
        if missing and strict:
            raise KeyError(f"Requested columns not found: {missing}")

        # Order keys first, then the remaining requested columns preserving order
        keys_first = [c for c in required_keys if c in df.columns]
        rest = [c for c in requested_with_required if c in df.columns and c not in required_keys]
        return df[keys_first + rest]

    def load_factors(
        self,
        *,
        country: Literal["usa", "kor"],
        dataset: Literal["factor", "theme", "mkt"],
        weighting: Literal["ew", "vw", "vw_cap"],
        frequency: Literal["monthly"] = "monthly",
        encoding: str = "utf-8",
        factors: Optional[List[str]] = None,
        strict: bool = True,
    ) -> pd.DataFrame:
        """
        Load factors and return a wide DataFrame (date index, factor names as columns).

        Parameters
        ----------
        factors : list[str], optional
            Subset of factor names (wide columns) to return. If provided and `strict=True`,
            raise when any requested factor is missing. If `strict=False`, return the
            intersection silently.
        """
        long_df = self.load_factor_dataset(
            country=country,
            dataset=dataset,
            weighting=weighting,
            frequency=frequency,
            encoding=encoding,
            columns=["date", "name", "ret"],
            strict=True,
        )
        wide = _transformer.to_wide_factors(long_df)
        if factors is None:
            return wide
        missing = [f for f in factors if f not in wide.columns]
        if missing and strict:
            raise KeyError(f"Requested factors not found: {missing}")
        present_in_order = [f for f in factors if f in wide.columns]
        return wide[present_in_order]

    def load_char_dataset(
        self,
        *,
        country: Literal["usa", "kor"],
        vintage: Literal["1972-", "2000-", "2020-"],
        columns: Optional[List[str]] = None,
        engine: str = "pyarrow",
        strict: bool = True,
        id_col: Literal["id"] = "id",
        date_col: Literal["eom", "date"] = "eom",
    ) -> pd.DataFrame:
        """
        Load JKP characteristics datasets (Parquet) via the public API.

        Constructs the filename from (vintage, country) and delegates to dataloader.load_chars.

        Notes
        -----
        - Regardless of the requested `columns`, the composite identifier
          [date_col, id_col] is always included in the returned frame to support
          downstream operations (e.g., pivoting). `date_col` must be one of {"eom","date"};
          `id_col` is fixed to "id".
        """
        file_name = f"jkp_{vintage}_{country}.parquet"
        # Always include composite identifier keys for chars
        required_keys = [date_col, id_col]
        if columns is None:
            requested_with_required = None
        else:
            requested_with_required = list(dict.fromkeys([*columns, *required_keys]))

        if requested_with_required is None or strict:
            # Strict mode (or no projection): delegate directly; underlying reader will raise on missing columns
            return self._loader.load_chars(
                file_name=file_name,
                columns=requested_with_required,
                engine=engine,
            )

        # Non-strict with projection: try pushdown first; if it fails, load all and filter intersection
        try:
            return self._loader.load_chars(
                file_name=file_name,
                columns=requested_with_required,
                engine=engine,
            )
        except (KeyError, ValueError):
            df_all = self._loader.load_chars(
                file_name=file_name,
                columns=None,
                engine=engine,
            )
            target_cols = requested_with_required or []
            keys_first = [c for c in required_keys if c in df_all.columns]
            rest = [c for c in target_cols if c in df_all.columns and c not in required_keys]
            return df_all[keys_first + rest]

    # Backward-compatible alias to previous API name
    def load_chars(
        self,
        *,
        country: Literal["usa", "kor"],
        vintage: Literal["1972-", "2000-", "2020-"],
        columns: Optional[List[str]] = None,
        engine: str = "pyarrow",
        strict: bool = True,
        id_col: Literal["id"] = "id",
        date_col: Literal["eom", "date"] = "eom",
    ) -> pd.DataFrame:
        return self.load_char_dataset(
            country=country,
            vintage=vintage,
            columns=columns,
            engine=engine,
            strict=strict,
            id_col=id_col,
            date_col=date_col,
        )

    def load_char(
        self,
        *,
        country: Literal["usa", "kor"],
        vintage: Literal["1972-", "2000-", "2020-"],
        char: str,
        engine: str = "pyarrow",
        strict: bool = True,
        id_col: Literal["id"] = "id",
        date_col: Literal["eom", "date"] = "eom",
    ) -> pd.DataFrame:
        """
        Load a single characteristic and return a 2D wide DataFrame with `date_col` as index
        and `id_col` as columns, values from the specified `char` column.
        """
        # Ensure required columns are present (strict load to surface errors early)
        df = self.load_char_dataset(
            country=country,
            vintage=vintage,
            columns=[date_col, id_col, char],
            engine=engine,
            strict=True if strict else False,
            id_col=id_col,
            date_col=date_col,
        )
        # Pivot to wide
        wide = _transformer.to_wide(
            df,
            index_cols=[date_col],
            column_col=id_col,
            value_col=char,
            agg="first",
            sort_index=True,
            sort_columns=True,
        )
        return wide

    def validate_factor(
        self,
        *,
        user: Union[pd.Series, pd.DataFrame],
        answer: Optional[Union[str, List[str]]] = None,
        reference_df: Optional[pd.DataFrame] = None,
        # Optional convenience params for auto-loading reference factors
        country: Literal["usa", "kor"] = "usa",
        dataset: Literal["factor", "theme", "mkt"] = "factor",
        weighting: Literal["ew", "vw", "vw_cap"] = "ew",
        frequency: Literal["monthly"] = "monthly",
        encoding: str = "utf-8",
        strict: bool = True,
        **kwargs: Any,
    ) -> Any:
        """Validate factor returns using a simple Series/DataFrame + factor-name(s) interface.

        This convenience wrapper expects wide-form factor data (date index, factor names as columns)
        as used by qdl.validator.validate_factor.

        Usage patterns
        --------------
        - Single factor:
          - user: pd.Series (index=date), answer: str factor name
          - or user: pd.DataFrame with one column; answer optionally the same name
        - Multiple factors:
          - user: pd.DataFrame with columns of factor names; answer: list[str] (optional). If omitted,
            all user columns are used.

        Reference data
        --------------
        - If reference_df is provided, it is used directly (wide form expected)
        - Otherwise, reference factors are auto-loaded via load_factors(...) using (country, dataset,
          weighting, frequency, encoding) and the requested factor names.
        """

        # Normalize user input to wide DataFrame and determine which factors to load
        if isinstance(user, pd.Series):
            # Series → single factor; infer name from 'answer' or the series name
            if isinstance(answer, list):
                raise ValueError("When 'user' is a Series, 'answer' must be a single factor name (str)")
            col_name: Optional[str]
            if isinstance(answer, str):
                col_name = answer
            else:
                col_name = str(user.name) if user.name is not None else None
            if not col_name:
                raise ValueError("Provide 'answer' as the factor name or set Series.name to the factor name")
            user_wide = user.to_frame(name=str(col_name))
            factors_to_load: List[str] = [str(col_name)]
        elif isinstance(user, pd.DataFrame):
            user_wide = user
            if answer is None:
                factors_to_load = [str(c) for c in user_wide.columns]
            elif isinstance(answer, str):
                factors_to_load = [answer]
                # If user has more columns than requested, project to the requested set when present
                if answer in user_wide.columns:
                    user_wide = user_wide[[answer]]
                elif strict:
                    raise KeyError(f"User DataFrame does not contain requested factor column: {answer}")
            else:
                # list[str]
                factors_to_load = [str(a) for a in answer]
                missing = [a for a in factors_to_load if a not in user_wide.columns]
                if missing and strict:
                    raise KeyError(f"User DataFrame missing requested factor columns: {missing}")
                # Keep only requested columns, in provided order, when present
                present_in_order = [a for a in factors_to_load if a in user_wide.columns]
                if present_in_order:
                    user_wide = user_wide[present_in_order]
        else:
            raise TypeError("'user' must be a pandas Series or DataFrame in wide form (date index)")

        # Resolve reference
        if reference_df is not None:
            ref_wide = reference_df
        else:
            # Auto-load the reference factors via the facade
            ref_wide = self.load_factors(
                country=country,
                dataset=dataset,
                weighting=weighting,
                frequency=frequency,
                encoding=encoding,
                factors=factors_to_load,
                strict=strict,
            )

        # Delegate to validator (expects wide-form)
        return self._validator.validate_factor(
            user=user_wide,
            reference=ref_wide,
            **kwargs,
        )
