### QDL (Quant Data Loader) — Product Requirements Document (PRD)

- **Document owner**: qdl module maintainers
- **Status**: Draft v0.2
- **Scope**: Define requirements for loading, transforming, and validating quant datasets via a simple facade.

### 1) Critical assessment of initial requirements

- **Ambiguities to clarify**:
  - Column names and schemas are not fixed in this PRD. They will be defined externally (e.g., `data/meta/data_spec.yaml` and later `qdl/config.py`/`qdl/config.yaml`). No concrete column names are assumed here.
  - Time conventions: frequency (monthly unless specified), end-of-period dating vs start; timezone handling. Exact time column name(s) will be configured.
  - Canonical identifiers for assets and countries/regions are not pre-decided. Exact field names will be configured.
  - Factor return alignment (EW, VW, VW by cap) and rebalance conventions depend on dataset metadata; not assumed here.
  - Missing-data policy for joins and validation (intersection vs union, NA handling) must be explicitly set; no silent defaults.
  - File encodings and dtype hints must be declared or inferred conservatively; avoid silent coercion.

### 2) Goals and non-goals

- **Goals**:
  - Provide consistent loading from `data/` subfolders: `chars/`, `factors/`, `meta/`, `returns/`.
  - Preprocess and convert datasets between long and wide formats with stable, schema-agnostic APIs.
  - Validate user-produced factor returns against canonical factor data using quantitative metrics.
  - Expose a simple facade API for most users, while keeping internal modules modular.
- **Non-goals**:
  - Running portfolio construction or backtests.
  - Data acquisition from external sources (assume files already exist locally).
  - Finalizing concrete schemas within this PRD (schemas are externalized and TBD).

### 3) Users and primary use cases

- **Users**: Students and researchers constructing factors; engineers wiring data pipelines.
- **Use cases**:
  - Load canonical factors and characteristics.
  - Transform into modeling-ready long/wide formats.
  - Compute custom factor returns and compare against canonical series.

### 4) Data model and directory layout

- **Directory layout**:
  - `data/chars/`: cross-sectional characteristics; CSV or Parquet.
  - `data/factors/`: canonical factor return series; CSV or Parquet.
  - `data/meta/`: data catalogs/specs (e.g., `data_spec.yaml`).
  - `data/returns/`: raw asset returns; CSV or Parquet.
- **File formats**: `.csv` (UTF-8, header present) and `.parquet` (pyarrow). Unknown files ignored.

### 4.1) Schema policy (TBD, externalized)

- **Schema source of truth**: Declared in `data/meta/data_spec.yaml` and/or `qdl/config.*`. This PRD does not name concrete columns.
- **Time fields**: One or more time columns may exist; exact names are configured. Frequency defaults to monthly unless specified.
- **Entity identifiers**: Asset or series identifiers exist; exact names are configured.
- **Regional fields**: Optional country/region fields; exact names are configured.
- **Value fields**: One or more numeric columns designated as values; names are configured.
- **Typing**: Dtypes are applied per configuration or conservative inference; failures raise errors. No silent synthesis.

### 4.2) Format conventions (schema-agnostic)

- **Long format**: A single time column, one categorical/dimension column that enumerates series/variables, and one numeric value column. Exact column names are user-configured.
- **Wide format**: One or more index columns (e.g., time, entity) form the row index; one categorical/dimension column becomes the wide column axis; one numeric column provides values. Exact column names are user-configured.
- **Characteristics (conceptual)**: Long format indexed by time and entity with a variable name and value; or wide format with `[time, entity]` as index and variables as columns. Exact names are user-configured.

### 5) Functional requirements

#### 5.1) DataLoader (`qdl/dataloader.py`)

- **Responsibilities**:
  - Discover and load files from the `data/` tree by domain (`chars`, `factors`, `meta`, `returns`).
  - Support CSV and Parquet with consistent parsing, dtypes, and time handling.
- **API (proposed)**:
  - `list_datasets(domain: str) -> list[Path]`: enumerate files in a domain.
  - `load_chars(...)-> pd.DataFrame`
  - `load_factors(...)-> pd.DataFrame`
  - `load_meta(...)-> pd.DataFrame | dict`
  - `load_returns(...)-> pd.DataFrame`
  - `load_by_path(path: Path | str) -> pd.DataFrame`
- **Params (common)**:
  - `base_path: PathLike = "data"`, `domain: Literal["chars","factors","meta","returns"]`.
  - `patterns: Optional[list[str]]` to filter files by glob-like name patterns.
  - `engine`: `"pyarrow"` for parquet; CSV via pandas default.
  - `parse_dates: Optional[list[str]] = None` (names provided by user/config; no PRD default).
  - `encoding: Optional[str] = "utf-8"`.
  - Optional `usecols`, `dtype` hints.
- **Behavior**:
  - Parse configured time columns and sort ascending by them (and additional keys if provided).
  - Drop fully empty rows; optionally standardize column names (case and whitespace), if enabled by config.
  - Enforce numeric types for configured value columns; raise on irrecoverable parsing.
  - Do not assume column names; require explicit parameters or configuration.
- **Errors**:
  - Raise `FileNotFoundError` when no files match; `ValueError` on schema violations; never silently synthesize data.
- **Performance**:
  - For large CSVs, allow `usecols` and `dtype` hints; Parquet read via pyarrow; optionally memory-map.

#### 5.2) Transformer (`qdl/transformer.py`)

- **Responsibilities**:
  - Preprocess raw loaded frames and convert between long/wide without assuming concrete column names.
