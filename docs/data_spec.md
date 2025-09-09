# Global Factor Data Documentation

# Theis Ingerslev Jensen
Bryan Kelly
Lasse Heje Pedersen*

* Jensen is at Yale School of Management; https:/ /sites ・ google.com/view/theis-ingerslev
-jensen/ Kelly is at AQR Capital Management, Yale School of Management, and NBER; www
bryankellyacademic. org. Pedersen is at AQR Capital Management, Copenhagen Business School, and
CEPR; www - lhpedersen ・ com. We are grateful to Faheem Almas and Tyler Gwinn for excellent research
assistance. AQR Capital Management is a global investment management firm, which may or may not
apply similar investment techniques or methods of analysis as described herein. The views expressed here
are those of the authors and not necessarily those of AQR.

# Table of Contents

1 Overview 2
1.1 How To Run the Code 2
1.2 How To Use the Data · 3
1.3 Versions, Bug Fixes, and Comments 3
1.4 Terminology . 6
2 Factor Portfolio Construction 7
3 Identifier Variables 7
4 Industry Identification 8
4.1 Datasets 9
5 Helper Functions 9
6 Accounting Characteristics 10
6.1 Datasets 10
6.2 General Information 10
6.3 Annualized Accounting Variables from Quarterly Data 10
6.4 Accounting Variables 11
7 Market Based Characteristics 25
8 Detailed Characteristic Construction 30
9 FX Conversion Rate Construction 36
10 Factor Details and Citations 37
11 Miscellaneous 48
References 50

1

# 1 Overview

● This documentation describes the Global Factor Data, and the associated code for
constructing the data, based on Jensen, Kelly, and Pedersen (2022). The citation for
use of this data and code is:

# @article{JensenKellyPedersen2022,

author = {Jensen, Theis Ingerslev and Kelly, Bryan T and Pedersen, Lasse Heje},
journal = {Journal of Finance, Forthcoming},
title = {Is There A Replication Crisis In Finance?},
year = {2022}

}

- ● The Global Factor Data includes 406 characteristics and their associated factor port-
- folios. This is a superset of the 153 factors analyzed in Jensen, Kelly, and Pedersen
- (2021).


- ● This documentation is grouped into eight main sections: Identifier Variables, Industry
- Identifiers, Helper Functions, Accounting Characteristics, Market Based Character-
- istics, Detailed Characteristic Construction, FX Conversion Rate Construction and
- Factor Details and Citations.


- - Identifier Variables include firm identifying information, date, etc...
- - Each of the Characteristics sections includes at least three subsections: Datasets,
- Variables, and Characteristics.
- - Datasets refers to which datasets the items in variables are drawn from. For
- example, 'COMP.FUNDA' suggests we use variables from the FUNDA dataset
- provided by Compustat.
- - Variables refers to a table containing information about the variables drawn from
- the datasets previously identified. These tables include the name, abbreviation
- used throughout the section, and the construction of the variables. These variables
- are constructed in a way to maximize coverage and are not directly included in
- the final dataset.
- Characteristics refers to a table of constructed characteristics made of the previ-
- ously describes variables. These tables include the name, the abbreviation used
- in the published dataset, and the construction. These characteristics are in the
- final dataset.


1.1 How To Run the Code

- ● Access the code for this data set at https: / /github .com/bkelly-lab/ReplicationCrisis.


- ● This data is produced using the SAS Studio on Wharton Research Data Services
- (WRDS) servers. The github README file contains instruction on how to gener-
- ate the data.


2

● Use the 'EOM' (end of month) variable as the date variable to join / merge datasets.

# 1.2 How To Use the Data

- ● The id column is the unique security x source1 identifier.


- ● The eom column shows the end of month, where the data is valid. In other words,
- it shows the information available by the end of a given month. As an example, the
- me value for a stocks with eom=20191231, will be the last available market equity
- before or at December 31st 2019. Therefore, when predicting the return column ret,
- characteristics should be lagged by one month (as ret shows the return in the current
- month identified by eom). Alternatively, you can predict next month's returns, stored
- in ret_exc_lead1m, without lagging the characteristics.


- ● The excntry column, identifies the country of the exchange where the security is
- traded.


- ● Suggested screens:


- - To restrict the sample to one observation per security x month, use obs _main=1.
- - To restrict the sample to common stocks, use common=1.
- - To restrict the sample to prominent exchanges, use exch main=1.
- - To restrict the sample to primary listing x month, use primary _sec=1.


1.3 Versions, Bug Fixes, and Comments

- ● We will update the code and data regularly as CRSP and Compustat updates become
- available. We will also release periodic updates with bug fixes. Our GitHub repository:
- https : //github . com /bkelly-lab/ReplicationCrisis/blob/master  GlobalFactors/
- CHANGELOG . md tracks the evolution in the code used to generate the data. Furthermore,
- Table 1 gives an overview of the most important changes.


- ● The code and data has been carefully vetted, but may contain bugs and certainly has
- room for improvement. We welcome any and all feedback regarding bugs or suggestions
- for improvements and extensions.


- ● Send correspondence to bryan.kelly@yale.edu with subject "Global Factor Data"


1CRSP or Compustat.

3

Table 1: Log of Important Code and Methodology

| Date | Changes |
| --- | --- |
| 03-03-2023 | ● Added 'me' (market equity) and 'ret' (total return) and removed 'source_crsp' from daily return files. |
| 02-08-2022 | ● Fixed error in the construction of intrinsic_value. Previously, we failed to scale intrinsic_value by market equity as done in Frankel and Lee (1998). We call the new characteristic ival me and keep intrinsic_value in the data set. The alpha of the new factor based on ival. me is signif- icantly different from zero, while the factor based on intrinsic_value is insignificant. |
| 11-16-2021 | ● Changed return cutoffs to depend on all stocks, instead of only stocks from CRSP. ● Changed the 'source' (character) column to 'source_crsp' (integer), source_crsp is 1 if CRSP is the return data source. ● Changed the 'id' column from character to integer. For stocks from CRSP, the id is just their permno. For stocks from Compustat, the first digit is 1 if the stock is traded on a US exchange, 2 if it's traded on a Canadian exchange, and 3 otherwise. The next two digits are the IID from Compustat, and the remaining six digits are the gvkey. ● Adapted the primary _sec column such that all observations from CRSP have primary _sec=1. ● Changed the treatment of zero return. Previously, we treated a zero return as a missing observation. Now, we have removed this screen, such that a zero return is treated like any other return. ● Changed the creation of characteristics based on daily stock market data. Previously, we winsorized daily returns, market equity, and dol- lar volume, before creating characteristics based on daily stock market data. Now, we have removed this winsorization, and daily characteris- tics are based on the raw data. ● Added the option to create daily factor return in the portfolios.R code. ● Added the option to create industry returns in the portfolios.R code. |
| 08-27-2021 | · Fixed a bug regarding how daily delisting returns from CRSP are in- corporated. ● Added indfmt='FS' to the international accounting data. |


4

| Date | Changes |
| --- | --- |
| 06-14-2021 | ● We changed the winsorization scheme. First, we removed the 0.01 %/99.9% winsorization of market equity in all countries. Second, we removed the winsorization of returns from the CRSP database. For Compustat returns, we set returns above (below) the 99.9% (0.01%) of CRSP returns in the same month, to that level. In other words, we base our winsorization of Compustat data on CRSP data from the same month. |
| 02-19-2021 | ● Previously we did not exclude securities that are only traded over the counter. In the new version of the data set, we include an indicator column " exch main" to exclude non-standard exchanges. In the US, the main exchanges are AMEX, NASDAQ, and NYSE. Outside of the US, we exclude over the counter exchanges, stock connect exchanges in China, and cross-country exchanges such as BATS Chi-X Europe. The documentation includes a full list of the excluded exchanges. ● Included SIC, NAICS, and GICS industry codes. |
| 02-15-2021 | ● Removed a bug that caused ivol. ff3_21d, iskew _ff3_21d, ivol_hxz4_21d, and iskew _hxz4_21d to require 17 (ff3) and 18 (hxz) observations for a valid estimate. Consistent with our original intent, we now require at least 15 observations for a valid estimate. |
| 02-01-2021 | ● Fixed a small bug in the bidask hl() macro. ● Lowered the requirement for the number of stocks needed when cre- ating asset pricing factors (FF and HXZ). We previously required at least 5 stocks in a sub-portfolio (e.g., small stocks with high BM) for the observation to be valid. This led to missing observations in the 1950s for small stocks with low BM. We lowered this requirement to 3 stocks. Furthermore, when creating asset pricing factors, we changed the breakpoints to be based on NYSE stocks in the US instead of non- microcap stocks. Outside of the US, breakpoints are still based on non-microcap stocks. |


5

| Date | Changes |
| --- | --- |
| 01-25-2021 | ● Changed residual momentum characteristics (resff3_12_1 & resff3_6_1) to be scaled with the standard deviation of residuals consistent with Blitz, Huij, and Mertens (2011). ● Fixed error in creating qmj_prof. The issue was that the oaccruals_at used the value instead of the z-score of ranks. This effectively meant that accruals didn't impact the profitability score. ● Fixed error for annual seasonality characteristics (factor names starting with seas_ and ending with _an). There was a bug in the screening procedure which meant that the characteristic for one stock could use information from an unrelated stock. ● Rounding issues when converting a .CSV file to an excel file, caused the zero_trades_* variables to not have any decimals which made the turnover tie-breaker ineffective. ● Standardized unexpected earnings (niq_su) and sales (saleq_su) is com- puted as the actual value minus the expected value (standardized by the standard deviation of this change). Before, the expected value was computed as the mean yearly change over the last 8 quarters added to the last quarterly value. Now the expected value is the same mean yearly change, but added to the quarterly value 4 quarters ago consis- tent with Jegadeesh and Livnat (2006). |
| Name | Description |
| size_grp | This groups each firm into one of five categories: Mega, large, small, micro and nano cap. The groups are non-overlapping and the breakpoints are based on the market equity of NYSE stocks by the end of each month. In particular, Mega caps are stocks with a market cap above the 80th percentile of NYSE stocks, large caps are all remaining stocks above the 50th percentile, small caps are above the 20th percentile, micro caps above the 1st percentile and nano caps are the remaining stocks. |


# 1.4 Terminology

- ● Annual data refers to accounting data from annual reports sourced from COMP.FUNDA
- and COMP. G_FUNDA.
- ● Quarterly data refers to accounting data from quarterly reports sourced from COMP.FUNDQ
- and COMP. G FUNDQ.
- ● Final Dataset refers to "world_data.sas 7bdat", the output dataset
- ● Fiscal period refers to the relevant period over which income and expenses have accrued.
- ● Accounting variables refers to accounting items such as assets, sales and net income.
- ● Market variables refers to market based items such as market equity and excess return.
- ● Characteristics refers to columns in the final dataset that reveals a characteristic about
- the security, For example asset growth, book to market equity, and net income to book
- equity.


6

# 2 Factor Portfolio Construction

- ● For each characteristic, we build the 1-month holding period factor return within each
- country as follows.


- ● In each country and month, we sort stocks into characteristic terciles (top/ middle /bot-
- tom third) with breakpoints based on non-micro stocks in that country. Specifically, we
- start with all non-micro stocks in a country (i.e., larger than NYSE 20th percentile) and
- sort them into three groups of equal numbers of stocks based on the characteristic, say
- book-to-market. Then we distribute the micro-cap stocks into the three groups based
- on the same characteristic breakpoints. This process ensures that the non-micro stocks
- are distributed equally among across portfolios, creating more tradable portfolios.


- ● For each tercile, we compute its "capped value weight" return, meaning that we weight
- stocks by their market equity, winsorized at the NYSE 80th percentile. This construc-
- tion ensures that tiny stocks have tiny weights and any one mega stock does not
- dominate a portfolio, seeking to create tradable, yet balanced, portfolios.


- ● The factor is then defined as the high-tercile return minus the low-tercile return, corre-
- sponding to the excess return of a long-short zero-net-investment strategy. The factor
- is long (short) the tercile identified by the original paper to have the highest (lowest)
- expected return.


- ● For a factor return to be non-missing, we require that it has at least 5 stocks in each of
- the long and short legs. We also require a minimum of 60 valid monthly observations
- for each country-specific factor for inclusion in our sample.


- ● We update characteristics with the most recent accounting data (which could be either
- annual or quarterly) starting four months after the end of the fiscal period.


- ● To compute a cluster (theme) return, we first sign factors according to the original
- reference, then we equal-weight the returns of factors within a specific cluster. The
- signing convention and cluster allocation follows Jensen et al. (2022) and we show it
- in table 9.


# 3 Identifier Variables

This section covers all of the variables that give firm / date level identifiers and information.
If a variable starts with 'comp' or 'crsp', then the following variable name is drawn from the
specified dataset. For example, 'crsp_shrcd' is the 'shrcd' variable from CRSP.

Table 2: Identifier Variables

7

| N ame | Description |
| --- | --- |
| id | We generate a unique number for each security in our data set. For securities from CRSP, the id is just the corresponding permno. For stocks from Compustat, the first digits is 1 if the stocks is traded on a US exchange, 2 if it's traded on a Canadian exchange, and 3 otherwise. The next six digits are the gvkey and the last two are the iid.2 |
| source_crsp | Identifies the source of the return data. A 1 (0), indicates that the source is CRSP (Compustat). For US stocks, we often have two observations for each security-month pair. One from Compustat, and one |
| obs_main | from CRSP. In cases with duplicates, the observation from CRSP has obs_main=1, and the observation from Compustat has obs_main=0. If there are more than one firm observations for one date, this identifies if the observation is considered as the 'main' observation. If available, CRSP observations are considered as the 'main' observation. |
| exch_main | Indicator for ordinary exchanges. If CRSP is the source, main exchanges are those with crsp_exchcd 1, 2 and 3. If Compustat is the source, main exchanges are all comp_exchg except 0, 1, 2, 3, 4, 13, 15, 16, 17, 18, 19, 20, 21, 127, 150, 157, 229, 263, 269, 281, 283, 290, 320, 326, 341, 342, 347, 348, 349, 352. |
| gvkey | Permanent six-digit unique firm identifier from Compustat |
| iid | Permanent two-digit addition to 'gvkey' that identifies specific security of a firm from Compustat |
| primary _sec | Primary security as identified by Compustat. A 'gvkey' can have up to three different primary securities ('iid)' at a given time (US, CA, and international). All observations from CRSP has primary _sec=1. |
| permco | Permanent unique firm identifier from CRSP |
| permno | Permanent security identifier from CRSP ISO currency |
| excntry | The country of the exchange where the security is traded. Usually expressed as an code with the exception of mul which indicates a multi country exchange⌀ |
| curcd | Currency of prc_local and the currency used to calculated ret_local. |
| fx | Ratio of curcd to USD at the date of observation the SHRCD variable is 10, 11 or 12. |
| common | Indicator for common stocks. If CRSP is the source, common is one if If Compustat is the source, common is one if TPCI is '0' |
| comp_tpci | Compustat issue type identifier |
| crsp _shrcd | CRSP share code |
| comp_exchg | Compustat stock exchange code |
| crsp_exchd | CRSP stock exchange code |
| date | Date of the last return observation during the month. |
| eom | The last day of the month in which the observation is made |
| adjfct | Share adjustment factor, using 'cfacshr' if the source is CRSP or 'ajexdi' if the source is Compustat |
| Name | Description |
| sic naics gics ff49 | Firm SIC industry. We use Compustat data if available and otherwise use CRSP data. Firm NAICS industry. We use Compustat data if available and otherwise use CRSP data. Firm GICS industry. We use historical data from Compustat. Classification of stocks into 49 industry groups based SIC codes and the methodology in Fama and French (1997) with the addition of a software industry. |


# 4 Industry Identification

This section describes the industry identifiers. First we contruct separate identifiers for
CRSP and Compustat. Based on these datasets, we create one SIC, NAICS and GICS code
for each firm based on Compustat data if available and otherwise CRSP. GVKEY is the
company identifier for COMPUSTAT. PERMNO is the security identifier for CRSP. While
we would prefer to use PERMCO, which is company level, different firms with different in-
dustry identifications can be listed under the same PERMCO. CRSP identifiers are available
on a daily basis. For Compustat, we extract SIC and NAICS codes from annual accounting
reports. Historical GICS codes are only available in Compustat. The Fama-French industry
identifier is mapped from SIC codes using documentation provided by Ken French. We allow
for using either 38 or 49 industry portfolio definitions, as defined here and here, respectively.
By default, we use the 49 portfolio definition, but that can be adjusted in 'main.sas'.

2In Compustat, a security is identified by gvkey and iid. To map our id to Compustat, add 'C' or 'W' to
the iid if the first digit is 2 or 3 respectively.
the counter

3Typically over

exchanges.

8

# 4.1 Datasets

- ● CRSP.DSEN AMES
- ● COMP.FUNDA
- ● COMP.G_FUNDA
- ● COMP.CO_HGIC
- ● COMP.G_CO_HGIC


Table 3: Identifier Variables

# 5 Helper Functions

This section describes functions that we use to create variables. Many of the functions are
used for variables with quarterly, monthly and daily frequencies, and these are specified
by " zQ", " _zM" and "_zD" respectively, where 66⌀xD is the number of quarters, months or
days that the function is referencing. For example, COVAR_12M(X, Y) is the covariance of
variables X and Y over the past 12 months.

Table 4: Helper Functions

| Function | Name | Description |
| --- | --- | --- |
| Mean Variance Covariance Standard Deviation Skewness Standardized Unexpected Realization Change to Expectations Maximum | Xz VARC_z(X) COVAR_z(X, Y) �z(X) SKEW _z(X) SUR_z(X) CHG_TO_EXP(X) MAXn_z(X) | 1 En=1 Xt-n z 1 �n=0(Xt-n-Xtz)2 z-1 1 �급(Xt-n-Xtz)(Yt-n - Ytz) z-1 VVARC_z(X) 1 En=1(Xt-n - Xtz)3 zx�z(X)3 Xt-(Xt-3+(Xt-3-Xt-15)z/4) �z(Xt-3-Xt-15) Xt (Xt-12+Xt-24)/2 The maximum n values of given input. |
| Quality Minus Junk Helpers | Quality Minus Junk Helpers | Quality Minus Junk Helpers |
| Earnings Volatility | _EVOL | RO EQ_BE_STD x 2. If this is unavailable, we use RO E_BE_STD. |


9

| Function | Name | Description |
| --- | --- | --- |
| Rank of Variable z transformation | _rV ar ZV(rVar) | Cross-sectional rank of Var within a country⌀ _rVAR-_rVARz _t(_rVAR) |


# 6 Accounting Characteristics

# 6.1 Datasets

- ● COMP.FUNDA
- ● COMP.FUNDQ
- ● COMP.G_FUNDA
- ● COMP.G_FUNDQ


# 6.2 General Information

- ● We create characteristics for annual and quarterly accounting data separately. We then
- take the most recent characteristics value from each dataset to create the final dataset.


- ● We assume that accounting variables are publically available 4 months after the end
- of the accounting period.


- ● In describing accounting variables, we use the Compustat item names from the annual
- dataset. The equivalent item name in the quarterly dataset can be found by adding
- a 'q' or 'y' to the end of the annual item name. Specifically, 'q' indicates a value
- calculated over one quarter while 'y' refers to the cummulative value over the quarters
- with data available within a fiscal year.


6.3 Annualized Accounting Variables from Quarterly Data

- ● The value of a balance sheet item such as asset or book equity has the same meaning
- in the annual and the quarterly data. It is the value by the end of a fiscal period.


- ● The value of an income or cash flow statement item is different. In the annual data, it is
- calculated over one year. However, in the quarterly data, it is calculated over one quar-
- ter. To make quarterly income and cash flows items comparable to the corresponding
- annual item, we take the sum of the item over the last four quarters.


40ACCRU ALS_AT, BET AB AB_1260d, DEBT_AT and _EVOL are sorted in descending order. All
other variables are sorted in ascending order.

10

# 6.4 Accounting Variables

The abbreviation is used to refer to the accounting variable. A suffix of 1*) indicates that
we have altered the original Compustat item to increase the coverage or to create a variable
that is a part of creating a characteristic in the final dataset. The characteristic name will
reflect the accounting name except the 7*2 suffix. As an example, 'gp_at' is gross profit scaled
by assets. In general, we will refer to Compustat variables using capital letters.

