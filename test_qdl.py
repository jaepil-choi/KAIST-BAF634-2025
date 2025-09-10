from qdl import dataloader, transformer, validator
import numpy as np
from qdl.facade import QDL


def main() -> None:
    q = QDL()

    # 1) Load long-form via facade.load_factor_dataset and pivot to wide
    df_long = q.load_factor_dataset(
        country="usa",
        dataset="factor",
        weighting="vw",
        columns=["date", "name", "ret"],
    )
    print(df_long.head(5))

    wide = transformer.to_wide_factors(df_long)
    print(wide.head(5))

    # 2) Load directly as wide via facade.load_factors (with factor selection)
    selected_factors = ["qmj", "sale_gr1", "ivol_ff3_21d", "cash_at", "be_me"]
    wide2 = q.load_factors(
        country="usa",
        dataset="factor",
        weighting="vw",
        factors=selected_factors,
        strict=False,
    )
    print(wide2.head(5))

    # Add clipped normal noise to create a distinct user series for demo
    rng = np.random.default_rng(42)
    noise = rng.normal(loc=0.0, scale=0.02, size=wide2.shape)
    noise = np.clip(noise, -0.1, 0.1)
    noisy_wide2 = wide2.add(noise, fill_value=0.0)

    # Index-aligned validation on shared period (inner join on index)
    # Simulate differing periods between user and reference series
    user_wide = noisy_wide2.iloc[12:].copy()   # drop first ~12 rows from user
    ref_wide = wide2.iloc[:-6].copy()          # drop last ~6 rows from reference

    common_idx = user_wide.index.intersection(ref_wide.index)
    common_cols = user_wide.columns.intersection(ref_wide.columns)
    user_aligned = user_wide.loc[common_idx, common_cols]
    ref_aligned = ref_wide.loc[common_idx, common_cols]

    print("\nValidation (index inner-join) period:", common_idx.min(), "to", common_idx.max())
    print("Aligned length:", len(common_idx))
    print("Columns equal (set):", set(user_aligned.columns) == set(ref_aligned.columns))

    # Validation using validator.ValidationReport over explicit join keys (column-based inner join)
    # Build long-form user/reference with differing periods and propagate the same noise to user
    user_start = common_idx.min()
    ref_end = common_idx.max()
    user_long = df_long[df_long["date"] >= user_start].copy()
    ref_long = df_long[df_long["date"] <= ref_end].copy()
    # Restrict to selected factors for validation
    user_long = user_long[user_long["name"].isin(selected_factors)]
    ref_long = ref_long[ref_long["name"].isin(selected_factors)]

    # Convert wide noise to long and merge to add noise to user_long 'ret'
    # Reconstruct as DataFrame with matching index/columns (same noise as wide2 above)
    import pandas as pd
    noise_df = pd.DataFrame(noise, index=wide2.index, columns=wide2.columns)
    noise_long = noise_df.stack().reset_index()
    noise_long.columns = ["date", "name", "_noise"]
    user_long = user_long.merge(noise_long, on=["date", "name"], how="left")
    user_long["_noise"] = user_long["_noise"].fillna(0.0)
    user_long["ret"] = user_long["ret"] + user_long["_noise"]
    user_long = user_long.drop(columns=["_noise"])  # clean up

    report = validator.validate_factor(
        user=user_long,
        reference=ref_long,
        on=["date", "name"],
        value_col="ret",
        return_plot=True,
        plot_title="Cumsum by factor: user vs reference",
        max_plot_factors=12,
    )
    print("\nValidator report:")
    print("n_obs:", report.n_obs, "date_start:", report.date_start, "date_end:", report.date_end)
    print("mse:", report.mse, "rmse:", report.rmse, "mae:", report.mae, "corr:", report.corr)
    # Per-factor metrics
    if report.per_factor_metrics:
        print("\nPer-factor metrics:")
        for factor, metrics in report.per_factor_metrics.items():
            n = (report.per_factor_n_obs or {}).get(factor)
            mse = metrics.get("mse")
            rmse = metrics.get("rmse")
            mae = metrics.get("mae")
            corr = metrics.get("corr")
            ic = metrics.get("ic")
            print(
                f"{factor}: n_obs={n}, mse={mse}, rmse={rmse}, mae={mae}, corr={corr}, ic={ic}"
            )
    if report.figure is not None:
        try:
            import matplotlib.pyplot as plt  # type: ignore
            plt.show(report.figure)
        except Exception:
            pass

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
