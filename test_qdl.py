from qdl import dataloader, transformer, validator
import numpy as np
from qdl.facade import QDL


def _assert_close(a: float, b: float, tol: float = 1e-6) -> None:
    assert a is not None
    assert abs(a - b) <= tol, f"Expected {b}, got {a}"


def run_validate_factor_facade_tests() -> None:
    q = QDL()

    # 1) Single factor: Series + answer
    ref = q.load_factors(country="usa", dataset="factor", weighting="ew", factors=["at_gr1"])  # wide
    user_series = ref["at_gr1"].copy()
    report = q.validate_factor(user=user_series, answer="at_gr1", return_plot=False)
    assert report.n_obs > 0
    _assert_close(report.mse, 0.0)
    _assert_close(report.rmse, 0.0)
    _assert_close(report.mae, 0.0)
    _assert_close(report.corr, 1.0)
    print("facade: series + answer OK")

    # 2) Single factor: Series with name inference
    user_series_named = ref["at_gr1"].copy()
    user_series_named.name = "at_gr1"
    report = q.validate_factor(user=user_series_named, return_plot=False)
    assert report.n_obs > 0
    _assert_close(report.corr, 1.0)
    print("facade: series name inference OK")

    # 3) Single factor: DataFrame projection
    user_df = ref.copy()
    report = q.validate_factor(user=user_df, answer="at_gr1", return_plot=False)
    assert report.n_obs > 0
    _assert_close(report.corr, 1.0)
    print("facade: dataframe single-factor projection OK")

    # 4) Multiple factors: DataFrame + answer list
    long_ref = q.load_factors(country="usa", dataset="factor", weighting="ew")
    factors = list(map(str, long_ref.columns[:3]))
    ref_multi = long_ref[factors].copy()
    report = q.validate_factor(user=ref_multi, answer=factors, return_plot=False)
    assert report.n_obs > 0
    assert report.per_factor_metrics is not None
    assert set(report.per_factor_metrics.keys()) == set(factors)
    for name in factors:
        _assert_close(report.per_factor_metrics[name]["mse"], 0.0)
        _assert_close(report.per_factor_metrics[name]["rmse"], 0.0)
        _assert_close(report.per_factor_metrics[name]["mae"], 0.0)
        _assert_close(report.per_factor_metrics[name]["corr"], 1.0)
    print("facade: dataframe multi-factor OK")

    # 5) Explicit reference_df
    report = q.validate_factor(user=ref, reference_df=ref, return_plot=False)
    assert report.n_obs > 0
    _assert_close(report.corr, 1.0)
    print("facade: explicit reference_df OK")

    # 6) Error case: Series without name and no answer
    s = ref["at_gr1"].copy()
    s.name = None
    try:
        _ = q.validate_factor(user=s, return_plot=False)
    except ValueError as e:
        assert "Provide 'answer'" in str(e)
        print("facade: error on unnamed series without answer OK")
    else:
        raise AssertionError("Expected ValueError for unnamed Series without answer")


def main() -> None:
    q = QDL()

    # 1) 퍼사드 load_factor_dataset로 장형(long) 데이터 로드 후 와이드로 피벗
    df_long = q.load_factor_dataset(
        country="usa",
        dataset="factor",
        weighting="vw",
        columns=["date", "name", "ret"],
    )
    print(df_long.head(5))

    wide = transformer.to_wide_factors(df_long)
    print(wide.head(5))

    # 2) 퍼사드 load_factors로 바로 와이드 데이터 로드(선택한 팩터만)
    # 과제 명세의 백틱(``) 변수명을 사용 (시장 mkt 제외)
    selected_factors = [
        "market_equity",  # Size
        "be_me",          # Value
        "ope_be",         # Profitability
        "at_gr1",         # Investment
        "ret_12_1",       # Momentum
        "ret_1_0",        # Short-term reversal
    ]
    wide2 = q.load_factors(
        country="usa",
        dataset="factor",
        weighting="vw",
        factors=selected_factors,
        strict=False,
    )
    print(wide2.head(5))

    # 데모용으로 사용자 시계열에 정규분포 잡음(±0.1로 클립) 추가
    rng = np.random.default_rng(42)
    noise = rng.normal(loc=0.0, scale=0.02, size=wide2.shape)
    noise = np.clip(noise, -0.1, 0.1)
    noisy_wide2 = wide2.add(noise, fill_value=0.0)

    # 인덱스(날짜) 기준 교집합 정렬(내부 조인)
    # 사용자/레퍼런스 기간을 일부 다르게 만들어 시나리오 구성
    user_wide = noisy_wide2.iloc[12:].copy()   # drop first ~12 rows from user
    ref_wide = wide2.iloc[:-6].copy()          # drop last ~6 rows from reference

    common_idx = user_wide.index.intersection(ref_wide.index)
    common_cols = user_wide.columns.intersection(ref_wide.columns)
    user_aligned = user_wide.loc[common_idx, common_cols]
    ref_aligned = ref_wide.loc[common_idx, common_cols]

    print("\n검증(인덱스 내부 조인) 기간:", common_idx.min(), "~", common_idx.max())
    print("정렬된 길이:", len(common_idx))
    print("열 집합 동일 여부:", set(user_aligned.columns) == set(ref_aligned.columns))

    # 와이드 포맷 검증 호출(인덱스/열 교집합 정렬된 DataFrame 사용)
    report = validator.validate_factor(
        user=user_aligned,
        reference=ref_aligned,
        return_plot=True,
        plot_title="Cumsum by factor: user vs reference",
        max_plot_factors=12,
    )
    print("\n검증 리포트:")
    print("관측치수:", report.n_obs, "시작일:", report.date_start, "종료일:", report.date_end)
    def _fmt(x):
        return f"{x:.3f}" if x is not None else "nan"
    print(
        "mse:", _fmt(report.mse),
        "rmse:", _fmt(report.rmse),
        "mae:", _fmt(report.mae),
        "corr:", _fmt(report.corr),
    )
    # Per-factor metrics
    if report.per_factor_metrics:
        print("\n팩터별 지표:")
        for factor, metrics in report.per_factor_metrics.items():
            n = (report.per_factor_n_obs or {}).get(factor)
            mse = _fmt(metrics.get("mse"))
            rmse = _fmt(metrics.get("rmse"))
            mae = _fmt(metrics.get("mae"))
            corr = _fmt(metrics.get("corr"))
            ic = _fmt(metrics.get("ic"))
            print(
                f"{factor}: 관측치수={n}, mse={mse}, rmse={rmse}, mae={mae}, corr={corr}, ic={ic}"
            )
    if report.figure is not None:
        try:
            import matplotlib.pyplot as plt  # type: ignore
            plt.show(report.figure)
        except Exception:
            pass

    # 3) Facade validate_factor API tests
    run_validate_factor_facade_tests()

    # 특성 데이터 로드(JKP 빈티지/국가 기준)
    chars = q.load_chars(
        country="usa",
        vintage="2020-",
        columns=["permno", "me", "be_me"],
    )
    print(chars.head(5))

    # 특성 데이터를 와이드로 피벗(날짜 인덱스, id 컬럼), 값은 'me'
    wide_chars = transformer.to_wide_chars(chars, value_col="me", date_col="eom")
    print(wide_chars.head(5))


if __name__ == "__main__":
    main()