Table 5: Accounting Variables

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Income Statement | Income Statement | Income Statement |
| Sales | sale* | We prefer SALE. If this is unavailable, we use REVT |
| Cost of Goods Sold | cogs | Compustat item COGS |
| Gross Profit | gp * | We prefer to use GP. If this is unavailable we use sale*-COGS |
| Selling, General and Administrative Expenses | xsga | Compustat item XSGA |
| Advertising Expenses | xad | Compustat item XAD. Note that this is not available in Com- pustat Global |
| Research and Development Expenses | xrd | Compustat item XRD. Note that this is not available in Com- pustat Global |
| Staff Expenses | xlr | Compustat item XLR |
| Special Items | spi | Compustat item SPI |
| Operating Expenses | opex* | We prefer to use XOPR. If this is unavailable, we use COGS+XSGA |
| Operating Income Before Depreciation | ebitda* | We prefer to use EBITDA. If this is unavailable, we use OIBDP. If this is unavailable, we use SALE*-OPEX*. If this is unavailable, we use GP*-XSGA |
| Depreciation and Amortization | dp | Compustat Item DP |
| Operating Income After Depreciation | ebit* | We prefer to use EBIT. If this is unavailable, we use OIADP. If this is unavailable, we use EBITDA*-DP |
| Interest Expenses | int | Compustat item XINT to |
| Operating Profit ala Ball et al (2015) | op * | We use EBITDA * + XRD. If XRD is unavailable, we set it zero |
| Operating Profit to Equity | ope* | We use EBITDA * XINT. Note that we target the same vari- able as the numerator of the profitability characteristic used to create the Robust-minus weak factor in the fama-French 5 factor model (Fama and French, 2015) |
| Earnings before Tax and Extraordi- nary Items | pi* | We prefer to use PI. If this is unavailable we use EBIT*- XINT+SPI+NOPI where we set SPI and NOPI to zero if missing |
| Income Tax | tax | Compustat item TXT We |
| Extraordinary Items and Discontinued Operations | xido* | prefer to use XIDO. If this is unavailable, we use XI+DO where we set DO to zero if missing. The reason why we set missing DO to zero is because it is not available in COMP.G_FUNDQ |
| Net Income | ni* | We prefer to use IB. If this is unavailable, we use NI-XIDO*. If this is unavailable, we prefer PI*-TXT-MII. If MII is un- availble, it is set to zero |
| Net Income Including Extraordinary Items | nix* | We prefer NI. If this is not available, we prefer NI*+XIDO*. If XIDO* is unavailable, we set it to zero. If that is unavailable, we prefer NI*+XI+DO |
| Firm Income | fi* | We use NIX*+XINT |
| Dividends for Common Shareholds | dvc | Compustat Item DVC |
| Total Dividends | div* | We prefer DVT. If this is not available, we use DV |
| Income Before Extraordinary Items Net Sales | ni_qtr* sale_qtr* | We use IBQ We use SALEQ |
| Cash Flow Statement | Cash Flow Statement | Cash Flow Statement |
| Capital Expenditures Capital Expenditures to Sales | capx capex_sale* | Compustat item CAPX We use CAPX / SALE* We Note that the free cash flow is |
| Free Cash Flow | fcf* | use OCF*-CAPX. com- puted before financing activities and sale of assets is taken into account |


11

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Equity Buyback | eqbb* | We use PRSTKC+PURTSHR Equity Buyback is mainly PRSTKC in NA and PURTSHR in GLOBAL. Either of PRSTKC or PURTSHR are allowed to be missing |
| Equity Issuance | eqis* | Compustat item SSTK |
| Equity Net Issuance | eqnetis* | We use EQIS*-EQBB*. Either EQIS* or EQBB* are allowed to be missing |
| Net Equity Payout | eqpo* | We use DIV*+EQBB* |
| Equity Net Payout | eqnpo* | We use DIV*-EQNETIS* |
| Net Long-Term Debt Issuance | dltnetis* | We prefer to use DLTIS-DLTR where we only require that one of the items are non-missing. If this is unavailable, we use LTDCH. If this is unavailable we use the yearly change in long-term book debt DLTT |
| Net Short-Term Debt Issuance | dstnetis* | We prefer DLCCH. If this is unavailable, we use the yearly change in short-term book debt DLC |
| Net Debt Issuance | dbnetis* | We use DLTNETIS*+DSTNETIS* and only require one of the items to be non-missing |
| Net Issuance | netis* | We use EQNETIS*+DBNETIS* and require that both EQNETIS* and DBNETIS* are non-missing If this |
| Financial Cash Flow | fincf* | We prefer FINCF. is unavailable, we use NETIS*- DV+FIAO+TXBCOF. If FIAO or TXBCOF is missing, it is set to |
| zero Balance Sheet - Assets | zero Balance Sheet - Assets | zero Balance Sheet - Assets |
| prefer Total Assets | at* | We to use AT. If this is unavailable, then we use SEQ* + DLTT + LCT + LO + TXDITC. If LCT, LO, or TXDITC are missing, then they are set to zero |
| Current Assets | * ca | We prefer ACT. If this is unavailable, we use RECT+INVT+CHE+ACO |
| Account Receivables | rec | Compustat item RECT |
| Cash and Short-Term Investment | cash | Compustat item CHE |
| Inventory | inv | Compustat item INVT |
| Non-Current Assets | nca* | We use AT* - CA* |
| Intangible Assets | intan | Compustat item INTAN |
| Investment and Advances | ivao | Compustat item IVAO |
| Property, Plans and Equipment Gross | ppeg | Compustat item PPEGT |
| Property, Plans and Equipment Net | ppen | Compustat item PPENT |
| Balance Sheet - Liabilities | Balance Sheet - Liabilities | Balance Sheet - Liabilities |
| Total Liabilities | lt | Compustat item LT |
| Current Liabilities | cl* | We prefer LCT. If this is unavailable, we use AP+ DLC+ TXP+ LCO |
| Accounts Payable | ap | Compustat item AP |
| Short-Term Debt | debtst | Compustat item DLC |
| Income Tax Payable | txp | Compustat item TXP |
| Non-Current Liabilities | ncl* | We use LT-CL* |
| Long-Term Debt | debtlt | Compustat item DLTT |
| Deferred Taxes and Investment Credit | txditc* | We prefer to use TXDITC. If this is unavailable, we use TXDB+ ITCB |
| Balance Sheet - Financing | Balance Sheet - Financing | Balance Sheet - Financing |
| Preferred Stock | pstk* | We prefer to use PSTKRV. If this is unavailable, we use PSTKL. If this is unavilable, we use PSTK |
| Total Debt | debt* | We use DLTT+ DLC. Either DLTT or DLC are allowed to me missing |
| Net Debt | netdebt* | We use DEBT*- CHE where we set CHE to zero if missing We prefer to use If this is unavailable, we use |
| Shareholders Equity | seq* | SEQ. CEQ+PSTK* where we set PSTK* to zero if missing. If this is unavailable, we use AT- LT |
| Book Equity | be* | We use SEQ*+TXDITC*-PSTK* where we set TXDITC* and PSTK* to zero if missing |
| Book Enterprise Value | bev* | We prefer to use ICAPT+DLC-CHE where DLC and CHE are set to zero if missing. If this is unavailable, we use SEQ*+NETDEBT*+ MIB where we set MIB to zero if miss- ing. In the global data ICAPT is reduced by Treasury stock |
| Balance Sheet - Summary | Balance Sheet - Summary | Balance Sheet - Summary |
| Net Working Capital | nwc* | We use CA*-CL* |
| Current Operating Assets | coa * | We use CA*- CHE |
| Current Operating Liabilities | col* | We use CL* - DLC. If DLC is missing, it is set to zero |
| Current Operating Working Capital Non-Current Operating Assets | cowc* ncoa* | We use COA*-COL* We use AT* - CA*- IVAO |


12

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Non-Current Operating Liabilities | ncol* | We use LT-CL*- DLTT |
| Net Non-Current Operating Assets | nncoa* | We use NCOA*-NCOL* |
| Financial Assets | fna* | We use IVST+ IVAO. If either is missing, they are set to zero |
| Financial Liabilities | fnl* | We use DEBT*+PSTK*. If PSTK* is missing, it is set to zero |
| Net Financial Assets | nfna* | We use FNA*-FNL* |
| Operating Assets | * oa | We use COA*+NCOA* |
| Operating Liabilities | ol* | We use COL*+NCOL* |
| Net Operating Assets | noa* | We use OA*-OL* |
| Long-Term NOA | lnoa* | PPENT + INTAN + AO - LO + DP |
| Liquid Current Assets | caliq* | We prefer to use CA* - INVT. If this is unavailable, we use CHE + RECT |
| Property Plant and Equipment Less Inventories | ppeinv* | PPEGT + INVT |
| Ortiz-Molina and Phillips Liquidity | aliq* | CHE + 0.75x COA* + 0.5(AT* - CA* - INTAN). If INTAN is missing, we set it to zero |
| Market Based | Market Based | Market Based |
| Market Equity | me | We use the market equity for the stock we deem to the primary security of the firm. Importantly, we do not align the market value with the end of the fiscal period. Instead, we update the market value on a monthly basis and align it with the most recently available accounting characteristic |
| Market Enterprise Value | mev* | x FX* |
| Market Assets | mat* | We use ME_COMPANY + NETDEBT* We use AT* x FX - BE* x FX + ME_COMPANY |
| Accruals | Accruals | Accruals |
| Operating Accruals | oacc* | We prefer NI*-OANCF. If that is unavailable, we use the yearly change in COWC*+the yearly change in NNCOA* |
| Total Accruals | tacc* | We use OACC* + the yearly change in NFNA* We prefer to use OANCF. If this is unavailable, we use NI*- |
| Operating Cash Flow | ocf* | OACC*. If this is unavailable, we use NI* + DP - WCAPT. If WCAPT is missing, we use 0. |
| Quarterly Operating Cash Flow | ocf_qtr* | We use OANCFQ. If this is unavailable, then we use IBQ + DPQ - WCAPTQ. If WCAPTQ is unavailable, we set it to unavailable, |
| Cash Based Operating Profitability | cop* | We prefer EBITDA* +XRD-OACC*. If XRD is we set it to zero |
| Other | Other | Other |
| Employees in Thousands | emp | Compustat item EMP |


Table 6: Accounting Characteristics

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Accounting Based Size Measures | Accounting Based Size Measures | Accounting Based Size Measures |
| Assets | assets | AT*t |
| Sales | sales | SALE*t |
| Book Equity | book_equity | BE*t |
| Net Income | net_income | NI*t |
| Enterprise Value | enterprise_value | M EV*t |
| Growth - Percentage 5 | Growth - Percentage 5 | Growth - Percentage 5 |
| Asset Growth lyr | at_gr1 | AT*t - 1 AT* t-12 |


5This refers to all variables with a suffix of " -gr1" or -gr3". The variables are percentage growth in the
"
accounting variables before the suffix. The number in the suffix refers to either 1 or 3 year growth. For all
variables, we only take the percentage growth if the denominator is above zero.

13

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Sales Growth 1yr | sale_gr1 | SALE*t - 1 SALE* t-12 |
| Current Asset Growth 1yr | ca_gr1 | CA*t - 1 CA* t-12 |
| Non-Current Asset Growth lyr | nca_gr1 | NCA* t - 1 NCA* t-12 |
| Total Liabilities Growth 1yr | lt_gr1 | LTt - 1 LTt-12 |
| Current Liabilities Growth 1yr | cl_gr1 | CL* t 1 - CL*t-12 |
| Non-Current Liabilities Growth 1yr | ncl_gr1 | NCL*t - 1 NCL* t-12 |
| Book Equity Growth 1yr | be_gr1 | BE* t 1 - BE* t-12 |
| Preferred Stock Growth 1yr | pstk_gr1 | PSTK* t 1 - PSTK* t-12 |
| Total Debt Growth 1yr | debt_gr1 | DEBT* t 1 - DEBT* t-12 |
| Cost of Goods Sold Growth 1yr | cogs_gr1 | COGSt - 1 COGSt-12 |
| Selling, General, and Administrative Expenses Growth 1yr | sga_gr1 | XSGAt - 1 XSGAt-12 |
| Operating Expenses Growth lyr | opex_gr1 | OPEX*t - 1 OPEX* t-12 |
| Asset Growth 3yr | at_gr3 | AT* t 1 - AT* t-36 |
| Sales Growth 3yr | sale_gr3 | SALE* t - 1 SALE* t-36 |
| Current Asset Growth 3yr | ca_gr3 | CA* 、 - 1 CA* t-36 |
| Non-Current Asset Growth 3yr | nca_gr3 | NCA* t 1 - NCA* t-36 |
| Total Liabilities Growth 3yr | lt_gr3 | LTt - 1 LTt -36 |
| Current Liabilities Growth 3yr | cl_gr3 | CL* t 1 - CL* t-36 |
| Non-Current Liabilities Growth 3yr | ncl_gr3 | NCL* t - 1 NCL* t-36 |
| Book Equity Growth 3yr | be_gr3 | BE* t 1 - BE* t-36 |
| Preferred Stock Growth 3yr | pstk_gr3 | PSTK*t - 1 PSTK*t-36 |
| Total Debt Growth 3yr | debt_gr3 | DEBT* t - 1 DEBT* t-36 |
| Cost of Goods Sold Growth 3yr | cogs_gr3 | COGSt - 1 COGSt-36 |
| Selling, General, and Administrative Expenses Growth 3yr | sga_gr3 | XSGAt XSGAt -36 - 1 |
| Operating Expenses Growth 3yr | opex_gr3 | OPEX*t - 1 OPEX* t-36 |
| Growth - Changed Scaled by Total Assets | Growth - Changed Scaled by Total Assets | Growth - Changed Scaled by Total Assets |
| Gross Profit Change lyr | gp-grla | GP*t-GP*t-12 AT*t |
| Operating Cash Flow Change lyr | ocf_grla | ocF*t-OCF* t- 12 AT*t |
| Cash and Short-Term Investments Change 1yr | cash_grla | CASHt-CASHt-12 AT*t |
| Inventory Change lyr | inv_grla | INVt-INVt-12 AT*t |
| Receivables Change 1yr | rec_grla | RECt-RECt-12 AT* |


14

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Property, Plans and Equiptment Gross Change 1yr | ppeg_grla | PPEGt-PPEGt-12 AT*t |
| Investment and Advances Change lyr | lti_grla | LTIt-LTIt-12 AT*t |
| Intangible Assets Change 1yr | intan_grla | INTANt-INTANt-12 AT*t |
| Short-Term Debt Change 1yr | debtst_grla | DEBTSTt-DEBT STt-12 AT*t |
| Accounts Payable Change lyr | ap_grla | APt-APt-12 AT*t |
| Income Tax Payable Change lyr | txp-grla | TXPt-TXPt-12 AT*t |
| Long-Term Debt Change 1yr | debtlt_gr1a | DEBTLTt-DEBTLTt - 12 AT*t |
| Deferred Taxes and Investment Credit Change 1yr | txditc_grla | TXDITC*t-TXDITC*t- 12 AT*t |
| Current Operating Assets Change 1yr | coa_grla | COA*t-COA* t-12 AT*t |
| Current Operating Liabilities Change 1yr | col_grla | COL*t-COL* t-12 AT* t |
| Current Operating Working Capital Change 1yr | cowc_grla | cowc*t-cowc* t-12 AT*t |
| Non-Current Operating Assets Change 1yr | ncoa_grla | NCOA*t-NCOA* t-12 AT*t |
| Non-Current Operating Liabilities Change lyr | ncol_grla | NCOL*1-NCOL*1-12 AT*t |
| Net Non-Current Operating Assets Change 1yr | nncoa_grla | NNCOA*t-NNCOA* t-12 AT*t |
| Operating Assets Change 1yr | oa_grla | OA*t -OA*t-12 AT* t |
| Operating Liabilities Change lyr | ol_grla | OL* t -OL* t-12 AT* t |
| Net Operating Assets Change 1yr | noa_grla | NOA*t-NOA*. t-12 AT*t |
| Financial Assets Change 1yr | fna_grla | FNA* t -FNA*t-12 AT*t |
| Financial Liabilities Change 1yr | fnl_grla | FNL* t -FNL*t-12 AT*t |
| Net Financial Assets Change 1yr | nfna_grla | NFNA*t-NFNA* t-12 AT*t |
| Operating Profit before Depreciation Change lyr | ebitda_grla | EBITDA*t-EBITDA* t-12 AT*t |
| Operating Profit after Depreciation Change 1yr | ebit_grla | EBIT*t-EBIT*t-12 AT*t |
| Operating Earnings to Equity Change 1yr | ope_grla | OP E* t -OPE* t-12 AT*t |
| Net Income Change 1yr | ni_grla | NI* t -NI* t-12 AT*t |
| Depreciation and Amortization Change 1yr | dp_grla | DPt-DPt-12 AT*t |
| Free Cash Flow Change 1yr | fcf_grla | FCF*t-FCF* t-12 AT*t |
| Net Working Capital Change 1yr | nwc_grla | NW C*t-NWC*t-12 AT*t |
| Net Income Including Extraordinary Items Change 1yr | nix_grla | NIX*t-NIX*t-12 AT*t |
| Equity Net Issuance Change 1yr | eqnetis_grla | EQN ETIS*t-EQN ETIS* t-12 AT*t |


