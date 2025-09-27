# %% [markdown]
# # QDL 튜토리얼
# 
# 이 노트북은 KAIST `고급금융계량분석` 과제(FF5 + Momentum + STR 팩터 복제)를 위한 사용 예시를 제공합니다. 과제 요구사항은 `docs/assignment_ff5.md` 를 참고하십시오. 여기서는 공개 메서드만 사용하며, 내부 구현 세부는 다루지 않습니다.
# 
# 

# %%
# 시작하기: 퍼사드 임포트
from qdl.facade import QDL
import numpy as np


# %% [markdown]
# ## 1. 데이터 로드

# %% [markdown]
# ### 1.1 팩터 데이터

# %%
# 1) 데이터 로드 (와이드)
q = QDL()

# 팩터 데이터셋 (와이드, 과제 백틱 변수 사용, mkt 제외)
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
print("팩터(와이드) 상위 5행:\n", wide2.head(5))


# %% [markdown]
# ### 1.2 특성 데이터

# %%
# 특성(Chars) 데이터셋 (와이드): 단일 특성 예시 'me'
wide_char_me = q.load_char(
    country="usa",
    vintage="2020-",
    char="me",
)
print("특성 'me'(와이드) 상위 5행:\n", wide_char_me.head(5))


# %% [markdown]
# ## 2. 팩터 검증

# %%
# 2) 검증 준비: 노이즈 추가 및 교집합 정렬
rng = np.random.default_rng(42)
noise = rng.normal(loc=0.0, scale=0.02, size=wide2.shape)
noise = np.clip(noise, -0.1, 0.1)
noisy_wide2 = wide2.add(noise, fill_value=0.0)

user_wide = noisy_wide2.iloc[12:].copy()
ref_wide = wide2.iloc[:-6].copy()

common_idx = user_wide.index.intersection(ref_wide.index)
common_cols = user_wide.columns.intersection(ref_wide.columns)
user_aligned = user_wide.loc[common_idx, common_cols]
ref_aligned = ref_wide.loc[common_idx, common_cols]

print("검증 기간:", common_idx.min(), "~", common_idx.max())
print("정렬된 길이:", len(common_idx))
print("열 집합 동일 여부:", set(user_aligned.columns) == set(ref_aligned.columns))


# %%
# 3) 팩터 검증(와이드, 퍼사드의 간편 인터페이스 사용; 팩터별 cumsum 플롯 포함)
report = q.validate_factor(
    user=user_aligned,
    weighting="vw",
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

if report.per_factor_metrics:
    print("\n팩터별 지표:")
    for factor, metrics in report.per_factor_metrics.items():
        n = (report.per_factor_n_obs or {}).get(factor)
        print(
            f"{factor}: 관측치수={n}, mse={_fmt(metrics.get('mse'))}, rmse={_fmt(metrics.get('rmse'))}, "
            f"mae={_fmt(metrics.get('mae'))}, corr={_fmt(metrics.get('corr'))}, ic={_fmt(metrics.get('ic'))}"
        )

try:
    import matplotlib.pyplot as plt
    if report.figure is not None:
        plt.show(report.figure)
except Exception:
    pass



