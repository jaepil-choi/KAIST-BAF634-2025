from qdl import dataloader, transformer


def main() -> None:
    df = dataloader.load_factors(country="usa", dataset="mkt", weighting="vw")
    print(df.head(5))

    wide = transformer.to_wide_factors(df)
    print(wide.head(5))


if __name__ == "__main__":
    main()