15

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Net Long-Term Debt Issuance Change 1yr | dltnetis_grla | DLTN ETIS*t-DLTN ETIS* t-12 AT*t |
| Net Short-Term Debt Issuance Change lyr | dstnetis_grla | DSTN ETIS*t-DSTN ETIS* t- 12 AT*t |
| Net Debt Issuance Change 1yr | dbnetis_grla | DBNETIS*t-DBNETIS* t-12 AT*t |
| Net Issuance Change 1yr | netis_grla | N ETIS*t-NETIS* t-12 AT* t |
| Financial Cash Flow Change lyr | fincf_grla | FINCF*1-FINCF*1-12 AT*t |
| Equity Net Payout Change lyr | eqnpo_grla | EQNPO*t-EQNPO* t-12 AT*t |
| Effective Tax Rate Change 1yr | tax_grla | TAXt -TAXt-12 AT*t |
| Dividend Payout Ratio Change 1yr | div_grla | DIV*t-DIV*t-12 AT*t |
| Equity Buyback Change 1yr | eqbb_grla | EQBB*t-EQBB* t- 12 AT*t |
| Equity Issuance Change 1yr | eqis_grla | EQIS* t -EQIS* t-12 AT*t |
| Net Equity Payout Change 1yr | eqpo_grla | EQPO*t-EQPO* t- 12 AT*t |
| Capital Expenditures Change 1yr | capx_grla | CAPXt-CAPXt-12 AT*t |
| Gross Profit Change 3yr | gp-gr3a | GP*t-GP* t-36 AT*t |
| Operating Cash Flow Change 3yr | ocf_gr3a | ocF*t-OCF* t-36 AT*t |
| Cash and Short-Term Investments Change 3yr | cash_gr3a | CASHt-CASHt-36 AT*t |
| Inventory Change 3yr | inv_gr3a | INVt-INVt-36 AT*t |
| Receivables Change 3yr | rec_gr3a | RECt-RECt-36 AT*t |
| Property, Plans and Equipment Gross Change 3yr | ppeg_gr3a | PPEGt -PPEGt-36 AT*t |
| Investment and Advances Change 3yr | lti_gr3a | LTIt-LTIt-36 AT*t |
| Intangible Assets Change 3yr | intan_gr3a | INTANt-INTANt-36 AT*t |
| Short-Term Debt Change 3yr | debst_gr3a | DEBTSTt-DEBT STt-36 AT*t |
| Accounts Payable Change 3yr | ap-gr3a | APt-APt-36 AT*t |
| Income Tax Payable Change 3yr | txp_gr3a | TXPt-TXPt-36 AT*t |
| Long-Term Debt Change 3yr | debtlt_gr3a | DEBTLT⌀ -DEBTLTt - 36 AT*t |
| Deferred Taxes and Investment Credit Change 3yr | txditc_gr3a | TXDITC*:-TXDITC* t-36 AT*t |
| Current Operating Assets Change 3yr | coa_gr3a | COA*t-COA* t-36 AT*t |
| Current Operating Liabilities Change 3yr | col_gr3a | COL*t-COL*t-36 AT*t |
| Current Operating Working Capital Change 3yr | cowc_gr3a | cowc*t-cowc* t-36 AT*t |
| Non-Current Operating Assets Change 3yr | ncoa_gr3a | NCOA*t-NCOA* t-36 AT*t |
| Net Non-Current Operating Assets Change 3yr | nncoa_gr3a | NNCOA*t-NNCOA*t-36 AT*t |
| Operating Assets Change 3yr | oa_gr3a | OA*t-OA* t-36 AT*t |


16

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Operating Liabilities Change 3yr | ol_gr3a | OL*t -OL* t-36 AT*t |
| Net Operating Assets Change 3yr | noa_gr3a | NOA*t-NOA*t-36 AT*t |
| Financial Assets Change 3yr | fna_gr3a | FNA*t-FNA*t-36 AT*t |
| Financial Liabilities Change 3yr | fnl_gr3a | FNL* t -FNL* t-36 AT* t |
| Net Financial Assets Change 3yr | nfna_gr3a | NF NA*t-NFNA*t-36 AT*t |
| Operating Profit before Depreciation Change 3yr | ebitda_gr3a | EBITDA*t-EBITDA* t-36 AT*t |
| Operating Profit after Depreciation Change 3yr | ebit_gr3a | EBIT*t-EBIT* t-36 AT*t |
| Operating Earnings to Equity Change 3yr | ope_gr3a | OPE*t -OPE* t-36 AT*t |
| Net Income Change 3yr | ni_gr3a | NI* t -NI* t-36 AT*t |
| Depreciation and Amortization Change 3yr | dp_gr3a | DPt-DPt-36 AT*t |
| Free Cash Flow Change 3yr | fcf_gr3a | FCF*t-FCF* t- 36 AT*t |
| Net Working Capital Change 3yr | nwc_gr3a | NWC*t-NWC* t-36 AT*t |
| Inventory Change 1yr | inv_gr3a | INVt-INVt-36 AT*t |
| Non-Current Operating Liabilities Change 3yr | ncol_gr3a | NCOL*t-NCOL* t- 36 AT*t |
| Net Income Including Extraordinary Items Change 3yr | nix_gr3a | NIX*t-NIX*t-36 AT*t |
| Equity Net Issuance Change 3yr | eqnetis_gr3a | EQN ETIS*t-EQN ETIS* t-36 AT*t |
| Net Long-Term Debt Issuance Change 3yr | dltnetis_gr3a | DLTNETIS*t-DLTN ETIS* t- 36 AT*t |
| Net Short-Term Debt Issuance Change 3yr | dstnetis_gr3a | DSTN ETIS*t-DSTN ETIS*t-36 AT*t |
| Net Debt Issuance Change 3yr | dbnetis_gr3a | DBNETIS*t-DBNETIS* t-36 AT*t |
| Net Issuance Change 3yr | netis_gr3a | N ETIS*t-NETIS* t-36 AT*t |
| Financial Cash Flow Change 3yr | fincf_gr3a | FINCF*t-FINCF* t-36 AT*t |
| Net Working Capital Change 3yr | nwc_gr3a | NW C*t-NWC*t-36 AT*t |
| Equity Net Payout Change 3yr | eqnpo_gr3a | EQNPO*t-EQNPO* t - 36 AT_t |
| Effective Tax Rate Change 3yr | tax_gr3a | TAXt-TAXt-36 AT_t |
| Dividend Payout Ratio Change 3yr | div_gr3a | DIV*t-DIV*t-36 AT_t |
| Equity Buyback Change 3yr | eqbb_gr3a | EQBB*t-EQBB* t-36 AT_t |
| Equity Issuance Change 3yr | eqis_gr3a | EQIS*t-EQIS*t-36 AT_t |
| Net Equity Payout Change 3yr | eqpo_gr3a | EQPO*t-EQPO* t-36 AT_t |
| Capital Expenditures Change 3yr | capx_gr3a | CAPXt-CAPXt-36 AT_t |
| Investment | Investment | Investment |
| Capital Expenditures scaled by Assets | capx_at | CAPXt AT*t |


17

| Name | Abbreviation | Construction |
| --- | --- | --- |
| R&D scaled by Assets | rd_at | XRDt AT* t |
| Non-Recurring Items | Non-Recurring Items | Non-Recurring Items |
| Special Items scaled by Assets | spi_at | SPIt AT*t XI DO* t |
| Extraordinary Items and Discontinued Opera- tions scaled by Assets | xido_at | AT* t |
| Non-Recurring Items scaled by Assets | nri_at | SPIt+XIDO*t AT*t |
| Profit Margins | Profit Margins | Profit Margins |
| Gross Profit Margin | gp_sale | GP* SALE* t |
| Operating Profit Margin before Depreciation | ebitda_sale | EBITDA* t SALE* t |
| Operating Profit Margin after Depreciation | ebit_sale | EBIT* t SALE * |
| Pretax Profit Margin | pi_sale | t PI* t SALE* |
| Profit Margin before XI | ni_sale | t NI*t SALE* t |
| Net Net Profit Margin | nix_sale | NIX* t |
|  |  | SALE* t |
| Free Cash Flow Margin | fcf_sale | FCF* SALE* t |
| Operating Cash Flow Margin | ocf_sale | OCF* t SAL E* t |
| Return on Assets | Return on Assets | Return on Assets |
| Gross Profit scaled by Assets | gp_at | GP* t AT*t |
| Operating Profit before Depreciation scaled by Assets | ebitda_at | EB ITDA* t AT* t |
| Operating Profit after Depreciation scaled by Assets | ebit_at | EBIT* t AT* t |
| Firm Income scaled by Assets | fi_at | FI* t AT* t |
| Cash Based Operating Profitability scaled by Assets | cop_at | COP* t AT* t |
| Return on Book Equity | Return on Book Equity | Return on Book Equity |
| Operating Profit to Equity scaled by BE | ope_be | OPE* t BE* t |
| Net Income scaled by BE | ni_be | NI* t BE * t |
| Net Income Including Extraordinary Items scaled by BE | nix_be | NIX* t BE* t |
| Operating Cash Flow scaled by BE | ocf_be | OCF* t BE* t |
|  | fcf_be | FCF* t B E* t |
| Free Cash Flow scaled by BE Return on Invested Capital | Free Cash Flow scaled by BE Return on Invested Capital | Free Cash Flow scaled by BE Return on Invested Capital |
| Gross Profit scaled by BEV | gp_bev | GP* BEV*t |
| Operating Profit before Depreciation scaled by BEV | ebitda_bev | EBITDA*t BEV*t |


18

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Operating Profit after Depreciation scaled by BEV Firm Income scaled by BEV Cash Based Operating Profitability scaled by BEV | ebit_bev fi_bev cop_bev | EBIT*t BEV * t FI* t BEV* t COP* t BEV* t |
| Return on Physical Capital | Return on Physical Capital | Return on Physical Capital |
| Gross Profit scaled by PPEN Operating Profit before Depreciation scaled by PPEN Free Cash Flow scaled by PPEN | gp-ppen ebitda_ppen fcf_ppen | GP*t PPENt EBITDA* t PPENt FCF*t PPENt |
| Issuance | Issuance | Issuance |
| Financial Cash Flow scaled by Assets Net Issuance scaled by Assets Equity Net Issuance scaled by Assets Equity Issuance scaled by Assets Net Debt Issuance scaled by Assets Net Long-Term Debt Issuance scaled by Assets Net Short-Term Debt Issuance scaled by As- sets | fincf_at netis_at eqnetis_at eqis_at dbnetis_at dltnetis_at dstnetis_at | FINCF*t AT*t N ETIS*t AT*t EQN ETIS* t AT*t EQIS*t AT*t DBN ETIS*t AT*t DLTN ETIS* t AT*t DST N ETIS* t AT*t |
| Equity Payout | Equity Payout | Equity Payout |
| Equity Net Payout scaled by Assets Net Equity Payout scaled by Assets Total Dividends scaled by Assets | eqnpo_at eqbb_at div_at | EQNPO*t AT*t EQBB* t AT* t DIV*t AT* t |
| Accruals | Accruals | Accruals |
| Operating Accruals Percent Operating Accruals Total Accruals Percent Total Accruals Net Operating Asset to Total Assets | oaccruals_at oaccruals_ni taccruals_at taccruals_ni noa_at | OACC* t AT* t OACC* t NIX*t TACC* t AT* t TACC* t |NIX*t| NOA*t AT* |
| Capitalization/Leverage Ratios | Capitalization/Leverage Ratios | Capitalization/Leverage Ratios |
| Common Equity scaled by BEV Total Debt scaled by BEV Cash and Short-Term Investments scaled by BEV Preferred Stock scaled by BEV | be_bev debt_bev cash_bev pstk_bev | BE* t BEV*t DE BT* BEV * t CASHt BEV* t PSTK* t BEV* t |


19

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Long-Term Debt scaled by BEV | debtlt_bev | DEBTLTt BEV*t |
| Short-Term Debt scaled by BEV | debtst_bev | DE BTSTt BEV*t |
| Total Debt scaled by MEV | debt_mev | DE BT* t M EV* t |
| Preferred Stock scaled by MEV | pstk_mev | PSTK*t * M EV t |
| Long-Term Debt scaled by MEV | debtlt_mev | DEBTLTt M EV* t |
| Short-Term Debt scaled by MEV | debtst_mev | DEBTSTt M EV* |
| t Financial Soundness Ratios | t Financial Soundness Ratios | t Financial Soundness Ratios |
| Interest scaled by Total Debt | int_debt | INTt DEBT*t |
| Interest scaled by Long- Term Debt | int_debtlt | INT+ DEBTLTt |
| Operating Profit before Depreciation scaled by Total Debt | ebitda_debt | EBITDA* t DEBT* t |
| Profit before D&A scaled by Current Liabili- ties | profit_cl | EBITDA*t CL* t |
| Operating Cash Flow scaled by Current Lia- bilities | ocf_cl | oc F* t CL * t |
| Operating Cash Flow scaled by Total Debt | ocf_debt | OCF* t DEBT * t |
| Cash Balance scaled by Total Liabilities | cash_lt | CASHt LTt |
| Inventory scaled by Current Assets | inv_act | INVt ACTt |
| Receivables scaled by Current Assets | rec_act | RECt ACTt |
| Short-Term Debt scaled by Total Debt | debtst_debt | DEBTSTt DEBT* t |
| Current Liabilities scaled by Total Liabilities | cl_lt | CL*t LTt |
| Long-Term Debt scaled by Total Debt | debtlt_debt | DEBTLTt DEBT* |
| Operating Leverage | opex_at | t OPEX*t AT* t |
| Free Cash Flow scaled by Operating Cash Flow | fcf_ocf | FCF* t OCF* t |
| Total Liabilities scaled by Total Tangible As- sets | lt_ppen | LTt PPENt |
| Long-Term Debt to Book Equity | debtlt_be | DEBTLTt BE*t |
| Working Capital scaled by Assets | nwc_at | NWC*t AT* |
| t Solvency Ratios | t Solvency Ratios | t Solvency Ratios |
| Debt-to-Assets | debt_at | DEBT*t AT*t |
| Debt to Shareholders' Equity Ratio | debt_be | DEBT*t BE* t |
| Interest Coverage Ratio | ebit_int | EBIT* t INTt |
| Liquidity Ratios | Liquidity Ratios | Liquidity Ratios |
| Days Inventory Outstanding | inv_days | INVt+INVt-12 COGSt x 365 |


20

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Days Sales Outstanding | rec_days | RECt+RECt-12 2 365 x SALE*t |
| Days Accounts Payable Outstanding | ap_days | APt+APt-12 2 x 365 COGSt |
| Cash Conversion Cycle | cash_conversion | INV _DAYSt + REC_DAYSt - AP_DAYSt |
| Cash Ratio | cash_cl | CASHt CL* t |
| Quick Ratio | caliq_cl | CALIQ*t CL* t |
| Current Ratio | ca_cl | CA* CL* |
| t Activity/Efficiency Ratios | t Activity/Efficiency Ratios | t Activity/Efficiency Ratios |
| Inventory Turnover | inv_turnover | COGSt (INVt+INVt-12)/2 |
| Asset Turnover | at_turnover | SALE*t (AT*t+AT*t-12)/2 |
| Receivables Turnover | rec_turnover | SALE*t (RECt+RECt-12)/2 |
| Account Payables Turnover | ap_turnover | COGSt+INVt-INVt -12 (APt+APt-12)/2 |
| Miscellaneous | Miscellaneous | Miscellaneous |
| Advertising scaled by Sales | adv_sale | XADt SALE* t |
| Labor Expense scaled by Sales | staff_sale | XLRt SALE* t |
| Sales scaled by BEV | sale_bev | SALE* t BEV * t |
| R&D scaled by Sales | rd_sale | X RDt SALE* t |
| Sales scaled by Total Stockholders' Equity | sale_be | SALE* t BE * t |
| Dividend Payout Ratio | div_ni | DVCt NI* t |
| Sales scaled by Working Capital | sale_nwc | SALE* t NWC* t |
| Effective Tax Rate | tax_pi | TAXt PI*t |
| Balance Sheet Fundamental to Market Equity | Balance Sheet Fundamental to Market Equity | Balance Sheet Fundamental to Market Equity |
| Book Equity scaled by Market Equity | be_me | BE* t M Et |
| Total Assets scaled by Market Equity | at_me | AT* t MEt |
| Cash and Short-Term Investments scaled by Market Equity | cash_me | CASHt M Et |
| Income Fundamentals to Market Equity | Income Fundamentals to Market Equity | Income Fundamentals to Market Equity |
| Gross Profit scaled by ME | gp_me | GP*t M Et |
| Operating Profit before Depreciation scaled by ME | ebitda_me | EBITDA*t M Et |
| Operating Profit after Depreciation scaled by ME | ebit_me | EBIT* t MEt |
| Operating Earnings to Equity scaled by ME | ope_me | OPE* t MEt |
| Net Income scaled by ME | ni_me | NI* t MEt |
| Sales scaled by ME | sale_me | SALE* t M Et |


21

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Operating Cash Flow scaled by ME Free Cash Flow scaled by ME Net Income Including Extraordinary Items scaled by ME Cash Based Operating Profitability scaled by ME R&D scaled by ME | ocf_me fcf_me nix_me cop_me rd_me | OCF*t M Et FCF* t MEt NIX* t MEt COP* t MEt XRDt M Et |
| Balance Sheet Fundamentals to Market Enterprise Value | Balance Sheet Fundamentals to Market Enterprise Value | Balance Sheet Fundamentals to Market Enterprise Value |
| Book Equity scaled by MEV Total Assets scaled by MEV Cash and Short-Term Investments scaled by MEV Book Enterprise Value scaled by MEV Property, Plans and Equipment Net scaled by MEV | be_mev at_mev cash_mev bev _mev ppen_mev | BE* と MEV * t AT* MEV* t CASHt MEV* t BEV* t MEV * t PPENt MEV* t |
| Equity Payout/Issuance to Market Equity | Equity Payout/Issuance to Market Equity | Equity Payout/Issuance to Market Equity |
| Total Dividends scaled by ME Equity Buyback scaled by ME Equity Issuance scaled by ME Net Equity Payout scaled by ME Equity Net Payout scaled by ME Equity Net Issuance scaled by ME | div _me eqbb_me eqis_me eqpo_me eqnpo_me eqnetis_me | DIV*t MEt EQBB*t M Et EQIS*t MEt EQPO*t MEt EQNPO*t MEt EQN ETIS*t MEt |
| Debt Issuance to Market Enterprise Value | Debt Issuance to Market Enterprise Value | Debt Issuance to Market Enterprise Value |
| Net Long-Term Debt Issuance scaled by MEV Net Short-Term Debt Issuance scaled by MEV Net Debt Issuance scaled by MEV | dltnetis_mev dstnetis_mev dbnetis_mev | DLTNETIS*t MEV*t DSTN ETIS*t MEV*t DBNETIS*t MEV*t |
| Firm Payout / Issuance to Market Enterprise Value | Firm Payout / Issuance to Market Enterprise Value | Firm Payout / Issuance to Market Enterprise Value |
| Net Issuance scaled by MEV | netis_mev | NETIS*t M EV*t |
| Income Fundamentals to Market Enterprise Value | Income Fundamentals to Market Enterprise Value | Income Fundamentals to Market Enterprise Value |
| Gross Profit scaled by MEV Operating Profit before Depreciation scaled by MEV Operating Profit after Depreciation scaled by MEV Sales scaled by MEV Operating Cash Flow scaled by MEV | gp_mev ebitda_mev ebit_mev sale_mev ocf_mev | GP*t MEV*t EBITDA*t MEV* t EBIT* t MEV* t SALE* t MEV * t OCF* t M EV* t |


