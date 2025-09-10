from qdl import dataloader, transformer, validator
from qdl.facade import QDL


def main() -> None:
    # Load via core loader and manually project required columns for wide pivot
    df = dataloader.load_factors(country="usa", dataset="mkt", weighting="vw")[
        ["date", "name", "ret"]
    ]
    print(df.head(5))

    wide = transformer.to_wide_factors(df)
    print(wide.head(5))

    # Alternative: load via public API and pivot to wide
    q = QDL()
    df2 = q.load_factors(
        country="usa",
        dataset="mkt",
        weighting="vw",
        columns=["date", "name", "ret"],
    )
    wide2 = transformer.to_wide_factors(df2)
    print(wide2.head(5))

    # Index-aligned validation on shared period (inner join on index)
    # Simulate differing periods between user and reference series
    user_wide = wide2.iloc[12:].copy()   # drop first ~12 rows from user
    ref_wide = wide2.iloc[:-6].copy()    # drop last ~6 rows from reference

    common_idx = user_wide.index.intersection(ref_wide.index)
    user_aligned = user_wide.loc[common_idx, "mkt"]
    ref_aligned = ref_wide.loc[common_idx, "mkt"]

    mse = ((user_aligned - ref_aligned) ** 2).mean()
    print("\nValidation (index inner-join) period:", common_idx.min(), "to", common_idx.max())
    print("Aligned length:", len(common_idx), "MSE:", float(mse))

    # Validation using validator.ValidationReport over explicit join keys (column-based inner join)
    # Build long-form user/reference with differing periods using df2 (date,name,ret)
    user_start = common_idx.min()
    ref_end = common_idx.max()
    user_long = df2[df2["date"] >= user_start]
    ref_long = df2[df2["date"] <= ref_end]

    report = validator.validate_factor(
        user=user_long,
        reference=ref_long,
        on=["date", "name"],
        value_col="ret",
        return_plot=False,
    )
    print("\nValidator report:")
    print("n_obs:", report.n_obs, "date_start:", report.date_start, "date_end:", report.date_end)
    print("mse:", report.mse, "rmse:", report.rmse, "mae:", report.mae, "corr:", report.corr)

    # Load characteristics via public API (JKP vintage and country)
    chars = q.load_chars(
        country="usa",
        vintage="2020-",
        columns=["permno", "me", "be_me"],
    )
    print(chars.head(5))

    # Pivot characteristics to wide (date index, ids as columns) using value column 'me'
    wide_chars = transformer.to_wide_chars(chars, value_col="me")
    print(wide_chars.head(5))


if __name__ == "__main__":
    main()
