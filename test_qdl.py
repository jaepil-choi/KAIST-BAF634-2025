from qdl import dataloader, transformer
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
