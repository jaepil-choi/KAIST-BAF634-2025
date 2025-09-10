# 과제: JKP 특성 데이터를 이용한 FF5 + Momentum + STR 팩터 복제 (USA, KOR)

## 1) 과제 개요

- **목표**: 제공된 특성(characteristics) 데이터를 사용하여 다음 7개 팩터의 월별 수익률을 복제합니다.
  - **Size (SMB)**: Small minus Big
  - **Value (HML)**: High minus Low (예: `be_me` 활용)
  - **Profitability (RMW)**: Robust minus Weak
  - **Investment (CMA)**: Conservative minus Aggressive
  - **Market (Mkt, Rm−Rf)**: 시장수익 − 무위험수익
  - **Momentum (MOM)**: 모멘텀
  - **Short-Term Reversal (STR)**: 단기 반전
- **대상**: **USA**, **KOR** 두 개 국가에 대해 동일한 절차로 팩터를 구성합니다.

## 2) 데이터 출처 및 맥락

- 본 과제의 원자료는 **JKP 글로벌 팩터 데이터셋**(jkpfactors.com)에 기반합니다.
- 데이터는 “Is There a Replication Crisis in Finance?” (Jensen, Kelly, Pedersen, Journal of Finance, 2023)을 사용합니다.

## 3) 구현 요구사항 (방법론 요약)

- **핵심 아이디어**: **Fama–French 이중 정렬(double sorting)** 방법론에 따라 **교차 정렬**을 수행하여 롱–숏 팩터 수익률을 산출합니다.
- **특성 데이터**(예: `be_me`)는 이미 제공되어 있으므로, **올바른 정렬 절차**와 **교차 포트폴리오 구성**으로 팩터 수익률을 계산합니다.
- **시장팩터(Mkt, Rm−Rf)** 는 시장수익에서 무위험수익을 차감하여 계산합니다.

## 4) 검증(Validation)과 피드백

- 본 과제에는 비교를 위한 **정답 팩터**(reference factors)가 제공되며, 제출한 결과와 자동으로 비교됩니다.
- 비교 지표(validator 참조: `qdl/validator.py`):
  - **MSE**, **RMSE**, **MAE**, **Pearson 상관계수(corr)**, **정보계수(IC)**
  - **비교 플롯**: 누적수익(cumsum) 기반의 **user vs reference** 시각화 제공
- **목표**: 참조 수익률에 **최대한 근접**한 팩터 수익률을 재현합니다.