- **API (proposed)**:
  - `preprocess(df: pd.DataFrame, *, drop_duplicates=True, trim_strings=True, standardize_cols=True) -> pd.DataFrame`
  - `to_long(df: pd.DataFrame, *, index_cols: list[str], value_vars: list[str], var_name: str, value_name: str) -> pd.DataFrame`
  - `to_wide(df: pd.DataFrame, *, index_cols: list[str], column_col: str, value_col: str, agg: Literal["mean","sum","first"] = "first") -> pd.DataFrame`
  - `standardize_schema(df: pd.DataFrame, schema: dict) -> pd.DataFrame` (minimal field presence and dtype checks).
- **Behavior**:
  - Normalize column names to a consistent style if enabled (e.g., snake_case); strip whitespace; cast configured time columns; sort by keys.
  - For long→wide and wide→long, ensure no duplicate keys; if duplicates exist, aggregate per `agg`.
  - Validate presence of required columns per the provided schema or parameters before conversion.
- **Errors**:
  - Raise `KeyError` when required columns are missing; `ValueError` when duplicates cannot be resolved.

#### 5.3) Validator (`qdl/validator.py`)

- **Responsibilities**:
  - Compare user-generated factor returns to canonical factors loaded via DataLoader.
- **Metrics**:
  - `MSE`, `RMSE`, `MAE`, `Pearson correlation`, `Information Coefficient (rank correlation)`.
- **Alignment**:
  - Join on explicitly provided key columns (e.g., time and optional group keys). Optional resample/align step (e.g., month end), driven by parameters or config.
  - Ensure comparison is on identical weighting scheme and universe, if specified.
- **API (proposed)**:
  - `validate_factor(user: pd.DataFrame, reference: pd.DataFrame, *, on: list[str], value_col: str, group_on: Optional[list[str]] = None, thresholds: Optional[dict] = None) -> ValidationReport`
  - `ValidationReport`: dataclass `{mse, rmse, mae, corr, ic, n_obs, date_start, date_end, pass_thresholds: bool, diagnostics: dict}`.
- **Defaults**:
  - No hard-coded defaults for `on` or `value_col` in PRD. Callers must specify them or supply a schema key that resolves via config.
- **Errors**:
  - Raise `ValueError` when alignment yields zero overlap or when schemas mismatch.

#### 5.4) Facade (`qdl/facade.py`)

- **Responsibilities**: Provide a simplified interface for end users.
- **API (proposed)**:
  - `class QDL:`
    - `load(domain: Literal["chars","factors","meta","returns"], **kwargs) -> pd.DataFrame`
    - `transform_to_long(df, **kwargs) -> pd.DataFrame`
    - `transform_to_wide(df, **kwargs) -> pd.DataFrame`
    - `preprocess(df, **kwargs) -> pd.DataFrame`
    - `validate_factor(user_df, reference_df=None, *, on: list[str] | None = None, value_col: str | None = None, schema_key: str | None = None, **kwargs) -> ValidationReport`
- **Behavior**:
  - Construct and hold internal DataLoader and Transformer instances; optionally accept them via DI for testing.
  - Accept either explicit column names via arguments or a `schema_key` that resolves names from config/meta.
  - Offer sensible defaults only when provided by configuration; avoid implicit assumptions.

### 6) Non-functional requirements

- **Performance**: Load 1M-row CSV within 5–10s on typical laptop; wide/long pivot within memory limits.
- **Reliability**: Deterministic transforms; explicit errors on schema issues; no silent coercions.
- **Compatibility**: Python 3.9+; Windows/macOS/Linux; `pandas`, `pyarrow` dependencies.
- **Observability**: Structured logging at INFO/DEBUG; timings for load/transform/validate.
- **I/O and paths**: Use `pathlib.Path`; avoid OS-specific separators; UTF-8 everywhere.
- **Typing**: Public APIs type-annotated; mypy-friendly where practical.

### 7) Example flows (schema-agnostic)

- **Load → Transform (wide)**:
  1. `df = qdl.load("factors", patterns=["..."])`
  2. `df = qdl.preprocess(df)`
  3. `wide = qdl.transform_to_wide(df, index_cols=[TIME_COL], column_col=SERIES_ID_COL, value_col=VALUE_COL)`
- **User factor validation**:
  1. User computes a dataframe with a time key, an identifier for the series, and a numeric value column.
  2. `ref = qdl.load("factors", patterns=["..."])`
  3. `report = qdl.validate_factor(user_df=user_df, reference_df=ref, on=[TIME_COL, SERIES_ID_COL], value_col=VALUE_COL)`

Note: `TIME_COL`, `SERIES_ID_COL`, and `VALUE_COL` are placeholders for user- or config-specified column names.

### 8) Acceptance criteria

- **DataLoader**: Loads sample CSV and Parquet from each domain; configured time column(s) parsed; errors on missing files or undeclared schemas; no assumed column names.
- **Transformer**: Correct long↔wide conversions with deterministic aggregation; raises on duplicate key conflicts without agg; requires explicit column parameters or schema.
- **Validator**: Computes metrics on overlapping keys; raises on zero-overlap; report contains all fields with correct types; requires explicit `on` and `value_col` or schema key.
- **Facade**: Single `QDL` instance can complete both example flows using only facade methods; respects config-driven schemas or explicit arguments.

### 9) Open questions

- Where is the authoritative schema maintained: `data/meta/data_spec.yaml`, `qdl/config.yaml`, or both? How are conflicts resolved?
- Do we expose canonical defaults for time and identifier columns per domain, or require explicit inputs in all calls?
- Should we auto-infer weighting scheme and universe from filenames/metadata or require explicit selection?
- Do we include IC by horizon (e.g., next-month returns) in Validator, or only same-period series?
- Should Transformer include optional outlier handling (winsorization) by default, or leave to users?