22

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Free Cash Flow scaled by MEV Cash Based Operating Profitability scaled by MEV Financial Cash Flow Change scaled by MEV | fcf_mev cop_mev fincf_mev | FCF*t MEV * t COP* t * MEV t FINCF* t MEV * t |
| New Variables not in HXZ | New Variables not in HXZ | New Variables not in HXZ |
| Net Income to Sales Quarterly Volatility | niq_saleq_std | NI-QTR*t �8Q SALE-QTR*t |
| Net Income scaled by Employees | ni_emp | NI* t EMPt |
| Sales scaled by Employees | sale_emp | SALE*t EMPt |
| Net Income scaled by Assets | ni_at | NI* t AT* t |
| Operating Cash Flow scaled by Assets | ocf_at | OCF*t AT* t |
| Operating Cash Flow to Assets 1 yr Change | ocf_at_chg1 | OCF_ATt - OCF_ATt-12 |
| Quarterly ROE Volatility | roeq_be_std | NI-QTR*t ) �16Q BE*t |
| ROE Volatility | roe_be_std | NI* ⌀60m BE* t |
| Gross Product to Assets 5 yr Change | gpoa_ch5 | GP* t- 60 GP* t - * AT * AT t t- 60 |
| ROE 5 yr Change | roe_ch5 | NI * NI* t- 60 t * BE * BE t t- 60 |
| ROA 5 yr Change | roa_ch5 | NI * NI* t- 60 t AT* t AT* t-60 |
| Operating Cash Flow to Assets 5 yr Change | cfoa_ch5 | OCF* t OCF* t- 60 - AT* t AT* t-60 |
| Gross Product to Sales 5 yr Change | gmar_ch5 | GP* GP* t-60 - SALE* t SALE* t- 60 |
| New Variables from HXZ | New Variables from HXZ | New Variables from HXZ |
| Cash and Short Term Investments scaled by Assets | cash_at | CASHt AT*t |
| Number of Consecutive Earnings Increases | ni_inc8q | Count number of earnings increases over past 8 quarters |
| Change in Property, Plant and Equipment Less Inventories scaled by lagged Assets | ppeinv_grla | PPEINV*1-PPEINV*1-12 AT* t-12 |
| Change in Long-Term NOA scaled by average Assets | lnoa_grla | LNOA*t-LNOA* t-12 AT*t-AT* t-12 |
| CAPX 1 year growth | capx_gr1 | CAPXt - 1 CAPXt-12 |
| CAPX 2 year growth | capx_gr2 | CAPXt CAPXt-24 - 1 |
| CAPX 3 year growth | capx_gr3 | CAPXt - 1 CAPXt-36 |
| Change in Short-Term Investments scaled by Assets | sti_grla | IVSTt-IVSTt -12 AT*t |
| Quarterly Income scaled by BE | niq_be | NI-QTR*t BE* t-3 |
| Change in Quarterly Income scaled by BE | niq_be_chg1 | NIQ_BEt - NIQ-BEt-12 |
| Quarterly Income scaled by AT | niq_at | NI-QTR*t AT* t-3 |
| Change in Quarterly Income scaled by AT | niq_at_chg1 | NIQ_ATt - NIQ-ATt-12 |


23

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Quarterly Sales Growth | saleq_gr1 | SALE QTR*t - 1 SALE-QTR* t-12 |
| R&D Capital-to-Assets | rd5_at | �:=0(1-.2xn)(XRDt-12en) AT*t |
| Age | age | Age of the firms in months |
| Change Sales minus Change Inventory | dsale_dinv | CHG_TO_EXP(SALE*t) - CHG_TO_EXP(INVt) |
| Change Sales minus Change Receivables | dsale_drec | CHG_TO EXP(SALE*t) - CHG_TO _EXP(RECt) |
| Change Gross Profit minus Change Sales | dgp_dsale | CHG_TO EXP(GP*t) - CHG_TO_EXP(SALE*t) |
| Change Sales minus Change SG&A | dsale_dsga | CHG_TO_EXP(SALE*t) - CHG_TO_EXP(XSGAt) |
| Earnings Surprise | saleq_su | SUR(SALE_QTR*) |
| Revenue Surprrise | niq_su | SUR(NI_QTR*) |
| Total Debt scaled by ME | debt_me | DEBT*t M Et |
| Net Debt scaled by ME | netdebt_me | NETDEBT*t M Et |
| Abnormal Corporate Investment | capex_abn | CAPX_SALE*t 1 (CAPX_SALE*. t-12+CAPX_SALE*t-24+CAPX_SALE* t-36)/3 |
| Inventory Change 1 yr | inv_gr1 | INVt - 1 INVt-12 |
| Book Equity Change 1 yr scaled by Assets | be_grla | BE*t-BE* t-12 AT* t |
| Ball Operating Profit to Assets | op_at | OP* t AT* t |
| Earnings before Tax and Extraordinary Items to Net Income Including Extraordinary Items | pi_nix | PI* * NIX t |
| Ball Operating Profit scaled by lagged Assets | op_atl1 | OP* t AT*t-12 |
| Operating Profit scaled by lagged Book Equity | ope_bel1 | OPE* t BE* t-12 |
| Gross Profit scaled by lagged Assets | gp_atl1 | GP* t AT* t-12 |
| Cash Based Operating Profitability scaled by lagged Assets | cop_atl1 | COP* t AT* t-12 |
| Book Leverage | at_be | AT* t BE* t |
| Operating Cash Flow to Sales Quarterly Volatility | ocfq_saleq_std | OCF_QTR* �16Q SALE-QTR*t |
| Liquidity scaled by lagged Assets | aliq_at |  |
| Liquidity scaled by lagged Market Assets | aliq_mat | ![image](/image/placeholder)
ALIQ*t
AT*
t-12
ALIQ* t
MAT*
t-12
CASHt +0.715x RECt+0.547xINVt +0.535x PPEGt
AT*t |
| Tangibility | tangibility |  |
| Equity Duration | eq_dur | Outlined in detail here |
| Piotroski F-Score | f_score | Outlined in detail here |
|  | o_score |  |
| Ohlson O-Score |  | Outlined in detail here |


24

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Altman Z-Score | z_score | Outlined in detail here |
| Kaplan- Zingales Index | kz_index | Outlined in detail here |
| Intrinsic Value | intrinsic_value | Outlined in detail here |
| Intrinsic value-to-market | ival_me | INTRINSIC_VALUE*, MEt |
| Sales scaled by Employees Growth 1 yr | sale_emp_gr1 | SALE-EMPt - 1 SALE-EMPt-12 |
| Employee Growth 1 yr | emp_gr1 | EM Pt-EMPt-12 0.5x EMPt+0.5x EM Pt- 12 |
| Earnings Variability | earnings_variability | �60M (NI*t/AT*t-12 ⌀60m (OCF*t/AT*t-12) |
| 1 yr lagged Net Income to Assets | ni_arl | cov((NI* /AT*)*,(NI*/AT*)t-12) var((NI*/AT*)t-12) |
|  |  |  |
| Net Income Idiosyncratic Volatility | ni_ivol | Outlined in detail here |


# 7 Market Based Characteristics

Datasets

- ● CRSP.MSF
- ● CRSP.DSF
- ● COMP.SECD
- ● COMP.G_SECD
- COMP.SECM
- ● COMP.SECURITY
- ● COMP.G_SECURITY


Market Variables
A suffix of 7*7 indicates that we have altered or renamed the original item.

Table 7: Market Variables

| Name | Abbreviation | Construction |
| --- | --- | --- |
| CRSP VariablesⓇ | CRSP VariablesⓇ | CRSP VariablesⓇ |


6lag is a lag function where lag(x) is the value of x from the previous time period

25

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Share Adjustment Factor | adjfct* | We use CFACSHR |
| Shares | shares* | We use SHROUT /1000 so shares outstanding are in millions. |
| Price | prc* | We use PRC |
| Local Price | prc_local* | We use PRC* then |
| Highest Daily Price | prc_high | We use ASKHI. If PRC* or AKSHI are negative, PRC_HIGH is set to missing |
| Lowest Daily Price | prc_low | We use BIDLO. If PRC* or BIDLO are negative, then PRC_LOW is set to missing |
| Market Equity | me* | We use PRC* xSHARES* so market equity is quoted in mil- lion USD. |
| Company Market Equity | me_company* | We sum ME* grouped by PERMCO and date |
| Trading Volume | tvol* | We use VOL |
| Dollar Volume | dolvol* | We use TVOL*xPRC* |
| Return | RET* | We use RET. In case of delisting, we calculate as (1+RET)*(1+DLRET)-1 |
| Local Return | ret_local* | We use RET. In case of delisting, we calculate as (1+RET)*(1+DLRET)-1 use RET*- T30RET/21. T30RET is unavailable, |
| Excess Return | ret_exc* | We If we use RF. If the return is a monthly return rather than a daily return, the T30RET is divided by 1 rather than 21. |
| Excess Return t+1 Since | ret_exc_lead1m* | Excess return (ret_exc*) in month t+1 We automatically set this to 1 |
| Time Most Recent Return Cumulative Return | ret_lag_dif* ri* | This is the cumulative return estimated from RET* |
| Monthly Dividend | div_tot* | We use (RET -RETX) xlag(PRC*)x (CFACSHR /lag(CFACSHR)) |
| Compustat Variables | Compustat Variables | Compustat Variables |
| Share Adjustment Factor | adjfct* | We use AJEXDI |
| Shares | shares* | We use CSHOC/1000000 |
| Price | prc* | We use PRC_LOCAL*xFX |
| Local Price | prc_local* | We use PRCCD |
| Market Equity | me* | We use PRC* xSHARES* |
| Company Market Equity Trading Volume | me_company* tvol* | We use ME* We use CSHTRD |
| Dollar Volume | dolvol* | We use TVOL* xPRC* |
| Cumulative Return - Local | ri_local* | We use PRC_LOCAL*x TRFD/AJEXDI delisting, |
| Local Return | ret_local* | We use RI_LOCAL* /lag(RI_LOCAL*) - 1. In case of we calculate as (RI_LOCAL* /lag(RI_LOCAL*) * (1+dlret) - 1) |
| Cumulative Return | ri* | RLLOCAL* x FX* |
| Return | RET* | We use RI* /lag(RI*) - 1. In case of delisting, we calculate as (RI* /lag(RI*) * (1+dlret) -1) |
| Excess Return | ret_exc* | We use RET*-T30RET/21. If T30RET is unavailable, we use RF. If the return is a monthly return rather than a daily return, |
|  |  | the T30RET is divided by 1 rather than 21. |
| Excess Return t+1 | ret_exc_lead1m* | Excess return (ret_exc*) in month t+1 We estimate the number of days since the previous return. If is in |
| Time Since Most Recent Return | ret_lag_dif* | the returns are monthly rather than daily, then the time months |
| Monthly Dividend | div_tot* | We use DIV x FX*. If DIV is missing, we set it to zero We use it to |
| Cash Dividend | div_cash* | DIVD x FX*. If DIVD is unavailable, we set zero |
| Special Cash Dividend | div_spc* | We use DIVSP x FX*. If DIVSP is unavailable, we set it to zero |
| Bid-Ask Average Dummy | bidask* | When PRCSTD = 4 then 1, otherwise 0 |
| Asset Pricing Factors | Asset Pricing Factors | Asset Pricing Factors |
| Excess Market Return | mktrf* | Country specific market return |
| High Minus Low | hml* | Country specific factor following Fama and French (1993) and using breakpoints from non-micro cap stocks within the coun- try |
| Small Minus Big ala Fama-French | smb_ff* | Average of small portfolios minus average of large portfolios from hml* |


7 dlret is set to -0.3 when dlsrni is '02' or '03' and set to 0 otherwise

26

| N ame | Abbreviation | Construction |
| --- | --- | --- |
| Return on Equity | roe* | Country specific factor following Hou, Xue and Zhang (2015) and using breakpoints from non-micro cap stocks within the country. We use double sorts on return on equity and size rather than triple sorts with investment, due to the limited number of stocks in some international markets. Country specific factor following Hou, Xue and Zhang (2015) |
| Investment | inv* | and using breakpoints from non-micro cap stocks within the country. We use double sorts on investment and size rather than triple sorts with return on equity, due to the limited number of stocks in some international markets large portfolios |
| Small Minus Big ala Hou et al | smb_hxz* | Average of small portfolios minus average of from roe* and inv* |
| Market Volatility for Each Stock | _mktvol_zd* | �zD(MKTRF*t) 8 |


# Table 8: Market Characteristics

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Market Based Size Measures | Market Based Size Measures | Market Based Size Measures |
| Market Equity | market_equity | ME*t |
| Total Dividend Paid to Market Equity | Total Dividend Paid to Market Equity | Total Dividend Paid to Market Equity |
| Dividend to Price - 1 Month Dividend to Price - 3 Months Dividend to Price - 6 Months Dividend to Price - 12 Months | div1m_me div3m_me div6m_me div12m_me | DIV TOT*txSHARES*t ME*t En=⌀ DIV _TOT*t-n xSH ARES* t-n ME*t En=o DIV _TOT*t-n xSH ARES* t-n ME*t En=⌀ DIV _TOT*t-nxSH ARES* t-n ME*t |
| Special Dividend Paid to Market Equity | Special Dividend Paid to Market Equity | Special Dividend Paid to Market Equity |
| Special Dividend to Price - 1 Month Special Dividend to Price - 12 Month | divspc1m_me divspc12m_me | DIV_SPC*txSHARES*t ME*t En=0 DIV-SPC*t-n xSH ARES* t-n ME*t |
| Change in Shares Outstanding | Change in Shares Outstanding | Change in Shares Outstanding |
| Change in Shares - 1 Month Change in Shares - 3 Month Change in Shares - 6 Month Change in Shares - 12 Month | chcsho_1m chcsho_3m chcsho_6m chcsho.12m | SH ARES*txADJFCT*t - 1 SHARES*1-1xADJFCT* t-1 SH ARES*txADJFCT*: - 1 SHARES*(-3XADJFCT* t-3 SH ARES*txADJFCT*t - 1 SH ARES*1-6XADJFCT* t-6 SHARES*txADJFCT*t - 1 SH ARES* t-12xADJFCT* t-12 |
| Net Equity Payout | Net Equity Payout | Net Equity Payout |
| Net Equity Payout - 1 Month Net Equity Payout - 3 Month Net Equity Payout - 6 Month Net Equity Payout - 12 Month | eqnpo_1m eqnpo_3m eqnpo_6m eqnpo_12m | RI*t ME* log - log RI* t-1 M E* t-1 RI* t log t M E* log - RI* t-3 ME* t-3 RI* t log M E* log - RI* t-6 ME* t-6 RI* ME* log - log RI*t-12 M E* t-12 |
| Momentum/Reversal | Momentum/Reversal | Momentum/Reversal |


8Must have enough non-missing values of stock to be estimated

27

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Short Term Reversal | ret_1_0 | RI*t - 1 RI* t-1 |
| Momentum 0-2 Months | ret_2_0 | RI*t - 1 RI* t-2 |
| Momentum 0-3 Months | ret_3_0 | RI* t - 1 RI* t-3 |
| Momentum 1-3 Months | ret_3_1 | RI* t-1 * - 1 RI t-3 |
| Momentum 0-6 Months | ret_6_0 | RI* t - 1 RI * t-6 |
| Momentum 1-6 Months | ret_6_1 | RI * t-1 * - 1 RI t-6 |
| Momentum 0-9 Months | ret_9_0 | RI * * t 1 - RI t-9 |
| Momentum 1-9 Months | ret_9_1 | RI * t-1 - 1 RI * t-9 |
| Momentum 0-12 Months | ret_12_0 | RI* t 1 - RI* t-12 |
| Momentum 1-12 Months | ret_12_1 | RI* t-1 - 1 RI* t-12 |
| Momentum 7-12 Months | ret_12_7 | RI * t-7 - 1 RI* t-12 |
| Momentum 1-18 Months | ret_18_1 | RI * t- 1 - 1 RI * t- 18 |
| Momentum 1-24 Months | ret_24_1 | RI t-1 - 1 RI * t-24 |
| Momentum 12-24 Months | ret_24_12 | RI * t-12 - 1 RI * t-24 |
| Momentum 1-36 Months | ret_36_1 | RI * t-1 - 1 RI * t-36 |
| Momentum 12-36 Months | ret_36_12 | RI * t-12 - 1 RI* t-36 |
| Momentum 1-48 Months | ret_48_1 | RI * t-1 - 1 RI* t-48 |
| Momentum 12-48 Months | ret_48_12 | RI * t-12 - 1 RI* t-48 |
| Momentum 1-60 Months | ret_60_1 | RI * t-1 - 1 RI* t-60 |
| Momentum 12-60 Months | ret_60_12 | RI * t-12 - 1 RI * t-60 |
| Momentum 36-60 Months | ret_60_36 | RI* t-36 - 1 RI* t- 60 |
| Seasonality | Seasonality | Seasonality |
| 1 Year Annual Seasonality | seas_ 1_lan | Return in month t-12 |
| 2 - 5 Year Annual Seasonality | seas_2_5an | Average return over annual lags from year t-2 to t-5 |
| 6 - 10 Year Annual Seasonality | seas_6_10an | Average return over annual lags from year t-6 to t-10 |
| 11 - 15 Year Annual Seasonality | seas_ 11_15an | Average return over annual lags from year t-11 to t-15 |
| 16 - 20 Year Annual Seasonality | seas_16_20an | Average return over annual lags from year t-16 to t-20) |
| 1 Year Non-Annual Seasonality | seas_ 1 1na | Average return from month t-1 to t-11 |
| 2 - 5 Year Non-Annual Seasonality | seas_2_5na | Average return over non-annual lags from year t-2 to t-5 |
| 6 - 10 Year Non-Annual Seasonality | seas_6_10na | Average return over non-annual lags from year t-6 to t-10 |
| 11 - 15 Year Non-Annual Seasonality | seas_ 11_15na | Average return over non-annual lags from year t-11 to t-15 |
| 16 - 20 Year Non-Annual Seasonality | seas_16_20na | Average return over non-annual lags from year t-16 to t-20 |


28

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Combined Accounting and Market Based Characteristics | Combined Accounting and Market Based Characteristics | Combined Accounting and Market Based Characteristics |
| Let et be defined as described here | Let et be defined as described here | Let et be defined as described here |
| 60 Month CAPM Beta Performance Based Mispricing Management Based Mispricing Residual Momentum - 6 Month Residual Momentum - 12 Month | beta_60m mispricing_perf mispricing_mgmt resff3_6_1 resff3_12_1 | COV AR_60M (RET*t,MKTRF*t) v ARC_60M(MKTRF*t) 1 4 (O_SCORE[01 + RET_12_1501 + GP_ATT01 + NIQ-ATT01) 1 6 (CHCSHO.12M[01 + EQNPO_12M[01 + OACCRU ALS_ATT01 + NOA_ATT01+ AT-GR1-01 + PPEINV _GR1A(01) -1 + IIn=1 1 + et-n -1 + IIn=1 1 + et-n |
| Daily Market Data 10 | Daily Market Data 10 | Daily Market Data 10 |
| Let Et be defined as described here | Let Et be defined as described here | Let Et be defined as described here |
| Return Volatility | rvol_zd | ⌀2D(RET_EXC*t) |
| Maximum Return | rmaxl _zd | MAX1_zD(RET*t) |
| Mean Maximum Return | rmax5_zd | 15 En=1 Xn, Xn E MAX5_zD(RET*) |
| Return Skewness | rskew zd | SKEW zD(RET_EXC*t) |
| Price-to-High | prc_highprc_zd | PRC ADJ*t MAX1_zD(P RC_ADJ*t) |
| Amihud (2002) Measure | ami_zd | |RET*t| * 1000000 DOLVOL*t zD |
| CAPM Beta | beta_zd | Described in detail here |
| CAPM Idiosyncratic Vol. | ivol_capm_zd | Described in detail here |
| CAPM Skewness | iskew _capm_zd | Described in detail here |
| Coskewness | coskew. zd11 | (etxMKTRF_DM2) zD V (약)2Dx(MKTRF_DM2)2D |
| Fama and French Idiosyncratic Vol. | ivol_ff3_zd | Described in detail here |
| Fama and French Skewness | iskew. _ff3_zd | Described in detail here |
| Hou, Xue and Zhang Idiosyncratic Vol. | ivol_hxz4_zd | Described in detail here |
| Hou, Xue and Zhang Skewness | iskew _hxz4_zd | Described in detail here |
| Dimson Beta | beta_dimson_zd | Created as described in Dimson (1979) |
| Downside Beta | betadown_zd | Described in detail here |


9A rank characteristic has the value of that characteristics rank with respect to other companies' same
characteristic of the same month and country scaled [0, 1]. This is identified with a "r01" superscript.
10Many of the variables in this section are estimated using rolling windows of data, and the variables are
estimated using a variety of window lengths: 21, 126, 252 and 1260 days. In this section, I refer to the
number of days as m as a proxy for any of the possible window lengths.
11 MKTRF _DMt = MKTRF*t - MKTRF* tzD

29

| Name | Abbreviation | Construction |
| --- | --- | --- |
| Zero Trades | zero_trades_zd | Number of days with zero trades over period. In case of equal number of zero trading days, turnover_zd will decide on the rank following Liu (2006) |
| Turnover | turnover_zd | TVOL*t SHARES*1*1000000 zD |
| Turnover Volatility | turnover_var _zd | ⌀zD ((TVOL*t/SHARES*t)*1000000) TURNOVER_zDt |
| Dollar Volume | dolvol_zd | DOLVOL*tzD |
| Dollar Volume Volatility | dolvol_var_zd | �zD(DOLVOL*t) DOLVOL_=Dt |
| Correlation to Market | corr_zd | The correlation between RET_EXC*3l = RET_EXC*t + RET_EXC*t-1 + RET_EXC*t-2 and MKT_EXC_3l = MKTRF*t + MKTRF*t-1 + MKTRF*t-2 |
| Betting Against Beta | betabab_1260d | CORR_1260dt x RVOL_252dt _MKTVOL_252d*t |
| Max Return to Volatility | rmax5_rvol_21d | RMAX5_21dt RV OL_252dt |
| 21 Day Bid-Ask High-Low | bidaskhl_21d | High-low bid ask estimator created using code from Corwin and Schultz (2012) from |
| 21 Day Return Volatility High-Low | rvolhl_21d | High-low return volatility estimator created using code Corwin and Schultz (2012) |
| Quality Minus Junk | Quality Minus Junk | Quality Minus Junk |
| Quality Minus Junk - Profit | qmj_prof | ZV ZV(GP_ATt) + ZV(NI_BEt)+ ZV(NI-ATt) + ZV(OCF_ATt) + ZV(GP_SALE*t)+ ZV(OACCRUALS_ATt)) |
| Quality Minus Junk - Growth | qmj_growth | zv ( ZV(GPOA_CH5t) + ZV(ROE_CH5t) +ZV(ROA_CH5t) + ZV(CFOA_CH5t)+ ZV(GMAR_CH5t)) |
| Quality Minus Junk - Safety Quality Minus Junk | qmj_safety qmj | zv ( ZV(BETABAB_1260dt) + ZV(DEBT_ATt) +ZV(O_SCOREt) + ZV(Z_SCOREt) + ZV(_EVOLt)) QMJ_PROFt+QMJ_GROWTHt+QMJ_SAFETY 3 |


8 Detailed Characteristic Construction

This section includes detailed descriptions how we built characteristics that don't easily fit
into the Accounting Characteristics or Market Characteristics tables.

# ● Equity Duration

- Define the following variables:

- * horizon: number of months used to estimate helper variables
- * r: constant used as assumed discount rate
- * roe_mean: constant used as the average ROE value


30

- * roe_arl: constant used as the expected growth rate of ROE
- * g_mean: constant used as the average sales growth rate
- * g_arl: constant used as the expected growth rate of sales


- Create initial variables:

$$-^{r o e0}=\frac{\displaystyle N I^{\star}_{t}}{\displaystyle B E^{\star}_{t-12}^{\star}}$$

* If the number of non-missing observations is less than or equal to 12 or the
variables' respective denominators are less than or equal to 1 _roe0t and -g0t
are set to missing.

- Forecast cash distributions

$$\begin{array}{l}{{\sqrt[[object Object]]{a}}}\\ {{\frac{\pi}{a{\sqrt[[object Object]]{a}}}}}\\ {{\frac{\pi}{a{\sqrt[[object Object]]{a}}}}}\end{array}$$

- Create duration helper variables 12

$$e d_{-}c o n s t a n t=h o r^{\cdot}i z o n+\frac{1+r}{r}$$

$$e d_{-}c w_{-}w_{t}=\sum_{i=1}^{h o r t z o n}e d_{-}c d_{-}w_{i-1}+i\times\frac{-c d_{t}}{(1+r)^{i}}$$

$$e d_{-}c d_{t}=\sum_{i=1}^{h o r t z o n}e d_{-}c d_{i-1}+{\frac{-c d_{t}}{(1+r)^{i}}}$$

- Characteristic:

$$v q\,d u r_{t}={\frac{e d.c d.w_{t}\times F X_{t}}{M E.C O M P A N Y_{t}}}+e d.c o n s t a n t{\times}{\frac{M E.C O M P A N Y_{t}-e d.c d_{t}\times F X_{t}}{M E.C O M P A N Y_{t}}}$$

12ed_cw_w, ed_cd and ed_err are equal to 0 at i = 1. ed_cw_w and ed_cd recusrively build upon themselves
over the length of the horiozon, so ed_cw_wi-1, for example, would be the previous iteration of ed_cw_w

31

# ● Piotroski F-Score

- Create helper variables:

$$\scriptstyle{\frac{\mathrm{d}_{t t}^{2}}{\mathrm{d}t_{t}^{2}}}{\mathrm{d}}}$$

* For all variables except _f_acc, _f_aturn _f_eqis, if the count of available
observations is less than or equal to 12, then the variable is set to missing.
If _f_aturn has less than or equal to 24 non-missing observations, it is set
to missing. If a variable has AT*t or AT*t-12 as an input and AT*t ≤ 0 or
AT*t-12 ≤ 0, then it is set to missing. If CL*t ≤ 0 or CL*t-12 ≤ 0 then
_f_liqt is set to missing. If SALE*t ≤ 0 or SALE*t-12 ≤ 0 then -f_gmt is
set to missing.

- Characteristic13

$$\begin{array}{c}{{f_{-S C O T e_{t}}=_{-}f_{-}F o a_{>0,t}+_{-}f_{-}C r o a_{>0,t}+_{-}f_{-}d r o a_{>0,t}+_{-}f_{-}d r o a_{>0,t}+_{-}f_{-}a t u r n_{>0,t}}}\\ {{-f_{-}t e v_{<0,t}+_{-}f_{-}d r s_{0,t}+_{-}f_{-}g m_{>0,t}+_{-}f_{-}d t s_{=0,t}+_{-}f_{-}a t u r n_{>0,t}}}\end{array}$$

# ● Ohlson O-Score

13A subscript of > 0, ex: V ARt>0,t, is a dummy for if the variable is greater than zero, and it is defined
similarly for V ARt <0,t or any other specification. Otherwise, not included as an input, Also, if any variables
other than _f_eqist are missing, then f_scoret is set to missing.

32

# - Create helper variables:

$$\begin{array}{l}{{\frac{a b}{a{\frac{b}{b}}}}}\\ {{\frac{a^{\frac{1}{b}}}{b}}}\\ {{\frac{a^{\frac{1}{b}}}{b}}}\\ {{\frac{a^{\frac{1}{b}}}{b}}}\\ {{\frac{a^{\frac{1}{b}}}{b}}}\\ {{\frac{a^{\frac{1}{b}}}{b}}}\\ {{a^{\frac{b}{b}}}}\\ {{\frac{a^{\frac{b}{b}}}{b}}}\end{array}$$

* If AT*t ≤ 0, then _o_latt, _o_levt, _O_WCt, and _o_roet are set to missing. If
CA*t ≤ 0 then _o_caclt is set to missing. If LTT ≤ 0 then _o_ffot is set to
missing. If LTt or AT*t are missing, then _o_neg_eqt is set to missing. If there
are less than or equal to 12 observations or either of NIX*t and NIX* t-12
are missing, then _o_nicht and _o_neg_earnt are set to missing.

- Characteristic:

o_scoret =- 1.37 - 0.407 x _o_latt + 6.03 x _o_levt + 1.43 x _o_wct+
0.076 x _o_caclt - 1.72 x _o_neg_eqt - 2.37 x _⌀_roet-
1.83 x _o_ffot + 0.285 x _o_neg_earnt - 0.52 x _o_nicht

● Altman Z-Score

- Create helper variables:

$$\begin{array}{r}{z.w c_{t}={\cfrac{C A^{*}t}{A T^{*}t}}}\\ {z.r e_{t}={\cfrac{R E_{t}}{A T^{*}t}}}\\ {z.e b_{t}={\cfrac{E B I T D A^{*}t}{A T^{*}t}}}\\ {z.e b_{t}={\cfrac{A E L^{*}t}{B T^{*}t}}}\end{array}$$

33

* If AT*t ≤ 0 then any variable including AT*t, then it is set to missing. If
LTt ≤ 0, then _z_met is set to missing.

- Characteristic:

z_scoret = 1.2x _z_wct +1.4x _z_ret+3.3x _z_ebt + 0.6 x _z_met +1.0x _z_sat

# ● Kaplan-Zingales Index

- Create helper variables:

$$\begin{array}{l}{{k z.c f_{t}={\frac{N^{\prime}t+D P_{t}}{P P E N T_{t-1}}}{I P E M^{*}t+B E Q^{*}t}}}\\ {{k z.d b_{t}={\frac{M T^{*}t+M E E H S C A L_{t}}{P P E M T_{t-1}}}}}\\ {{k z.d b_{t}={\frac{D E M^{*}t}{P P E M T_{t}^{*}t}}}}\end{array}$$

* If the number of non-missing observations is less than or equal to 12, then
_kz_cft, _kz_dvt and _kz_cst are set to zero. If PPENTt-12 ≤ 0 then _kz_cft,
_kz_dvt and _kz_cst are set to missing. If AT*t ≤ 0 then _kz-qt is set to
missing. If (DEBT*t+ SEQ*t) = 0 then _kz_dbt is set to missing.

- Characteristic:

kz_index = -1.002x_kz_cft+0.283x_kz_ge+3.139x_kz_dbt-39.368x_kz_dot-1.315x_kz_cst

● Intrinsic Value from Frankel and Lee

- - Define r as a constant assumed discount rate
- - Create helper variables:


$$\begin{array}{l}{{\displaystyle\lbrack\left.\right.\left.\cfrac\right.\star\right.\D\displaystyle\left(\begin{array}{c}{\displaystyle\left.\frac{\displaystyle\displaystyle\vphantom{\cal D}\displaystyle\vphantom{\cal1}\vphantom{\wedge}_{\it t}}^{\star}}\\ {\displaystyle\vphantom{\left.\nabla\vphantom2}\vphantom3\left(\vphantom{\cal B}\vphantom{E}^{\wedge\vphantom t}\vphantom{\left.\vphantom2}\vphantom{\left.\left.\vphantom3\right)\vphantom2}}{\displaystyle\left(\vphantom{\cal D}\vphantom{\Delta}^{\star\vphantom2}\vphantom{\cal A}\vphantom{\left.\vphantom2\right)\vphantom2}\vphantom2\right)\vphantom2\right.\vphantom2\vphantom{\cal B}\vphantom{\cal E}^{\wedge\vphantom2\bot}\vphantom{\left/\vphantom2\right.\vphantom2\right.\vphantom2}\vphantom2\right)\vphantom2\vphantom2\vphantom2\vphantom{\cal D}\vphantom{\cal F}\vphantom2\vphantom2\vphantom2\right)\vphantom2\right)\bot}}}\end{array}\right)}}\end{array}$$

