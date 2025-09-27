# %% [markdown]
# # Factor construction demo

# %%
# 시작하기: 퍼사드 임포트
from qdl.facade import QDL
import pandas as pd
import numpy as np


# %% [markdown]
# ## 과제 목표
# 
# - 국가별로 (usa/kor) --> 할 것 없음
# - Size, Value, Profitability, Investment, Market, Momentum, Short-Term Reversal 팩터들을
# - ew/vw/vw_cap 각각으로 가중치 방법을 다르게 하여 
# - 최대한 JKP 팩터 수익률과 비슷한 팩터(수익률)을 만드는 것
# 
# ## 과제 방법
# 
# - `qdl`을 통해 특성/팩터 데이터셋을 로드하여
# - data spec 의 섹션 2: Factor Portfolio Construction 방법론에 따라 구현
#     - 주의: Fama French의 double independent sort 방법 쓰지 않음
# 

# %% [markdown]
# ## 데이터 로드

# %%
q = QDL()

# %%
# 특성(Chars) 데이터셋 (와이드): 초과수익률 
wide_ret_exc = q.load_char(
    country="usa",
    vintage="2020-",
    char="ret_exc",
    date_col="date",
)


# %%
print(wide_ret_exc.head(10))

# %% [markdown]
# ## 전처리

# %% [markdown]
# ### `eom`
# 

# %% [markdown]
# Q: 날짜는 왜 이렇게 불규칙적인가요? 
# 
# A: 그냥 데이터가 그렇습니다.. 월말 기준이어야 하지만 그 때 데이터가 available하지 않은 경우들이 있는 듯 합니다. (추측: 분할/합병을 위한 일시적 거래 정지 등)
# 
# ** data spec 시트의 date 컬럼 설명: 
# 
# > Date of the last return observation during the month.

# %%
long_chars = q.load_char_dataset( # 특성 데이터셋 원본 로드
    country="usa",
    vintage="2020-",
)

# %%
d = '2020-01-06'
a = wide_ret_exc.dropna(how='all', axis=0).copy()

print(a.loc[d, :].dropna())

# %%
a_id = a.loc[d, :].dropna().index[0]
a_id

# %%
print(long_chars[long_chars['id'] == a_id][['id', 'date', 'ret_exc', 'at_gr1']])

# %% [markdown]
# 
# 기존에는 `date` 컬럼을 기본으로 사용
# 
# `eom`을 default로 하여 `date_col=`을 고를 수 있도록 고쳤습니다. 

# %%
# 특성(Chars) 데이터셋 (와이드): 초과수익률 
wide_ret_exc = q.load_char(
    country="usa",
    vintage="2020-",
    char="ret_exc",
    # date_col="date",
)


# %%
print(wide_ret_exc.head(10))

# %% [markdown]
# ### `size_grp` 불러오기

# %%
# 특성(Chars) 데이터셋 (와이드): size_grp
wide_size_grp = q.load_char(
    country="usa",
    vintage="2020-",
    char="size_grp",
)


# %%
print(wide_size_grp.head(10))

# %%
long_chars['size_grp'].unique()

# %% [markdown]
# > In each country and month, we sort stocks into characteristic terciles (top/middle/bottom third) with breakpoints based on non-micro stocks in that country. Specifically, we start with all non-micro stocks in a country (i.e., larger than NYSE 20th percentile) and sort them into three groups of equal numbers of stocks based on the characteristic, say book-to-market. Then we distribute the micro-cap stocks into the three groups based on the same characteristic breakpoints. This process ensures that the non-micro stocks are distributed equally among across portfolios, creating more tradable portfolios.

# %% [markdown]
# ## 팩터 포트폴리오 만들기
# 
# - investment (CMA, conservative minus aggressive)
#   - `at_gr1`

# %%
# 특성(Chars) 데이터셋 (와이드): 단일 특성 예시 'at_gr1' (Investment 팩터용)
wide_atgr1 = q.load_char(
    country="usa",
    vintage="2020-",
    char="at_gr1",
)


# %%
wide_atgr1_xs_rank = wide_atgr1.rank(axis=1, method='min', pct=True)
print(wide_atgr1_xs_rank.head(5))

# %%
wide_atgr1_xs_high_mask = wide_atgr1_xs_rank >= 0.666
wide_atgr1_xs_low_mask = wide_atgr1_xs_rank <= 0.333

# %%
print(wide_atgr1_xs_high_mask.head(5))

# %%
# shift(1) 하는 이유: forward looking 하지 않기 위해. 
short_port_ew = -1 * wide_ret_exc[wide_atgr1_xs_high_mask.shift(1)] # aggressive
long_port_ew = wide_ret_exc[wide_atgr1_xs_low_mask.shift(1)] # conservative


# %%
long_port_returns = long_port_ew.mean(axis=1)
short_port_returns = short_port_ew.mean(axis=1)

# %%
investment_factor_returns = long_port_returns + short_port_returns

# %%
investment_factor_returns.cumsum().plot()

# %% [markdown]
# ## 결과 비교

# %% [markdown]
# ### 팩터 불러오기

# %%
investment_factor_answer =q.load_factors(
    country="usa",
    dataset='factor',
    weighting='ew',
    factors=["at_gr1"],
)

investment_factor_answer.loc['2020-01-06':, :].cumsum().plot()

# %%
my_factor = pd.DataFrame(investment_factor_returns)
my_factor.columns = ['at_gr1']

# %%
report = q.validate_factor(
    user=my_factor,
    weighting="ew",
    return_plot=True,
    plot_title="Investment Factor: user vs reference",
)


# %%
print("\n검증 리포트:")
print("관측치수:", report.n_obs, "시작일:", report.date_start, "종료일:", report.date_end)

# %%
def _fmt(x):
    return f"{x:.3f}" if x is not None else "nan"

print(
    "mse:", _fmt(report.mse),
    "rmse:", _fmt(report.rmse),
    "mae:", _fmt(report.mae),
    "corr:", _fmt(report.corr),
)


# %%



