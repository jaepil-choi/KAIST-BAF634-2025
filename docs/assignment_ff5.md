# 과제: JKP 특성 데이터를 이용한 FF5 + Momentum + STR 팩터 복제 (USA, KOR)

## 1) 과제 개요

- **목표**: 제공된 특성(characteristics) 데이터를 사용하여 Size, Value, Profitability, Investment, Market, Momentum, Short-Term Reversal 요인의 월별 수익률을 복제합니다.
- **대상**: **USA**, **KOR** 두 개 국가에 대해 동일한 절차로 팩터를 구성합니다.

## 2) 데이터 출처 및 맥락

- 본 과제의 원자료는 **JKP 글로벌 팩터 데이터셋**(jkpfactors.com)에 기반합니다.
- 데이터는 “Is There a Replication Crisis in Finance?” (Jensen, Kelly, Pedersen, Journal of Finance, 2023)을 사용합니다.

## 3) 구현 요구사항

- 데이터 스펙 문서의 "2. Factor Portfolio Construction" 절을 그대로 따릅니다.
  - 모든 팩터를 `ew`, `vw`, `vw_cap` 가중치 각각에 대해 만듭니다.
  - 힌트:
    - NYSE 20th percentile은 `size_grp`로 구분할 수 있습니다.
- size (SMB, small minus big)
  - `market_equity`
- value (HML, high minus low)
  - `be_me`
- profitability (RMW, robust minus weak)
  - `ope_be`
- investment (CMA, conservative minus aggressive)
  - `at_gr1`
- market (Rm-Rf)
  - 적절한 `[usa]_[mkt]_[monthly]_..` 를 사용합니다
- momentum (MOM)
  - `ret_12_1`
- short-term reversal (STR)
  - `ret_1_0`

## 4) 검증(Validation)과 피드백

- 본 과제에는 비교를 위한 **정답 팩터**(reference factors)가 제공되며, 제출한 결과와 자동으로 비교됩니다.
- 비교 지표(validator 참조: `qdl/validator.py`):
  - **MSE**, **RMSE**, **MAE**, **Pearson 상관계수(corr)**, **정보계수(IC)**
  - **비교 플롯**: 누적수익(cumsum) 기반의 **user vs reference** 시각화 제공
- **목표**: 참조 수익률에 **최대한 근접**한 팩터 수익률을 재현합니다.