* If NIX*t ≤ 0 then

$$-i v_{-}p o_{t}=\frac{{\cal D}/V^{\times}_{t}}{A T^{\star}{_{t}}\times0.06}$$

* If the number of non-missing observations is less than or equal to 12 or
(BE*t+ BE*t-12) ≤ 0 then _iv_roet is set to missing.

34

- Characteristics:

$$i n t r i n s i c_{-}v a l u e_{t}=B E^{\star}{}_{t}+{\frac{\textstyle{\frac{\cdot}{\textstyle{v}}{\textstyle{v}}{\cdot}r{\textstyle{v}}}}{\textstyle{1+r}}}\times B E^{\star}{}_{t}+{\frac{\textstyle{\frac{\cdot}{\textstyle{v}}}{\textstyle{v}}\cdot{\mathit{r}}}}\times\cdots\star_{-}b e{\textstyle{1_{t}}}$$

* If intrinsic_valuet ≤ 0 then it is set to missing.

● Net Income Idiosyncratic Volatility

# - Define the following variable 14:

$$n i_{-}a t_{t}=\frac{N{I^{\star}}_{t}}{A T^{\star}t}$$

- A rolling regression of the following form is run for each company, with the time
series split up into n groups:

$$-n i_{-}a t_{t}=\beta_{0}+\beta_{1.}n i_{-}a t_{t-12}+u_{t}$$

where edft = the error degrees of freedom of regression and rmset = root mean
square error of the regression.

- Characteristic:

$$n i_{-}i v o l_{t}=\sqrt{\frac{r m s e_{t}^{2}\times e d f_{t}}{e d f_{t}+1}}$$

● Beta, Idiosyncratic Volatility and Skewness of Asset Pricing Factor Regressions

- This section describes the construction of beta_zd for the CAPM model, and the
idiosyncratic volatility and skewness characteristics, which are estimated using
three different factor models:

* CAPM (capm):

RET_EXC*t = Bo + �1M KTRF*t + Et

* Fama-French 3 Factor Model (ff3):

RET_EXC*t = Bo + �1M KTRF*t + �2HML*t + �3SMB_FF*t + et
* Hou, Xue and Zhang 4 Factor Model (hxz4):

RET_EXC*t = �0+�1MKTRF*t+ �2SM B _HXZ*t+ �3ROE*t+ �INV*t++�t

14If AT*t ≤ 0, then _ni_att is set to missing

35

- Characteristics 15.

beta_zd = �1 from the CAPM model

ivol_capm_zdt = �zD(�t)

ivol_ff3_zdt = �zD(et)

ivol_hxz4_zdt = �zD(�t)

iskew_capm_zdt = SKEW _zD(�t)

iskew-ff3-zdt = SKEW _zD(et)

iskew_hxz4_zdt = SKEW _zD(�t)

● Downside Beta

- Define the following regression model run over z days:

RET_EXC*t = Bo + �1MKTRF*t + Et

However, we restrict the data to when M KTRF* is negative.

- Characteristic:

* betadown_zd = �1

# 9 FX Conversion Rate Construction

This section outlines how we create a daily dataset, beginning 01/01 /1950 to now, of X
currency - USD exchange rate using COMPUSTAT. This is run in the macro compustat_fx()
in the project_macros.sas file.

- ● We use COMP.EXRT_DLY, which has daily conversion rates from GBP to other cur-
- rencies 'X'.


- ● Every day available, we estimate the exchange rate fxt as


$$f x_{t}=\frac{U S D_{G B P,t}}{X_{G B P,t}}$$

where XGBP,t is the exchange rate of GBP to currency X on day t.

● In case there are gaps in information, we assume the exchange rate of the last obser-
vation until a new observation is available.

- Xt USD, do Xt x fxt
- ● fxt is quoted as SO to go from X to
- USDt ,


15 之 indicates over how many days the model is run.

36

# 10 Factor Details and Citations

Table 9: Factor and Cluster Details

