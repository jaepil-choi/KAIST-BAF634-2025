# KAIST 고급금융계량분석 · 과제1 (QDL)

본 저장소는 KAIST `고급금융계량분석` 과목의 과제1(FF5 + Momentum + STR 팩터 복제)을 위한 코드와 사용 예시를 제공합니다. 과제 요구사항은 `docs/assignment_ff5.md`를 참고하십시오. 본 저장소는 퍼사드(`qdl.facade.QDL`)를 통해 일관된 데이터 접근과 검증 인터페이스를 제공합니다.

## 시작하기

- 저장소를 클론하거나 ZIP으로 다운로드하여 로컬에 풀어주세요.
  - Git: `git clone <본 저장소 URL>`
  - 또는 GitHub에서 ZIP 다운로드 후 압축 해제
- 데이터는 Google Drive로 제공됩니다. 제공된 `data/` 디렉터리 구조에 맞게 파일을 배치하세요.
  - 요인 데이터(CSV): `data/factors/`
  - 특성 데이터(Parquet): `data/chars/`
- 데이터 스펙은 데이터 스펙서를 참고하세요.

## 데이터 스펙(요약)

- 요인 데이터(factors, CSV)
  - 파일명 규칙: `[<country>]_[<dataset_token>]_[monthly]_[<weighting>].csv`
    - `<country>` ∈ {usa, kor}
    - `<dataset_token>` ∈ {all_factors, all_themes, mkt}
    - `<weighting>` ∈ {ew, vw, vw_cap}
  - 스키마 가정 없음(롱 포맷 원본). 와이드 변환은 퍼사드에서 지원.
- 특성 데이터(chars, Parquet)
  - JKP 파일명: `jkp_<vintage>_<country>.parquet`
    - `<vintage>` ∈ {1972-, 2000-, 2020-}
      - RAM/용량이 부족할 시 큰 데이터를 로드하기 어려울 수 있습니다. 이 경우 더 작은 데이터를 로드해 주세요.
      - 팩터 검증시 더 작은 쪽으로 자동으로 맞춰집니다. 
    - `<country>` ∈ {usa, kor}
  - 스키마 가정 없음. 단일 특성 와이드 변환은 퍼사드에서 지원.

## Quick Start: 특성 데이터(Chars) 로드만(와이드)

아래는 퍼사드만 사용하여 단일 특성 컬럼을 날짜×`id` 와이드 포맷으로 불러오는 최소 예시입니다.

```python
from qdl.facade import QDL

q = QDL()
wide_char_me = q.load_char(
    country="usa",
    vintage="2020-",
    char="me",
)
print(wide_char_me.head())
```

자세한 사용법(요인 데이터 로드/검증 포함)은 `tutorial.ipynb`를 참고하세요.

---

## 참고 자료

- 과제 명세: `docs/assignment_ff5.md`
- 데이터 스펙: 데이터 스펙서를 참고하세요.
- 튜토리얼: `tutorial.ipynb` (퍼사드만 사용, 와이드 검증 예시 포함)

## 원칙

- 퍼사드 우선: 공개 API인 `QDL`만으로 데이터 접근
- 명시적 정렬: 검증 전 인덱스/컬럼 교집합 정렬
- 재현성: 동일 입력 → 동일 출력, 명확한 오류 메시지
