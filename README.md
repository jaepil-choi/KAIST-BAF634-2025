# QDL (Quant Data Loader)

간단한 인터페이스로 로컬 `data/` 폴더의 정량 데이터(요인·특성·메타·수익률)를 로드하고, 사용자가 만든 요인 수익률을 기준 데이터와 비교·검증할 수 있도록 돕는 모듈입니다. 내부 구현(로더·변환·검증)은 숨기고, 외부에서는 일관된 공개 API만 사용합니다.


## 빠른 시작

간단한 공개 API로 데이터를 로드하고(검증은 추후 제공), DataFrame을 바로 다룰 수 있습니다.

```python
from qdl.facade import QDL

q = QDL()
# 요인 데이터 로드(미국/시장/월별/시가총액가중)
factors = q.load_factors(country="usa", dataset="mkt", weighting="vw")
print(factors.head())

# 특성 데이터 로드(JKP 빈티지 2020-, 미국)
chars = q.load_chars(country="usa", vintage="2020-")
print(chars.head())
```

> 주의: 이 공개 API는 컬럼명/스키마를 임의로 추측하지 않습니다. 검증(`validate_factor`)은 스키마 키/명시적 컬럼 지정과 함께 제공될 예정입니다.

## 요인(factors) 옵션

| 파라미터 | 허용 값 | 기본값 | 설명 |
|---|---|---|---|
| country | `"usa"`, `"kor"` | (필수) | 국가/지역 선택 |
| dataset | `"factor"`, `"theme"`, `"mkt"` | (필수) | 요인 집합, 테마 집합, 시장(시장포트폴리오) |
| weighting | `"ew"`, `"vw"`, `"vw_cap"` | (필수) | 동일가중, 시가총액가중, 시가총액기준 가중 |
| frequency | `"monthly"` | `"monthly"` | 현재 월별만 지원 |
| encoding | 예: `"utf-8"` | `"utf-8"` | 파일 인코딩 |

예시 호출:

```python
q.load_factors(country="kor", dataset="factor", weighting="ew")
q.load_factors(country="usa", dataset="theme", weighting="vw_cap")
q.load_factors(country="usa", dataset="mkt", weighting="vw")
```

## 공개 API

- `QDL.load_factors(*, country, dataset, weighting, frequency="monthly", encoding="utf-8") -> pd.DataFrame`
- `QDL.load_chars(*, country, vintage, columns=None, engine="pyarrow") -> pd.DataFrame`
- `QDL.validate_factor(user_df, reference_df=None, *, on, value_col, reference_load_params=None, **kwargs) -> ValidationReport`

## 원칙

- **단일 공개 API 우선**: 외부 사용자는 공개 API만 사용합니다. 내부 모듈(로더·변환·검증)은 문서화하지 않습니다.
- **명시성**: 스키마/키는 명시적으로 지정하거나 설정으로 해석합니다. 임의 추측을 하지 않습니다.
- **재현성**: 동일 입력은 동일 출력. 침묵 없는 오류 처리.

## 튜토리얼

- 사용 예시는 `tutorial.ipynb`를 참고하세요. 공개 API로 로드하는 예시가 포함되어 있습니다.