|  | Variable Name | Citation | Orig. Sample | Sign | Orig. Signif. |
| --- | --- | --- | --- | --- | --- |
| Description Accruals | Description Accruals | Description Accruals | Description Accruals | Description Accruals | Description Accruals |
| Change in current operating work- ing capital | cowc_grla | Richardson, Sloan, Soliman, and Tuna (2005) | 1962-2001 | -1 | 1 |
| Operating accruals | oaccruals_at | Sloan (1996) | 1962-1991 | -1 | 1 |
| Percent operating accruals | oaccruals_ni | Hafzalla, Lundholm, and Matthew Van Winkle (2011) | 1989-2008 | -1 | 1 |
| Years 16-20 lagged returns, nonan- nual | seas. _16_20na | Heston and Sadka (2008) | 1965-2002 | 1 | 1 |
| Total accruals | taccruals_at | Richardson et al. (2005) | 1962-2001 | -1 | 1 |
| Percent total accruals | taccruals_ni | Hafzalla et al. (2011) | 1989-2008 | -1 | 1 |
| Debt Issuance | Debt Issuance | Debt Issuance | Debt Issuance | Debt Issuance | Debt Issuance |
| Abnormal corporate investment | capex_abn |  |  |  |  |
| Growth in book debt (3 years) | debt_gr3 |  |  |  |  |
| Change in financial liabilities | fnl_grla |  |  |  |  |
| Change in noncurrent operating li- abilities | ncol_grla | <table><thead></thead><tbody><tr><td>Titman, Wei, and Xie (2004)</td><td>1973-1996</td><td>-1</td><td>1</td></tr><tr><td>Lyandres, Sun, and Zhang (2008)</td><td>1970-2005</td><td>-1</td><td>1</td></tr><tr><td>Richardson et al. (2005)</td><td>1962-2001</td><td>-1</td><td>1</td></tr><tr><td>Richardson et al. (2005)</td><td>1962-2001</td><td>-1</td><td>0</td></tr><tr><td>Richardson et al. (2005)</td><td>1962-2001</td><td>1</td><td>1</td></tr><tr><td>Francis, LaFond, Olsson, and Schipper (2004)</td><td>1975-2001</td><td>1</td><td>0</td></tr><tr><td>Hirshleifer, Hou, Te⌀h, and Zhang (2004)</td><td>1964-2002</td><td>-1</td><td>1</td></tr></tbody></table> |  |  |  |
| Change in net financial assets | nfna_grla |  |  |  |  |
| Earnings persistence | ni_arl |  |  |  |  |
| Net operating assets | noa_at |  |  |  |  |
| Investment | Investment | Investment | Investment | Investment | Investment |
| Liquidity of book assets | aliq_at | Ortiz-Molina and Phillips (2014) | 1984-2006 | -1 | 0 |
| Asset Growth | at_grl | Cooper, Gulen, and Schill (2008) | 1968-2003 | -1 | 1 |
| Change in common equity | be_grla | Richardson et al. (2005) | 1962-2001 | -1 | 1 |
| CAPEX growth (1 year) | capx_grl | Xie (2001) | 1971-1992 | -1 | 0 |
| CAPEX growth (2 years) | capx_gr2 | Anderson and Garcia-Feijoo (2006) | 1976-1998 | -1 | 1 |
| CAPEX growth (3 years) | capx_gr3 | Anderson and Garcia-Feijoo (2006) | 1976-1998 | -1 | 1 |
| Change in current operating assets | coa_grla | Richardson et al. (2005) | 1962-2001 | -1 | 1 |
| Change in current operating liabil- ities | col_grla | Richardson et al. (2005) | 1962-2001 | -1 | 1 |
| Hiring rate | emp_gr1 | Belo, Lin, and Bazdresch (2014) | 1965-2010 | -1 | 1 |
| Inventory growth | inv_grl | Belo and Lin (2012) | 1965-2009 | -1 | 1 |
| Inventory change | inv_grla | J. K. Thomas and Zhang (2002) | 1970-1997 | -1 | 1 |
| Change in long-term net operating assets | lnoa_grla | Fairfield, Whisenant, and Yohn (2003) | 1964-1993 | -1 | 1 |
| Mispricing factor: Management | mispricing_mgmtStambaugh | and Yuan (2017) | 1967-2013 | 1 | 1 |
| Change in noncurrent operating as- sets | ncoa_grla | Richardson et al. (2005) | 1962-2001 | -1 | 1 |
| Change in net noncurrent operating assets | nncoa_grla | Richardson et al. (2005) | 1962-2001 | -1 | 1 |
| Change in net operating assets | noa_grla | Hirshleifer et al. (2004) | 1964-2002 | -1 | 1 |
| Change PPE and Inventory | ppeinv_grla | Lyandres et al. (2008) | 1970-2005 | -1 | 1 |
| Long-term reversal | ret_60_12 | De Bondt and Thaler (1985) | 1926-1982 | -1 | 1 |


37

|  |  | <table><thead></thead><tbody><tr><td>Sales Growth (1 year)</td><td>sale_gr1</td><td>Lakonishok, Shleifer, and Vishny (1994)</td><td>1968-1989</td><td>-1</td><td>1</td></tr><tr><td>Sales Growth (3 years)</td><td>sale_gr3</td><td>Lakonishok et al. (1994)</td><td>1968-1989</td><td>-1</td><td>1</td></tr><tr><td>Sales growth (1 quarter)</td><td>saleq_gr1</td><td></td><td>1967-2016</td><td>-1</td><td>0</td></tr><tr><td>Years 2-5 lagged returns, nonannual</td><td>seas_2_5na</td><td>Heston and Sadka (2008)</td><td>1965-2002</td><td>-1</td><td>1</td></tr></tbody></table> |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
| <table><thead></thead><tbody><tr><td colspan="6">Low Leverage</td></tr><tr><td>Firm age</td><td>age</td><td>Jiang, Lee, and Zhang (2005)</td><td>1965-2001</td><td>-1</td><td>1</td></tr><tr><td>Liquidity of market assets</td><td>aliq_mat</td><td>Ortiz-Molina and Phillips (2014)</td><td>1984-2006</td><td>-1</td><td>0</td></tr><tr><td>Book leverage</td><td>at_be</td><td>Fama and French (1992)</td><td>1963-1990</td><td>-1</td><td>0</td></tr><tr><td>The high-low bid-ask spread</td><td>bidaskhl_21d</td><td>Corwin and Schultz (2012)</td><td>1927-2006</td><td>1</td><td>1</td></tr><tr><td>Cash-to-assets</td><td>cash_at</td><td>Palazzo (2012)</td><td>1972-2009</td><td>1</td><td>0</td></tr><tr><td>Net debt-to-price</td><td>netdebt_me</td><td>Penman, Richardson, and Tuna (2007)</td><td>1962-2001</td><td>-1</td><td>1</td></tr><tr><td>Earnings volatility</td><td>ni_ivol</td><td>Francis et al. (2004)</td><td>1975-2001</td><td>1</td><td>0</td></tr><tr><td>R&D-to-sales</td><td>rd_sale</td><td>Chan, Lakonishok, and Sougiannis (2001)</td><td>1975-1995</td><td>1</td><td>0</td></tr><tr><td>R&D capital-to-book assets</td><td>rd5_at</td><td>Li (2011)</td><td>1952-2004</td><td>1</td><td>0</td></tr><tr><td>Asset tangibility</td><td>tangibility</td><td>Hahn and Lee (2009)</td><td>1973-2001</td><td>1</td><td>0</td></tr><tr><td>Altman Z-score</td><td>z_score</td><td>Dichev (1998)</td><td>1981-1995</td><td>1</td><td>1</td></tr></tbody></table> Low Risk |  |  |  |  |  |
| Market Beta |  |  | 1935-1968 | -1 | 1 |
|  | beta_60m beta_dimson_21d | Fama and MacBeth (1973) |  |  |  |
| Dimson beta |  | Dimson (1979) | 1955-1974 | -1 | 0 |
| Frazzini-Pedersen market beta Downside beta | betabab_1260d betadown_252d | Frazzini and Pedersen (2014) Ang, Chen, and Xing (2006) | 1926-2012 1963-2001 | -1 | 1 |
| Earnings variability |  | et al. (2004) |  | -1 | 1 0 |
| Idiosyncratic volatility from the CAPM (21 days) | earnings_variabilifyrancis ivol_capm_21d |  | 1975-2001 1967-2016 | -1 -1 | 0 |
| the | ivol_capm_252d | Ali, Hwang, and Trombley (2003) | 1976-1997 | -1 | 1 |
| Idiosyncratic volatility from CAPM (252 days) |  |  | 1963-2000 | -1 | 1 |
| Idiosyncratic volatility from the Fama-French 3-factor model | ivol_ff3_21d | Ang, Hodrick, Xing, and Zhang (2006) | 1967-2016 | -1 | 0 |
| Idiosyncratic volatility from the q- factor model Cash flow volatility | ivol_hxz4_21d ocfq_saleq_std | Huang (2009) | 1980-2004 | -1 | 1 |
| Maximum daily return | rmax1_21d | Bali, Cakici, and Whitelaw (2011) | 1962-2005 | -1 | 1 |
| Highest 5 days of return | rmax5_21d | Bali, Brown, and Tang (2017) | 1993-2012 | -1 | 1 |
| Return volatility | rvol_21d | Ang, Hodrick, et al. (2006) | 1963-2000 | -1 | 1 |
| Years 6-10 lagged returns, nonan- nual | seas_6_10na | Heston and Sadka (2008) | 1965-2002 | -1 | 1 |
| Share turnover | turnover_126d | Datar, Naik, and Radcliffe (1998) | 1963-1991 | -1 | 1 |
| Number of zero trades with turnover as tiebreaker (1 month) | zero_trades_21d | Liu (2006) | 1963-2003 | 1 | 0 |
| Number of zero trades with turnover as tiebreaker (6 months) | zero_trades_126d zero_trades_252d | Liu (2006) Liu (2006) | 1963-2003 | 1 | 1 |
| Number of zero trades with turnover as tiebreaker (12 months) |  |  | 1963-2003 | 1 | 1 |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
| Momentum |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  | <table><thead></thead><tbody><tr><td>Current price to high price over last year</td><td></td><td>prc_highprc_252dGeorge and Hwang (2004)</td><td>1963-2001</td><td>1</td><td>1</td></tr><tr><td>Residual momentum t-6 to t-1</td><td>resff3_6_1</td><td>Blitz, Huij, and Martens (2011)</td><td>1930-2009</td><td>1</td><td>1</td></tr><tr><td>Residual momentum t-12 to t-1</td><td>resff3_12_1</td><td>Blitz et al. (2011)</td><td>1930-2009</td><td>1</td><td>1</td></tr></tbody></table> |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |


38

| Price momentum t-3 to t-1 |  |  |  |  | 1 |
| --- | --- | --- | --- | --- | --- |
| Price momentum t-6 to t-1 |  |  |  |  | 1 |
| Price momentum t-9 to t-1 |  | <table><thead></thead><tbody><tr><td>ret_3_1</td><td>Jegadeesh and Titman (1993)</td><td>1965-1989</td><td>1</td></tr><tr><td>ret_6_1</td><td>Jegadeesh and Titman (1993)</td><td>1965-1989</td><td>1</td></tr><tr><td>ret_9_1</td><td>Jegadeesh and Titman (1993)</td><td>1965-1989</td><td>1</td></tr><tr><td>ret_12_1</td><td>Jegadeesh and Titman (1993)</td><td>1965-1989</td><td>1</td></tr><tr><td>seas_l 1na</td><td>Heston and Sadka (2008)</td><td>1965-2002</td><td>1</td></tr></tbody></table> |  |  | 1 |
| Price momentum t-12 to t-1 |  |  |  |  | 1 |
| Year 1-lagged return, nonannual |  |  |  |  | 1 |
| Change sales minus change Inven- | dsale_dinv |  |  |  |  |
| tory Change sales minus change receiv- ables | dsale_drec |  |  |  |  |
| Change sales minus change SG&A | dsale_dsga |  |  |  |  |
| Change in quarterly return on as- sets | niq_at_chg1 |  |  |  |  |
| Change in quarterly return on eq- uity | niq_be_chg1 | <table><thead></thead><tbody><tr><td colspan="4">Profit Growth</td></tr><tr><td>Abarbanell</td><td>and Bushee (1998) 1974-1988</td><td>1</td><td>1</td></tr><tr><td>Abarbanell</td><td>and Bushee (1998) 1974-1988</td><td>-1</td><td>0</td></tr><tr><td>Abarbanell (1998)</td><td>and Bushee 1974-1988</td><td>1</td><td>0</td></tr><tr><td></td><td>1972-2016</td><td>1</td><td>0</td></tr><tr><td></td><td>1967-2016</td><td>1</td><td>0</td></tr><tr><td></td><td>Foster, Olsen, and Shevlin (1984) 1974-1981</td><td>1</td><td>1</td></tr><tr><td>Bouchaud, Landier,</td><td>Krueger, and 1990-2015 Thesmar (2019)</td><td>1</td><td>1</td></tr><tr><td>Novy-Marx (2012)</td><td>1925-2010</td><td>1</td><td>1</td></tr><tr><td>Abarbanell and Bushee (1998)</td><td>1974-1988</td><td>1</td><td>0</td></tr><tr><td>Jegadeesh</td><td>and Livnat (2006) 1987-2003</td><td>1</td><td>1</td></tr><tr><td></td><td>Heston and Sadka (2008) 1965-2002</td><td>1</td><td>1</td></tr><tr><td></td><td>J. Thomas and Zhang (2011) 1977-2006</td><td>1</td><td>1</td></tr></tbody></table> |  |  |  |
| Standardized earnings surprise | niq_su |  |  |  |  |
| Change in operating cash flow to as- sets | ocf_at_chg1 |  |  |  |  |
| Price momentum t-12 to t-7 | ret_12_7 |  |  |  |  |
| Labor force efficiency | sale_emp_grl |  |  |  |  |
| Standardized Revenue surprise | saleq_su |  |  |  |  |
| Year 1-lagged return, annual | seas_l_lan |  |  |  |  |
| Tax expense surprise | tax_grla |  |  |  |  |
| Profitability |  |  |  |  |  |
| Coefficient of variation for dollar trading volume | dolvol_var_126d | Chordia, Subrahmanyam, and An- shuman (2001) | 1966-1995 | -1 | 1 |
| Return on net operating assets | ebit_bev | Soliman (2008) | 1984-2002 | 1 | 1 |
| Profit margin | ebit_sale | Soliman (2008) | 1984-2002 | 1 | 1 |
| Pitroski F-score | f_score | Piotroski (2000) | 1976-1996 | 1 | 1 |
| Return on equity | ni_be | Haugen and Baker (1996) | 1979-1993 | 1 | 1 |
| Quarterly return on equity | niq_be | Hou, Xue, and Zhang (2015) | 1972-2012 | 1 | 1 |
| Ohlson O-score | o_score | Dichev (1998) | 1981-1995 | -1 | 1 |
| Operating cash flow to assets | ocf_at | Bouchaud et al. (2019) | 1990-2015 | 1 | 1 |
| Operating profits-to-book equity | ope_be | Fama and French (2015) | 1963-2013 | 1 | 1 |
| Operating profits-to-lagged book equity | ope_bell |  | 1967-2016 | 1 | 0 |
| Coefficient of variation for share turnover | turnover_var_126Chordia | et al. (2001) | 1966-1995 | -1 |  |
|  |  |  |  |  | 1 |
|  | <table><thead></thead><tbody><tr><td>Capital turnover</td><td>at_turnover</td><td>Haugen and Baker (1996)</td><td>1979-1993</td><td>1</td><td>0</td></tr><tr><td>Cash-based operating profits-to- book assets</td><td>cop_at</td><td></td><td>1967-2016</td><td>1</td><td>0</td></tr><tr><td>Cash-based operating profits-to- lagged book assets</td><td>cop_atll</td><td>Ball, Gerakos, Linnainmaa, and Nikolaev (2016)</td><td>1963-2014</td><td>1</td><td>1</td></tr><tr><td>Change gross margin minus change sales</td><td>dgp_dsale</td><td>Abarbanell and Bushee (1998)</td><td>1974-1988</td><td>1</td><td>0</td></tr><tr><td>Gross profits-to-assets</td><td>gp-at</td><td>Novy-Marx (2013)</td><td>1963-2010</td><td>1</td><td>1</td></tr><tr><td>Gross profits-to-lagged assets</td><td>gp_atl1</td><td></td><td>1967-2016</td><td>1</td><td>0</td></tr><tr><td>Mispricing factor: Performance</td><td>mispricing_perf</td><td>Stambaugh and Yuan (2017)</td><td>1967-2013</td><td>1</td><td>1</td></tr><tr><td>Number of consecutive quarters with earnings increases</td><td>ni_inc8q</td><td>Barth, Elliott, and Finn (1999)</td><td>1982-1992</td><td>1</td><td>0</td></tr></tbody></table> | Quality |  |  |  |


39

| Quarterly return on assets | niq_at |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Operating profits-to-book assets | op_at |  |  |  |  |
| Operating profits-to-lagged book assets | op_atll |  |  |  |  |
| Operating leverage | opex_at | <table><thead></thead><tbody><tr><td>Balakrishnan, Bartov, and Faurel (2010)</td><td>1976-2005</td><td>1</td><td>1</td></tr><tr><td></td><td>1963-2013</td><td>1</td><td>1</td></tr><tr><td>Ball et al. (2016)</td><td>1963-2014</td><td>1</td><td>1</td></tr><tr><td>Novy-Marx (2011)</td><td>1963-2008</td><td>1</td><td>1</td></tr><tr><td>C. S. Asness, Frazzini, and Peder- sen (2019)</td><td>1957-2016</td><td>1</td><td>1</td></tr><tr><td>C. S. Asness et al. (2019)</td><td>1957-2016</td><td>1</td><td>1</td></tr><tr><td>C. S. Asness et al. (2019)</td><td>1957-2016</td><td>1</td><td>1</td></tr><tr><td>C. S. Asness et al. (2019)</td><td>1957-2016</td><td>1</td><td>1</td></tr><tr><td>Soliman (2008)</td><td>1984-2002</td><td>1</td><td>1</td></tr></tbody></table> |  |  |  |
| Quality minus Junk: Composite | qmj |  |  |  |  |
| Quality minus Junk: Growth | qmj_growth |  |  |  |  |
| Quality minus Junk: Profitability | qmj_prof |  |  |  |  |
| Quality minus Junk: Safety | qmj_safety |  |  |  |  |
| Assets turnover | sale_bev |  |  |  |  |
| Seasonality | Seasonality | Seasonality | Seasonality | Seasonality | Seasonality |
| Market correlation | corr_1260d |  |  |  |  |
| Coskewness | coskew_21d |  |  |  |  |
| Net debt issuance | dbnetis_at |  |  |  |  |
| Kaplan-Zingales index | kz_index |  |  |  |  |
| Change in long-term investments | lti_grla | <table><thead></thead><tbody><tr><td></td><td>C. Asness, Frazzini, Gormsen, and Pedersen (2020)</td><td>1925-2015</td><td>-1</td><td>1</td></tr><tr><td></td><td>Harvey and Siddique (2000)</td><td>1963-1993</td><td>-1</td><td>1</td></tr><tr><td></td><td>Bradshaw, Richardson, and Sloan (2006)</td><td>1971-2000</td><td>-1</td><td>1</td></tr><tr><td></td><td>Lamont, Polk, and Saa�-Requejo (2001)</td><td>1968-1995</td><td>1</td><td>1</td></tr><tr><td></td><td>Richardson et al. (2005)</td><td>1962-2001</td><td>-1</td><td>1</td></tr><tr><td></td><td>Lev and Nissim (2004)</td><td>1973-2000</td><td>1</td><td>1</td></tr><tr><td></td><td>Heston and Sadka (2008)</td><td>1965-2002</td><td>1</td><td>1</td></tr><tr><td></td><td>Heston and Sadka (2008)</td><td>1965-2002</td><td>1</td><td>1</td></tr><tr><td></td><td>Heston and Sadka (2008)</td><td>1965-2002</td><td>1</td><td>1</td></tr><tr><td></td><td>Heston and Sadka (2008)</td><td>1965-2002</td><td>-1</td><td>0</td></tr><tr><td></td><td>Heston and Sadka (2008)</td><td>1965-2002</td><td>-1</td><td>1</td></tr><tr><td></td><td>Richardson et al. (2005)</td><td>1962-2001</td><td>1</td><td>0</td></tr></tbody></table> |  |  |  |
| Taxable income-to-book income | pi_nix |  |  |  |  |
| Years 2-5 lagged returns, annual | seas_2_5an |  |  |  |  |
| Years 6-10 lagged returns, annual | seas_6_10an |  |  |  |  |
| Years 11-15 lagged returns, annual | seas_11_15an |  |  |  |  |
| Years 11-15 lagged returns, nonan- nual | seas_11_15na |  |  |  |  |
| Years 16-20 lagged returns, annual | seas_16_20an |  |  |  |  |
| Change in short-term investments | sti_grla |  |  |  |  |
| Size | Size | Size | Size | Size | Size |
| Amihud Measure |  |  |  |  |  |
| Dollar trading volume |  |  |  |  |  |
| Market Equity Price per share |  | <table><thead></thead><tbody><tr><td>ami_126d</td><td>Amihud (2002)</td><td>1964-1997</td><td>1</td><td>1</td></tr><tr><td>dolvol_126d</td><td>Brennan, Chordia, and Subrah- manyam (1998)</td><td>1966-1995</td><td>-1</td><td>1</td></tr><tr><td>market_equity</td><td>Banz (1981)</td><td>1926-1975</td><td>-1</td><td>1</td></tr><tr><td>prc</td><td>Miller and Scholes (1982)</td><td>1940-1978</td><td>-1</td><td>1</td></tr><tr><td>rd_me</td><td>Chan et al. (2001)</td><td>1975-1995</td><td>1</td><td>1</td></tr></tbody></table> |  |  |  |
|  |  |  |  |  |  |
| R&D-to-market Short-Term Reversal | R&D-to-market Short-Term Reversal | R&D-to-market Short-Term Reversal | R&D-to-market Short-Term Reversal | R&D-to-market Short-Term Reversal | R&D-to-market Short-Term Reversal |
| Idiosyncratic skewness from the CAPM | iskew_capm_21d |  | 1967-2016 | -1 | 0 |
| Idiosyncratic skewness from the Fama-French 3-factor model | iskew_ff3_21d | Bali, Engle, and Murray (2016) | 1925-2021 | -1 | 1 |
| Idiosyncratic skewness from the q- factor model | iskew_hxz4_21d |  | 1967-2016 | -1 | 0 |
| Short-term reversal | ret_1_0 | Jegadeesh (1990) | 1929-1982 | -1 | 1 |
| Highest 5 days of return scaled by volatility | rmax5_rvol_21d | C. Asness et al. (2020) | 1925-2015 | -1 | 1 |
| Total skewness | rskew_21d | Bali et al. (2016) | 1925-2021 | -1 | 1 |
| Value | Value | Value | Value | Value | Value |
| Assets-to-market | at_me | Fama and French (1992) | 1963-1990 | 1 | 0 |


