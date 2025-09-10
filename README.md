# QDL (Quant Data Loader)

이 저장소는 KAIST `고급금융계량분석` 과목의 과제(FF5 + Momentum + STR 팩터 복제)를 위한 실습용 코드와 데이터를 제공합니다. 핵심 과제 설명은 `docs/assignment_ff5.md` 를 참고합니다.

## 목적과 범위

- 과제 목적: JKP 특성 데이터를 이용하여 7개 팩터(SMB, HML, RMW, CMA, Mkt, Momentum, STR)의 월별 수익률을 복제하고, 제공된 기준(reference)과의 오차를 검증합니다.
- 범위: 데이터 로드(요인/특성), 팩터 검증(지표·플롯), 퍼사드 기반의 일관된 사용 경험 제공.
- 데이터 출처: jkpfactors.com (Jensen, Kelly, Pedersen, 2023). 인용은 과제 문서 참조.

## 주요 기능

### 데이터 로더

- `QDL` 클래스를 사용해 요인(factors)과 특성(characteristics) 데이터를 간단히 로드합니다.
- 파일 명명 규칙을 따르는 CSV/Parquet를 읽고, 스키마 가정 없이 반환합니다.

### 검증

- 사용자가 산출한 팩터 시계열을 기준(reference)과 비교하여 지표(MSE, RMSE, MAE, corr, IC)와 비교 플롯을 제공합니다.
- `QDL.validate_factor` 로 간단히 사용할 수 있습니다.

## 빠른 시작

```python
from qdl.facade import QDL

q = QDL()

# 1) 요인 데이터 로드 (와이드: 날짜×팩터)
wide = q.load_factors(
    country="usa",
    dataset="factor",
    weighting="vw",
)
print(wide.head())

# 2) 요인 데이터 로드 (롱: date, name, ret 컬럼만)
long = q.load_factor_dataset(
    country="usa",
    dataset="factor",
    weighting="vw",
    columns=["date", "name", "ret"],
)
print(long.head())

# 3) 팩터 검증 (사용자 vs 기준)
# 기준을 직접 전달하거나, 아래처럼 reference_load_params 로 로드할 수 있습니다.
report = q.validate_factor(
    user_df=long,                 # 사용자 팩터(롱 포맷)
    reference_df=None,            # 생략 시 아래 파라미터로 기준 로드
    reference_load_params={
        "country": "usa",
        "dataset": "factor",
        "weighting": "vw",
        "frequency": "monthly",
        "encoding": "utf-8",
    },
    on=["date", "name"],        # 조인 키(명시적)
    value_col="ret",            # 비교할 값 컬럼명
    thresholds={"corr_min": 0.9},
    return_plot=True,
    plot_title="Cumsum by factor: user vs reference",
    max_plot_factors=12,
)
print("n_obs=", report.n_obs, "mse=", report.mse, "corr=", report.corr)

# 4) 특성 데이터 로드 (빈티지/국가)
chars = q.load_chars(
    country="usa",
    vintage="2020-",
    columns=["date", "id", "be_me"],
)
print(chars.head())
```

> 주의: 예시는 `QDL` 클래스만 사용합니다. 내부 모듈 구현 세부는 다루지 않습니다.

## 사용 가능한 메서드와 파라미터

아래 파라미터는 `qdl/dataloader.py`, `qdl/validator.py` 구현을 근거로 요약했습니다. 공개 메서드만 간단히 소개합니다.

### QDL.load_factor_dataset(...) -> pd.DataFrame (롱 포맷)

- country: {"usa", "kor"} (필수)
- dataset: {"factor", "theme", "mkt"} (필수)
- weighting: {"ew", "vw", "vw_cap"} (필수)
- frequency: {"monthly"} = "monthly"
- encoding: str = "utf-8"
- columns: list[str] | None = None  (요청 시, 내부적으로 ["date","name"]는 항상 포함)
- strict: bool = True  (요청한 컬럼이 없으면 오류)

설명: `data/factors/` 내 파일 명명 규칙을 조합해 CSV를 로드합니다. 스키마는 가정하지 않으며, 파싱·피벗 등은 내부에서 처리됩니다.

### QDL.load_factors(...) -> pd.DataFrame (와이드 포맷)

- 인수는 `load_factor_dataset` 과 동일 +
- factors: list[str] | None = None  (선택한 팩터 컬럼만 반환)
- strict: bool = True  (요청 팩터가 없으면 오류)

설명: 내부적으로 `load_factor_dataset(..., columns=["date","name","ret"])` 로 롱 포맷을 읽은 뒤, 날짜 인덱스×팩터 컬럼의 와이드 포맷으로 변환합니다.

### QDL.load_chars(...) -> pd.DataFrame (특성 롱 포맷)

- country: {"usa", "kor"} (필수)
- vintage: {"1972-", "2000-", "2020-"} (필수)
- columns: list[str] | None = None  (요청 시, 내부적으로 ["date","id"]는 항상 포함)
- engine: str = "pyarrow"
- strict: bool = True

설명: `data/chars/` 에서 빈티지·국가 조합으로 Parquet 파일을 선택해 로드합니다. 스키마는 가정하지 않습니다.

### QDL.load_char(...) -> pd.DataFrame (2D 와이드: index=date, columns=id)

- country, vintage, char, engine, strict (상동)
- 설명: 지정한 단일 특성 `char` 컬럼을 와이드 형태(날짜×id)로 피벗하여 반환합니다.

### QDL.validate_factor(...)

- user_df: pd.DataFrame (필수)
- reference_df: pd.DataFrame | None = None (미제공 시 `reference_load_params` 로 로드)
- on: list[str] (필수, 예: ["date", "name"]) — 조인 키
- value_col: str (필수, 예: "ret") — 비교 값 컬럼
- reference_load_params: dict | None — `QDL.load_factor_dataset(**params)` 에 전달될 인수
- names: list[str] | None — (롱 포맷에서) 특정 팩터명만 필터링
- 기타 kwargs: `qdl.validator.validate_factor` 로 전달

검증 옵션:

- thresholds: dict | None — {"mse_max", "rmse_max", "mae_max", "corr_min", "ic_min"}
- return_plot: bool = True — Matplotlib 가능 시 비교 플롯 반환
- plot_title: str | None — 플롯 제목
- sort_by_time: bool = True — 시간 키 정렬
- max_plot_factors: int = 8 — 이름별 서브플롯 최대 개수

반환: `ValidationReport`

- mse, rmse, mae, corr, ic, n_obs, date_start, date_end, pass_thresholds, thresholds, diagnostics, figure(옵션), per_factor_metrics/obs(옵션)

## 참고: 과제 문서

- 과제 개요·요건·검증 방식은 `docs/assignment_ff5.md` 에 상세히 기술되어 있습니다.

## 원칙

- **단일 공개 API 우선**: 퍼사드(`QDL`)만 사용합니다.
- **명시성**: 조인 키/값 컬럼은 명시적으로 지정합니다.
- **재현성**: 동일 입력 → 동일 출력, 침묵 없는 오류 처리.

## 튜토리얼

- 예제 워크플로우는 `tutorial.ipynb` 를 참고합니다.