40

# Book-to-market equity

# Book-to-market enterprise

Net stock issues

# Debt-to-market

Dividend yield

# Ebitda-to-market enterprise

Equity duration

Net equity issuance

Equity net payout

Net payout yield

| Payout yield | eqpo_me |
| --- | --- |
| Free cash flow-to-price | fcf_me |
| Intrinsic value-to-market | ival_me |
| Net total issuance | netis_at |
| Earnings-to-price | ni_me |
| Operating cash flow-to-market | ocf_me |


# Sales-to-market

|  | be_me | Rosenberg, Reid, and Lanstein (1985) | 1973-1984 | 1 | 1 |
| --- | --- | --- | --- | --- | --- |
| value | bev_mev | Penman et al. (2007) | 1962-2001 | 1 | 1 |
|  | chcsho.12m | Pontiff and Woodgate (2008) | 1970-2003 | -1 | 1 |
|  | debt_me | Bhandari (1988) | 1948-1979 | 1 | 1 |
|  | div12m_me | Litzenberger and Ramaswamy (1979) | 1940-1980 | 1 | 1 |
| value | ebitda_mev | Loughran and Wellman (2011) | 1963-2009 | 1 | 1 |
|  | eq_dur | Dechow, Sloan, and Soliman (2004) | 1962-1998 | -1 | 1 |
|  | eqnetis_at | Bradshaw et al. (2006) | 1971-2000 | -1 | 1 |
|  | eqnpo_12m | Daniel and Titman (2006) | 1968-2003 | 1 | 1 |
|  | eqnpo_me | Boudoukh, Michaely, Richardson, and Roberts (2007) | 1984-2003 | 1 | 1 |
|  |  | Boudoukh et al. (2007) | 1984-2003 | 1 | 1 |
|  |  | Lakonishok et al. (1994) | 1963-1990 | 1 | 1 |
|  |  | Frankel and Lee (1998) | 1975-1993 | 1 | 0 |
|  |  | Bradshaw et al. (2006) | 1971-2000 | -1 | 1 |
|  |  | Basu (1983) | 1963-1979 | 1 | 1 |
|  |  | Desai, Rajgopal, and Venkatacha- lam (2004) | 1973-1997 | 1 | 1 |
|  | sale_me | Barbee Jr, Mukherji, and Raines (1996) | 1979-1991 | 1 | 1 |


Other Factors

| Assets | assets |
| --- | --- |
| Sales | sales |
| Book Equity | book_equity |
| Net Income | net_income |
| Enterprise Value | enterprise_value |
| Current Asset Growth lyr | ca_grl |
| Non-Current Asset Growth lyr | nca_grl |
| Total Liabilities Growth lyr | lt_gr1 |
| Current Liabilities Growth lyr | cl_gr1 |
| Non-Current Liabilities Growth lyr | ncl_gr1 |
| Book Equity Growth lyr | be_gr1 |
| Preferred Stock Growth 1 yr | pstk_gr1 |
| Total Debt Growth lyr | debt_gr1 |
| Cost of Goods Sold Growth lyr | cogs_grl |
| Selling, General, and Administra- tive Expenses Growth lyr | sga_grl |
| Operating Expenses Growth lyr | opex_gr1 |
| Asset Growth 3yr | at_gr3 |
| Current Asset Growth 3yr | ca_gr3 |
| Non-Current Asset Growth 3yr | nca_gr3 |
| Total Liabilities Growth 3yr | lt_gr3 |
| Current Liabilities Growth 3yr | cl_gr3 |
| Non-Current Liabilities Growth 3yr | ncl_gr3 |
| Book Equity Growth 3yr | be_gr3 |
| Preferred Stock Growth 3yr | pstk_gr3 |
| Cost of Goods Sold Growth 3yr | cogs_gr3 |
| Selling, General, and Administra- tive Expenses Growth 3yr | sga_gr3 |
| Operating Expenses Growth 3yr | opex_gr3 |
| Gross Profit Change lyr | gp-grla |


41

| Operating Cash Flow Change lyr | ocf_grla |
| --- | --- |
| Cash and Short-Term Investments Change lyr | cash_grla |
| Receivables Change lyr | rec_grla |
| Property, Plans and Equipment Gross Change lyr | ppeg_grla |
| Intangible Assets Change lyr | intan_grla |
| Short-Term Debt Change lyr | debtst_grla |
| Accounts Payable Change lyr | ap_grla |
| Income Tax Payable Change lyr | txp_grla |
| Long-Term Debt Change lyr | debtlt_grla |
| Deferred Taxes and Investment Credit Change lyr | txditc_grla |
| Non-Current Operating Liabilities Change lyr | ncol_grla |
| Operating Assets Change lyr | oa_grla |
| Operating Liabilities Change lyr | ol_grla |
| Financial Assets Change lyr | fna_grla |
| Operating Profit before Deprecia- tion Change lyr | ebitda_grla |
| Operating Profit after Depreciation Change lyr | ebit_grla |
| Operating Earnings to Equity Change lyr | ope_grla |
| Net Income Change lyr | ni_grla |
| Depreciation and Amortization Change lyr | dp_grla |
| Free Cash Flow Change lyr Net Working Capital lyr | fcf_grla |
| Change Net Income Including Extraordi- nary Items Change lyr | nwc_grla nix_grla |
| Equity Net Issuance Change lyr | eqnetis_grla |
| Net Long-Term Debt Issuance Change lyr | dltnetis_grla |
| Net Short-Term Debt Issuance Change lyr | dstnetis_grla |
| Net Debt Issuance Change lyr Net Issuance Change 1yr | dbnetis_grla netis_grla |
|  |  |
| Financial Cash Flow Change 1yr | fincf_grla |
| Equity Net Payout Change lyr | eqnpo_grla |
| Dividend Payout Ratio Change lyr Equity Buyback Change lyr | div_grla eqbb_grla |
| Equity Issuance Change lyr | eqis_grla |
| Net Equity Payout Change lyr | eqpo_grla |
| Capital Expenditures Change lyr | capx_grla |
| Gross Profit Change 3yr | gp-gr3a |
| Operating Cash Flow Change 3yr | ocf_gr3a |
| Cash and Short-Term Investments Change 3yr |  |
|  |  |
|  |  |
|  |  |
| Inventory Change 3yr Receivables Change 3yr | cash_gr3a inv_gr3a |
|  | rec_gr3a |
|  |  |
|  |  |
| Property, Plans and Equipment Gross Change 3yr | ppeg_gr3a |


42

| Investment and Advances Change | lti_gr3a |
| --- | --- |
| 3yr | intan_gr3a |
| Intangible Assets Change 3yr | debtst_gr3a |
| Short-Term Debt Change 3yr Accounts Payable Change 3yr | ap_gr3a |
| Income Tax Payable Change 3yr | txp_gr3a |
| Long-Term Debt Change 3yr | debtlt_gr3a |
| Deferred Taxes and Investment Credit Change 3yr | txditc_gr3a |
| Current Operating Assets Change 3yr | coa_gr3a |
| Current Operating Liabilities Change 3yr | col_gr3a |
| Current Operating Working Capi- tal Change 3yr | cowc_gr3a |
| Non-Current Operating Assets Change 3yr | ncoa_gr3a |
| Net Non-Current Operating Assets Change 3yr | nncoa_gr3a |
| Operating Assets Change 3yr | oa_gr3a |
| Operating Liabilities Change 3yr | ol_gr3a |
| Net Operating Assets Change 3yr | noa_gr3a |
| Financial Assets Change 3yr | fna_gr3a |
| Financial Liabilities Change 3yr | fnl_gr3a |
| Net Financial Assets Change 3yr | nfna_gr3a |
| Operating Profit before Deprecia- tion Change 3yr | ebitda_gr3a |
| Operating Profit after Depreciation Change 3yr | ebit_gr3a |
| Operating Earnings to Equity Change 3yr | ope_gr3a |
| Net Income Change 3yr | ni_gr3a |
| Depreciation and Amortization Change 3yr | dp_gr3a |
| Free Cash Flow Change 3yr | fcf_gr3a |
| Net Working Capital Change 3yr Inventory Change lyr | nwc_gr3a inv_gr3a |
| Non-Current Operating Liabilities 3yr | ncol_gr3a |
| Change |  |
| Net Income Including Extraordi- nary Items Change 3yr | nix_gr3a |
| Equity Net Issuance Change 3yr Net Long-Term Debt Issuance Change 3yr | eqnetis_gr3a dltnetis_gr3a |
| Net Short-Term Debt Issuance Change 3yr | dstnetis_gr3a |
| Net Debt Issuance Change 3yr | dbnetis_gr3a |
| Net Issuance Change 3yr | netis_gr3a |
| Financial Cash Flow Change 3yr | fincf_gr3a |
| Net Working Capital Change 3yr Equity Net Change 3yr | nwc_gr3a |
| Payout Effective Tax Rate Change 3yr | eqnpo_gr3a tax_gr3a |
|  |  |
| Dividend Payout Ratio Change 3yr | div_gr3a |
| Equity Buyback Change 3yr | eqbb_gr3a |


43

| Equity Issuance Change 3yr | eqis_gr3a |
| --- | --- |
| Net Equity Payout Change 3yr | eqpo_gr3a |
| Capital Expenditures Change 3yr | capx_gr3a |
| Capital Expenditures scaled by As- sets | capx_at |
| R&D scaled by Assets | rd_at |
| Special Items scaled by Assets | spi_at |
| Extraordinary Items and Discontin- | xido_at |
| ued Operations scaled by Assets Non-Recurring Items scaled by As- sets | nri_at |
| Gross Profit Margin | gp_sale |
| Operating Profit Margin before De- preciation | ebitda_sale |
| Pretax Profit Margin | pi_sale |
| Net Profit Margin before extraordi- nary income | ni_sale |
| Net Profit Margin | nix_sale |
| Free Cash Flow Margin | fcf_sale |
| Operating Cash Flow Margin | ocf_sale |
| Operating Profit before Deprecia- tion scaled by Assets | ebitda_at |
| Operating Profit after Depreciation scaled by Assets | ebit_at |
| Firm Income scaled by Assets | fi_at |
| Net Income Including Extraordi- nary Items scaled by BE | nix_be |
| Operating Cash Flow scaled by BE | ocf_be |
| Free Cash Flow scaled by BE Gross Profit scaled by BEV | fcf_be gp_bev |
| Operating Profit before Deprecia- tion scaled by BEV | ebitda_bev |
| Firm Income scaled by BEV | fi_bev |
| Cash Based Operating Profitability scaled by BEV | cop_bev |
| Gross Profit scaled by PPEN | gp-ppen |
| Operating Profit before Deprecia- tion scaled by PPEN | ebitda_ppen |
| Free Cash Flow scaled by PPEN Financial Cash Flow scaled by As- sets | fcf_ppen fincf_at |
| Equity Issuance scaled by Assets Long-Term Debt Issuance scaled by Assets | eqis_at dltnetis_at |
| Net Short-Term Debt Issuance scaled by Assets | dstnetis_at |
| Net |  |
| Equity Net Payout scaled by Assets | eqnpo_at |
| Net Equity Payout scaled by Assets Total Dividends scaled by Assets | eqbb_at |
| Common Equity scaled by BEV | div_at be_bev |
| Total Debt scaled by BEV | debt_bev |
|  | cash_bev |
|  |  |
| Cash and Short-Term Investments scaled by BEV Preferred Stock scaled by BEV | pstk_bev |


44

| Long-Term Debt scaled by BEV | debtlt_bev |
| --- | --- |
| Short-Term Debt scaled by BEV | debtst_bev |
| Total Debt scaled by MEV | debt_mev |
| Preferred Stock scaled by MEV | pstk_mev |
| Long-Term Debt scaled by MEV | debtlt_mev |
| Short-Term Debt scaled by MEV | debtst_mev |
| Interest scaled by Total Debt | int_debt |
| Interest scaled by Long-Term Debt | int_debtlt |
| Operating Profit before Deprecia- tion scaled by Total Debt | ebitda_debt |
| Profit before D&A scaled by Cur- rent Liabilities | profit_cl |
| Operating Cash Flow scaled by Current Liabilities | ocf_cl |
| Operating Cash Flow scaled by To- tal Debt | ocf_debt |
| Cash Balance scaled by Total Lia- bilities | cash_lt |
| Inventory scaled by Current Assets | inv_act |
| Receivables scaled by Current As- sets | rec_act |
| Short-Term Debt scaled by Total Debt | debtst_debt |
| Current Liabilities scaled by Total Liabilities | cl_lt |
| Long-Term Debt scaled by Total Debt | debtlt_debt |
| Free Cash Flow scaled by Operating Cash Flow | fcf_ocf |
| Total Liabilities scaled by Total Tangible Assets | lt_ppen |
| Long-Term Debt to Book Equity | debtlt_be |
| Working Capital scaled by Assets | nwc_at |
| Debt-to-Assets | debt_at |
| Debt to Shareholders' Equity Ratio | debt_be |
| Interest Coverage Ratio | ebit_int |
| Days Inventory Outstanding | inv_days |
| Days Sales Outstanding | rec_days |
| Days Accounts Payable Outstand- ing | ap_days |
| Cash Conversion Cycle | cash_conversion |
| Cash Ratio | cash_cl |
| Quick Ratio | caliq_cl |
| Current Ratio | ca_cl |
| Inventory Turnover | inv_turnover |
| Receivables Turnover | rec_turnover |
| Account Payables Turnover | ap_turnover |
| Advertising scaled by Sales | adv_sale |
| Labor Expense scaled by Sales | staff_sale |
| Sales scaled by Total Stockholders' Equity | sale_be |
| Dividend Payout Ratio | div_ni |
| scaled by Working Capital | sale_nwc |
| Sales Effective Tax Rate | tax_pi |


45

| Intrinsic Value | intrinsic_value |
| --- | --- |
| Cash and Short-Term Investments scaled by Market Equity | cash_me |
| Gross Profit scaled by ME | gp_me |
| Operating Profit before Deprecia- tion scaled by ME | ebitda_me |
| Operating Profit after Depreciation scaled by ME | ebit_me |
| Operating Earnings to Equity scaled by ME | ope_me |
| Net Income Including Extraordi- nary Items scaled by ME | nix_me |
| Cash Based Operating Profitability scaled by ME | cop_me |
| Book Equity scaled by MEV | be_mev |
| Total Assets scaled by MEV | at_mev |
| Cash and Short-Term Investments scaled by MEV | cash_mev |
| Property, Plans and Equipment Net scaled by MEV | ppen_mev |
| Total Dividends scaled by ME | div_me |
| Equity Buyback scaled by ME | eqbb_me |
| Equity Issuance scaled by ME | eqis_me |
| Equity Net Issuance scaled by ME Net Long-Term Debt Issuance scaled by MEV | eqnetis_me |
| Net Short-Term Debt Issuance scaled by MEV | dstnetis_mev |
| Net Debt Issuance scaled by MEV | dbnetis_mev |
| Net Issuance scaled by MEV | netis_mev |
| Gross Profit scaled by MEV | gp_mev |
| Operating Profit after Depreciation scaled by MEV | ebit_mev |
| Sales scaled by MEV | sale_mev |
| Operating Cash Flow scaled by MEV | ocf_mev |
| Free Cash Flow scaled by MEV | fcf_mev |
| Cash Based Operating Profitability scaled by MEV | cop_mev |
| Financial Cash Flow Change scaled by MEV | fincf_mev |
| Net Income to Sales Quarterly Volatility | niq_saleq_std |
| Net Income scaled by Employees | ni_emp |
| Sales scaled by Employees | sale_emp |
| Net Income scaled by Assets | ni_at |
| Quarterly ROE Volatility | roeq_be_std |
| ROE Volatility | roe_be_std |
| Gross Product to Assets 5 yr Change | gpoa_ch5 |
| ROE 5 yr Change | roe_ch5 |
| ROA 5 yr Change | roa_ch5 |
| Operating Cash Flow to Assets 5 yr Change | cfoa_ch5 |


46

|  |
| --- |
| <table><thead></thead><tbody><tr><td>Gross Product to Sales 5 yr Change</td><td>gmar_ch5</td></tr><tr><td>Dividend to Price - 1 Month</td><td>div1m_me</td></tr><tr><td>Dividend to Price - 3 Months</td><td>div3m_me</td></tr><tr><td>Dividend to Price - 6 Months</td><td>div6m_me</td></tr><tr><td>Special Dividend to Price - 1 Month</td><td>divspc1m_me</td></tr><tr><td>Special Dividend to Price - 12 Month</td><td>divspc12m_me</td></tr><tr><td>Change in Shares - 1 Month</td><td>chcsho_1m</td></tr><tr><td>Change in Shares - 3 Month</td><td>chcsho_3m</td></tr><tr><td>Change in Shares - 6 Month</td><td>chcsho_6m</td></tr><tr><td>Net Equity Payout - 1 Month</td><td>eqnpo_1m</td></tr><tr><td>Net Equity Payout - 3 Month</td><td>eqnpo_3m</td></tr><tr><td>Net Equity Payout - 6 Month</td><td>eqnpo_6m</td></tr><tr><td>Momentum 0-2 Months</td><td>ret_2_0</td></tr><tr><td>Momentum 0-3 Months</td><td>ret_3_0</td></tr><tr><td>Momentum 0-6 Months</td><td>ret_6_0</td></tr><tr><td>Momentum 0-9 Months</td><td>ret_9_0</td></tr><tr><td>Momentum 0-12 Months</td><td>ret_12_0</td></tr><tr><td>Momentum 1-18 Months</td><td>ret_18_1</td></tr><tr><td>Momentum 1-24 Months</td><td>ret_24_1</td></tr><tr><td>Momentum 12-24 Months</td><td>ret_24_12</td></tr><tr><td>Momentum 1-36 Months</td><td>ret_36_1</td></tr><tr><td>Momentum 12-36 Months</td><td>ret_36_12</td></tr><tr><td>Momentum 1-48 Months</td><td>ret_48_1</td></tr><tr><td>Momentum 12-48 Months</td><td>ret_48_12</td></tr><tr><td>Momentum 1-60 Months</td><td>ret_60_1</td></tr><tr><td>Momentum 36-60 Months</td><td>ret_60_36</td></tr><tr><td>Market beta (21 days)</td><td>beta_21d</td></tr><tr><td>Market beta (252 days)</td><td>beta_252d</td></tr><tr><td>Return volatility (252 days)</td><td>rvol_252d</td></tr><tr><td>Idiosyncratic volatility from the CAPM (60 months)</td><td>ivol_capm_60m</td></tr><tr><td>The high-low return volatility</td><td>rvolhl_21d</td></tr></tbody></table> |
|  |
| Corwin and Schultz (2012) |


Note: This table shows cluster names as underlined section headings and, for each cluster, a description of the
factors included, the variable name used in the code, the original reference, the sample period used in the original
reference, the sign of the factor ("1" means "long" , "-1" means "short"), and whether the original reference found
the factor to be significant ("1" means "yes", "⌀" means "no"). For example, the first value factor "at_me" goes
long stocks with high values of assets-to-market and shorts those with low values (and would be done the reverse
if the sign was "-1" instead of "1 " )

47

# 11 Miscellaneous

Table 10: Country Code Key and MSCI Categorization

| Country | EXCNTRY-Country Code | MSCI Categorization |
| --- | --- | --- |
| Argentina | ARG | standalone |
| Australia | AUS | developed |
| Austria | AUT | developed |
| Bahrain | BHR | frontier |
| Bangladesh | BGD | frontier |
| Belgium | BEL | developed |
| Bermuda | BMU | not rated |
| Botswana | BWA | standalone |
| Brazil | BRA | emerging |
| Bulgaria | BGR | standalone |
| Canada | CAN | developed |
| Chile | CHL | emerging |
| China | CHN | emerging |
| Colombia | COL | emerging |
| Croatia | HRV | frontier |
| Cyprus | CYP | not rated |
| Czech Republic | CZE | emerging |
| Denmark | DNK | developed |
| Ecuador | ECU | not rated |
| Egypt | EGY | emerging |
| Estonia | EST | frontier |
| Finland | FIN | developed |
| France | FRA | developed |
| Germany | DEU | developed |
| Ghana | GHA | not rated |
| Greece | GRC | emerging |
| Guernsey | GGY | not rated |
| Hong Kong | HKG | developed |
| Hungary | HUN | emerging |
| Iceland | ISL | frontier |
| India | IND | emerging |
| Indonesia | IDN | emerging |
| Iran, Islamic Republic of | IRN | not rated |
| Ireland | IRL | developed |
| Israel | ISR | developed |
| Italy | ITA | developed |
| Jamaica | JAM | standalone |
| Japan | JPN | developed |
| Jordan | JOR | frontier |
| Kazakhstan | KAZ | frontier |
| Kenya | KEN | frontier |
| Korea, Republic of | KOR | emerging |
| Kuwait | KWT | emerging |
| Latvia | LVA | frontier |
| Lebanon | LBN | standalone |


48

| Country | EXCNTRY-Country Code | MSCI Categorization |
| --- | --- | --- |
| Lithuania | LTU | frontier |
| Luxembourg | LUX | not rated |
| Malawi | MWI | not rated |
| Malaysia | MYS | emerging |
| Malta | MLT | standalone |
| Mauritius | MUS | frontier |
| Mexico | MEX | emerging |
| Morocco | MAR | frontier |
| Namibia | NAM | not rated |
| Netherlands | NLD | developed |
| New Zealand | NZL | developed |
| Nigeria | NGA | standalone |
| Norway | NOR | developed |
| Oman | OMN | frontier |
| Pakistan | PAK | frontier |
| Palestinian Territory, Occupied | PSE | standalone |
| Peru | PER | emerging |
| Philippines | PHL | emerging |
| Poland | POL | emerging |
| Portugal | PRT | developed |
| Qatar | QAT | emerging |
| Romania | ROU | frontier |
| Russian Federation | RUS | not rated |
| Saudi Arabia | SAU | emerging |
| Senegal | SEN | frontier |
| Serbia | SRB | frontier |
| Singapore | SGP | developed |
| Slovakia | SVK | not rated |
| Slovenia | SVN | frontier |
| South Africa | ZAF | emerging |
| Spain | ESP | developed |
| Sri Lanka | LKA | frontier |
| Sweden | SWE | developed |
| Switzerland | CHE | developed |
| Taiwan, Province of China | TWN | emerging |
| Tanzania, United Republic of | TZA | not rated |
| Thailand | THA | emerging |
| Trinidad and Tobago | TTO | standalone |
| Tunisia | TUN | frontier |
| Turkey | TUR | emerging |
| Uganda | UGA | not rated |
| Ukraine | UKR | standalone |
| United Arab Emirates | ARE | emerging |
| United Kingdom | GBR | developed |
| United States | USA | developed |
| Uruguay | URY | not rated |
| Venezuela, Bolivarian Republic of | VEN | not rated |
| Viet Nam | VNM | frontier |
| Zambia | ZMB | not rated |
| Country | EXCNTRY-Country Code | MSCI Categorization |
| Zimbabwe | ZWE | standalone |


49

References

Abarbanell, J. S., & Bushee, B. J. (1998). Abnormal returns to a fundamental analysis
strategy. Accounting Review, 19-45.
Ali, A., Hwang, L.-S., & Trombley, M. A. (2003). Arbitrage risk and the book-to-market
anomaly. Journal of Financial Economics, 69(2), 355-373.
Amihud, Y. (2002). Illiquidity and stock returns: cross-section and time-series effects.
Journal of financial markets, 5(1), 31-56.
Anderson, C. W., & Garcia-Feijoo, L. (2006). Empirical evidence on capital investment,
growth options, and security returns. The Journal of Finance, 61(1), 171-194.
Ang, A., Chen, J., & Xing, Y. (2006). Downside risk. The review of financial studies, 19(4),
1191-1239.
Ang, A., Hodrick, R. J., Xing, Y., & Zhang, X. (2006). The cross-section of volatility and
expected returns. The Journal of Finance, 61(1), 259-299.
Asness, C., Frazzini, A., Gormsen, N. J., & Pedersen, L. H. (2020). Betting against correla-
tion: Testing theories of the low-risk effect. Journal of Financial Economics, 135(3),
629-652.
Asness, C. S., Frazzini, A., & Pedersen, L. H. (2019). Quality minus junk. Review of
Accounting Studies, 24(1), 34-112.
Balakrishnan, K., Bartov, E., & Faurel, L. (2010). Post loss / profit announcement drift.
Journal of Accounting and Economics, 50(1), 20-41.
Bali, T. G., Brown, S. J., & Tang, Y. (2017). Is economic uncertainty priced in the cross-
section of stock returns? Journal of Financial Economics, 126(3), 471-489.
Bali, T. G., Cakici, N., & Whitelaw, R. F. (2011). Maxing out: Stocks as lotteries and the
cross-section of expected returns. Journal of Financial Economics, 99(2), 427-446.
Bali, T. G., Engle, R. F., & Murray, S. (2016). Empirical asset pricing: The cross section
of stock returns. John Wiley & Sons.
Ball, R., Gerakos, J., Linnainmaa, J. T., & Nikolaev, V. (2016). Accruals, cash flows,
and operating profitability in the cross section of stock returns. Journal of Financial
Economics, 121 (1), 28-45.
Banz, R. W. (1981). The relationship between return and market value of common stocks.
Journal of financial economics, 9(1), 3-18.
Barbee Jr, W. C., Mukherji, S., & Raines, G. A. (1996). Do sales-price and debt-equity
explain stock returns better than book-market and firm size? Financial Analysts
Journal, 52(2), 56-60.
Barth, M. E., Elliott, J. A., & Finn, M. W. (1999). Market rewards associated with patterns
of increasing earnings. Journal of Accounting Research, 37(2), 387-413.
Basu, S. (1983). The relationship between earnings' yield, market value and return for nyse
common stocks: Further evidence. Journal of financial economics, 12(1), 129-156.
Belo, F., & Lin, X. (2012). The inventory growth spread. The Review of Financial Studies,
25(1), 278-313.

50

Belo, F., Lin, X., & Bazdresch, S. (2014). Labor hiring, investment, and stock return
predictability in the cross section. Journal of Political Economy, 122(1), 129-177.
Bhandari, L. C. (1988). Debt/equity ratio and expected common stock returns: Empirical
evidence. The journal of finance, 43(2), 507-528.
Blitz, D., Huij, J., & Martens, M. (2011). Residual momentum. Journal of Empirical
Finance, 18(3), 506-521.
Bouchaud, J.-P., Krueger, P., Landier, A., & Thesmar, D. (2019). Sticky expectations and
the profitability anomaly. The Journal of Finance, 74 (2), 639-674.
Boudoukh, J., Michaely, R., Richardson, M., & Roberts, M. R. (2007). On the importance
of measuring payout yield: Implications for empirical asset pricing. The Journal of
Finance, 62(2), 877-915.
Bradshaw, M. T., Richardson, S. A., & Sloan, R. G. (2006). The relation between corporate
financing activities, analysts' forecasts and stock returns. Journal of accounting and
economics, 42(1-2), 53-85.
Brennan, M. J., Chordia, T., & Subrahmanyam, A. (1998). Alternative factor specifications,
security characteristics, and the cross-section of expected stock returns. Journal of
financial Economics, 49(3), 345-373.
Chan, L. K., Lakonishok, J., & Sougiannis, T. (2001). The stock market valuation of research
and development expenditures. The Journal of finance, 56(6), 2431-2456.
Chordia, T., Subrahmanyam, A., & Anshuman, V. R. (2001). Trading activity and expected
stock returns. Journal of financial Economics, 59(1), 3-32.
Cooper, M. J., Gulen, H., & Schill, M. J. (2008). Asset growth and the cross-section of stock
returns. the Journal of Finance, 63(4), 1609-1651.
Corwin, S. A., & Schultz, P. (2012). A simple way to estimate bid-ask spreads from daily
high and low prices. The Journal of Finance, 67(2), 719-760.
Daniel, K., & Titman, S. (2006). Market reactions to tangible and intangible information.
The Journal of Finance, 61 (4), 1605-1643.
Datar, V. T., Naik, N. Y., & Radcliffe, R. (1998). Liquidity and stock returns: An alternative
test. Journal of financial markets, 1(2), 203-219.
De Bondt, W. F. , & Thaler, R. (1985). Does the stock market overreact? The Journal of
finance, 40(3), 793-805.
Dechow, P. M., Sloan, R. G., & Soliman, M. T. (2004). Implied equity duration: A new
measure of equity risk. Review of Accounting Studies, 9(2), 197-228.
Desai, H., Rajgopal, S., & Venkatachalam, M. (2004). Value-glamour and accruals mispric-
ing: One anomaly or two? The Accounting Review, 79(2), 355-385.
Dichev, I. D. (1998). Is the risk of bankruptcy a systematic risk? the Journal of Finance,
53(3), 1131-1147.
Dimson, E. (1979). Risk measurement when shares are subject to infrequent trading. Journal
of Financial Economics, 7(2), 197-226.
Fairfield, P. M., Whisenant, J. S., & Yohn, T. L. (2003). Accrued earnings and growth:
Implications for future profitability and market mispricing. The accounting review,
78(1), 353-371.
Fama, E. F., & French, K. R. (1992). The cross-section of expected stock returns. the
Journal of Finance, 47(2), 427-465.

51

Fama, E. F., & French, K. R. (1997). Industry costs of equity. Journal of Financial Eco-
nomics, 43(2), 153-193. Retrieved from https : / /www · sciencedirect . com/ science/
article/pii/S0304405X96008963 doi: https:/ /doi.org/ 10.1016/S0304-405X(96)
00896-3
Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model. Journal of financial
economics, 116(1), 1-22.
Fama, E. F., & MacBeth, J. D. (1973). Risk, return, and equilibrium: Empirical tests.
Journal of political economy, 81 (3), 607-636.
Foster, G., Olsen, C., & Shevlin, T. (1984). Earnings releases, anomalies, and the behavior
of security returns. Accounting Review, 574-603.
Francis, J., LaFond, R., Olsson, P. M., & Schipper, K. (2004). Costs of equity and earnings
attributes. The accounting review, 79(4), 967-1010.
Frankel, R., & Lee, C. M. (1998). Accounting valuation, market expectation, and cross-
sectional stock returns. Journal of Accounting and economics, 25(3), 283-319.
Frazzini, A., & Pedersen, L. H. (2014). Betting against beta. Journal of Financial Economics,
111(1), 1-25.
George, T. J., & Hwang, C.-Y. (2004). The 52-week high and momentum investing. The
Journal of Finance, 59(5), 2145-2176.
Hafzalla, N., Lundholm, R., & Matthew Van Winkle, E. (2011). Percent accruals. The
Accounting Review, 86(1), 209-236.
Hahn, J., & Lee, H. (2009). Financial constraints, debt capacity, and the cross-section of
stock returns. The Journal of Finance, 64(2), 891-921.
Harvey, C. R., & Siddique, A. (2000). Conditional skewness in asset pricing tests. The
Journal of finance, 55(3), 1263-1295.
Haugen, R. A., & Baker, N. L. (1996). Commonality in the determinants of expected stock
returns. Journal of financial economics, 41(3), 401-439.
Heston, S. L., & Sadka, R. (2008). Seasonality in the cross-section of stock returns. Journal
of Financial Economics, 87(2), 418-445.
Hirshleifer, D., Hou, K., Teoh, S. H., & Zhang, Y. (2004). Do investors overvalue firms with
bloated balance sheets? Journal of Accounting and Economics, 38, 297-331.
Hou, K., Xue, C., & Zhang, L. (2015). Digesting anomalies: An investment approach. The
Review of Financial Studies, 28(3), 650-705.
Huang, A. G. (2009). The cross section of cashflow volatility and expected stock returns.
Journal of Empirical Finance, 16(3), 409-429.
Jegadeesh, N. (1990). Evidence of predictable behavior of security returns. The Journal of
finance, 45(3), 881-898.
Jegadeesh, N., & Livnat, J. (2006). Revenue surprises and stock returns. Journal of
Accounting and Economics, 41 (1-2), 147-171.
Jegadeesh, N., & Titman, S. (1993). Returns to buying winners and selling losers: Implica-
tions for stock market efficiency. The Journal of finance, 48(1), 65-91.
Jensen, T. I., Kelly, B. T., & Pedersen, L. H. (2022). Is there a replication crisis in finance?
Journal of Finance, forthcoming.
Jiang, G., Lee, C. M., & Zhang, Y. (2005). Information uncertainty and expected returns.
Review of Accounting Studies, 10(2-3), 185-221.

52

Lakonishok, J., Shleifer, A., & Vishny, R. W. (1994). Contrarian investment, extrapolation,
and risk. The journal of finance, 49(5), 1541-1578.
Lamont, O., Polk, C., & Saa�-Requejo, J. (2001). Financial constraints and stock returns.
The review of financial studies, 14(2), 529-554.
Lev, B., & Nissim, D. (2004). Taxable income, future earnings, and equity values. The
accounting review, 79(4), 1039-1074.
Li, F. (2011). Earnings quality based on corporate investment decisions. Journal of Ac-
counting Research, 49(3), 721-752.
Litzenberger, R. H., & Ramaswamy, K. (1979). The effect of personal taxes and dividends
on capital asset prices: Theory and empirical evidence. Journal of financial economics,
7(2), 163-195.
Liu, W. (2006). A liquidity-augmented capital asset pricing model. Journal of financial
Economics, 82(3), 631-671.
Loughran, T., & Wellman, J. W. (2011). New evidence on the relation between the enterprise
multiple and average stock returns. Journal of Financial and Quantitative Analysis,
1629-1650.
Lyandres, E., Sun, L., & Zhang, L. (2008). The new issues puzzle: Testing the investment-
based explanation. The Review of Financial Studies, 21 (6), 2825-2855.
Miller, M. H., & Scholes, M. S. (1982). Dividends and taxes: Some empirical evidence.
Journal of Political Economy, 90(6), 1118-1141.
Novy-Marx, R. (2011). Operating leverage. Review of Finance, 15(1), 103-134.
Novy-Marx, R. (2012). Is momentum really momentum? Journal of Financial Economics,
103(3), 429-453.
Novy-Marx, R. (2013). The other side of value: The gross profitability premium. Journal
of financial economics, 108(1), 1-28.
Ortiz-Molina, H., & Phillips, G. M. (2014). Real asset illiquidity and the cost of capital.
Journal of Financial and Quantitative Analysis, 1-32.
Palazzo, B. (2012). Cash holdings, risk, and expected returns. Journal of Financial Eco-
nomics, 104(1), 162-185.
Penman, S. H., Richardson, S. A., & Tuna, I. (2007). The book-to-price effect in stock
returns: accounting for leverage. Journal of accounting research, 45(2), 427-467.
Piotroski, J. D. (2000). Value investing: The use of historical financial statement information
to separate winners from losers. Journal of Accounting Research, 1-41.
Pontiff, J., & Woodgate, A. (2008). Share issuance and cross-sectional returns. The Journal
of Finance, 63(2), 921-945.
Richardson, S. A., Sloan, R. G., Soliman, M. T., & Tuna, I. (2005). Accrual reliability,
earnings persistence and stock prices. Journal of accounting and economics, 39(3),
437-485.
Rosenberg, B., Reid, K., & Lanstein, R. (1985). Persuasive evidence of market inefficiency.
The Journal of Portfolio Management, 11(3), 9-16.
Sloan, R. G. (1996). Do stock prices fully reflect information in accruals and cash flows
about future earnings? Accounting review, 289-315.
Soliman, M. T. (2008). The use of dupont analysis by market participants. The Accounting
Review, 83(3), 823-853.

53

Stambaugh, R. F., & Yuan, Y. (2017). Mispricing factors. The Review of Financial Studies,
30(4), 1270-1315.
Thomas, J., & Zhang, F. X. (2011). Tax expense momentum. Journal of Accounting
Research, 49(3), 791-821.
Thomas, J. K., & Zhang, H. (2002). Inventory changes and future returns. Review of
Accounting Studies, 7(2), 163-187.
Titman, S., Wei, K. C. J., & Xie, F. (2004, December). Capital investments and stock
returns. The Journal of Financial and Quantitative Analysis, 39(4), 677-700.
Xie, H. (2001). The mispricing of abnormal accruals. The accounting review, 76(3), 357-373.

54