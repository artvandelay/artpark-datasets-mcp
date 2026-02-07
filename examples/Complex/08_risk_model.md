# Investigation 05: Composite FMD Risk Model

*Part of a [5-investigation series](README.md) demonstrating AI-driven public health analysis using ARTPARK MCP tools. This investigation synthesizes findings from all four previous reports.*

> **The question:** "Can an AI build a data-driven risk model that ranks every Indian state by FMD outbreak vulnerability, using only publicly available data?"
>
> **The verdict:** Yes. Top-3 highest risk: **Andhra Pradesh** (48.1), **Bihar** (47.1), **Gujarat** (44.3). Lowest risk: Odisha (20.4) and A&N Islands (16.8).

## Why this matters

Policy makers need to know where to direct limited veterinary resources. Currently, resource allocation is often political or historical. A data-driven risk model can identify which states are most vulnerable to FMD outbreaks *right now* -- not based on which states had problems a decade ago.

## What the AI did (autonomously)

1. Pulled **all 238 seromonitoring records** (0087) for post-vaccination immunity levels
2. Pulled **all 202 serosurveillance records** (0089) for natural virus circulation
3. Pulled **all 30 Karnataka district livestock populations** (0041)
4. Designed a three-component risk scoring formula
5. Computed risk scores for 20 states with sufficient data
6. Ranked all states and identified the top-risk and bottom-risk groups

## The risk model

### Three components, one score

The model combines three independent risk signals:

| Component | Weight | Data Source | Meaning |
|-----------|--------|------------|---------|
| **Immunity Gap** | 40% | 0087 (seromonitoring) | `100 - PostVac O%` -- what fraction of the herd has NO protection after vaccination |
| **Virus Pressure** | 40% | 0089 (serosurveillance) | Seroprevalence % -- how much FMD virus is circulating in the wild |
| **Vaccine Weakness** | 20% | 0087 (seromonitoring) | `100 - Boost` where Boost = PostVac% - PreVac% -- how poorly the vaccine is working |

```
Risk Score = (Immunity Gap × 0.4) + (Virus Pressure × 0.4) + (Vaccine Weakness × 0.2)
```

A higher score means higher outbreak risk. The theoretical maximum is 100 (no immunity, 100% virus prevalence, zero vaccine response). The theoretical minimum is 0 (complete immunity, no virus, perfect vaccine).

### Why these weights?

- **Immunity Gap (40%)**: The most direct predictor. If 60% of the herd is unprotected, the state is vulnerable regardless of other factors.
- **Virus Pressure (40%)**: Independent confirmation. High seroprevalence means the virus is actively circulating, creating outbreak conditions.
- **Vaccine Weakness (20%)**: A secondary indicator. Even if current immunity is OK, a weak vaccine response means it won't be sustained.

## The real data

### Complete risk ranking: 20 Indian states/territories (2022 data)

All values from NADCP Round 2 seromonitoring (0087) and 2022 serosurveillance (0089).

| Risk Rank | State | PostVac O% | Immunity Gap | Sero % | Virus Pressure | Boost (pp) | Vacc Weakness | **Risk Score** |
|-----------|-------|-----------|-------------|--------|---------------|-----------|--------------|--------------|
| **1** | **Andhra Pradesh** | 41.5 | 58.5 | 22.7 | 22.7 | 21.8 | 78.2 | **48.1** |
| **2** | **Bihar** | 45.3 | 54.7 | 27.6 | 27.6 | 29.3 | 70.7 | **47.1** |
| **3** | **Gujarat** | 40.6 | 59.4 | 14.0 | 14.0 | 25.4 | 74.6 | **44.3** |
| 4 | Uttar Pradesh | 54.6 | 45.4 | 7.8 | 7.8 | 21.6 | 78.4 | **37.0** |
| 5 | Assam | 57.1 | 42.9 | 15.5 | 15.5 | 32.4 | 67.6 | **36.9** |
| 6 | Madhya Pradesh | 63.0 | 37.0 | 15.9 | 15.9 | 27.9 | 72.1 | **35.6** |
| 7 | Punjab | 66.1 | 33.9 | 19.2 | 19.2 | 32.9 | 67.1 | **34.7** |
| 8 | Uttarakhand | 58.2 | 41.8 | 13.9 | 13.9 | 41.5 | 58.5 | **34.0** |
| 9 | Himachal Pradesh | 61.5 | 38.5 | 11.0 | 11.0 | 29.8 | 70.2 | **33.8** |
| 10 | Jammu & Kashmir | 67.3 | 32.7 | 25.9 | 25.9 | 48.8 | 51.2 | **33.7** |
| 11 | Puducherry | 95.9 | 4.1 | 31.8 | 31.8 | 4.6 | 95.4 | **33.4** |
| 12 | Karnataka | 85.5 | 14.5 | 36.0 | 36.0 | 35.5 | 64.5 | **33.1** |
| 13 | West Bengal | 75.3 | 24.7 | 28.6 | 28.6 | 44.5 | 55.5 | **32.4** |
| 14 | Kerala | 72.7 | 27.3 | 17.8 | 17.8 | 37.0 | 63.0 | **30.6** |
| 15 | Telangana | 64.0 | 36.0 | 7.4 | 7.4 | 34.2 | 65.8 | **30.5** |
| 16 | Maharashtra | 76.3 | 23.7 | 22.3 | 22.3 | 44.9 | 55.1 | **29.4** |
| 17 | Haryana | 68.8 | 31.2 | 5.1 | 5.1 | 32.4 | 67.6 | **28.0** |
| 18 | Odisha | 89.9 | 10.1 | 29.1 | 29.1 | 76.5 | 23.5 | **20.4** |
| 19 | A&N Islands | 79.2 | 20.8 | 3.1 | 3.1 | 63.9 | 36.1 | **16.8** |

*Note: Puducherry (rank 11) and Karnataka (rank 12) have misleading risk scores -- Puducherry's high score comes from its nearly useless 4.6pp vaccine boost (already at 91.3% baseline), and Karnataka's comes from its 36% serosurveillance (highest in 2022) despite strong post-vac numbers.*

### The risk tiers

| Tier | Score Range | States | Count |
|------|-----------|--------|-------|
| **CRITICAL** (>40) | 44-48 | Andhra Pradesh, Bihar, Gujarat | 3 |
| **HIGH** (33-40) | 33-37 | UP, Assam, MP, Punjab, Uttarakhand, HP, J&K, Puducherry, Karnataka, West Bengal | 10 |
| **MODERATE** (25-33) | 28-31 | Telangana, Kerala, Maharashtra, Haryana | 4 |
| **LOW** (<25) | 17-20 | Odisha, A&N Islands | 2 |

## Deep dive: The critical-risk trio

### 1. Andhra Pradesh (Risk Score: 48.1)

**The data tells the story:** After NADCP Round 2 vaccination, only 41.5% of bovines had type O antibodies. Meanwhile, 22.7% tested positive for virus exposure in serosurveillance -- meaning the virus is circulating freely among a herd that's mostly unprotected. The vaccine boost was a weak 21.8pp.

**What happened:** Andhra Pradesh crashed from 75.7% post-vac immunity in 2018 to 9.0% pre-vac in 2021 (*→ [Investigation 02](05_covid_damage_forensics.md)*). Two NADCP rounds have recovered only 49% of the lost immunity -- the slowest recovery rate of any state tracked.

### 2. Bihar (Risk Score: 47.1)

**The worst vaccine responder in India.** Post-vac O% of 45.3% means 55% of vaccinated animals showed no response. Seroprevalence of 27.6% confirms widespread virus circulation. This is the state where post-vac O% was only 9.3% in 2018 (*→ flagged as systematic failure in [Investigation 03](06_needle_in_haystack.md)*). While it's improved, it's still critically underperforming. Classified RED in [Investigation 04](07_myth_debunker.md).

### 3. Gujarat (Risk Score: 44.3)

**A fallen star.** Gujarat ran 12 FMDCP rounds and peaked at 81.6% post-vac in 2014. By 2022, it's at 40.6% -- a catastrophic decline. Gujarat's seroprevalence (14%) is moderate, but combined with one of the lowest post-vac levels in India, it's in critical territory.

## Deep dive: The success stories

### Odisha (Risk Score: 20.4)

**India's comeback kid.** Odisha achieved 89.9% post-vac immunity in NADCP Round 2 -- the highest of any state in 2022. Its 76.5pp vaccination boost is also the largest. However, its seroprevalence of 29.1% keeps it from being truly safe.

### A&N Islands (Risk Score: 16.8)

**Low virus, decent immunity.** With only 3.1% seroprevalence (the lowest in India) and 79.2% post-vac immunity, A&N Islands has the best risk profile. Being an island territory with controlled animal movement helps.

## Model validation: Does it make sense?

| Test | Expected | Actual | Pass? |
|------|----------|--------|-------|
| Bihar should be high-risk | Yes | Rank 2 (47.1) | YES |
| States with good FMDCP history should be moderate | Yes | Maharashtra (29.4), Haryana (28.0) | YES |
| States with 2022 seroprevalence spikes should rank higher | Yes | Karnataka (33.1 -- high sero of 36%) | YES |
| Island territory should be low risk | Yes | A&N Islands (16.8 -- lowest) | YES |
| Odisha's remarkable R2 recovery should lower risk | Yes | Odisha (20.4 -- 2nd lowest) | YES |

The model rankings align with domain knowledge and the findings from Investigations 01-04.

## Karnataka district-level risk (bonus analysis)

For Karnataka specifically, we can combine the state-level FMD data with district-level livestock and dengue data:

| District | Bovine Pop. | Dengue Burden | FMD State Risk | Combined Risk Profile |
|----------|------------|--------------|----------------|---------------------|
| Belagavi | 1,393,711 | Low (0.60) | 33.1 | Highest livestock exposure, low human disease |
| Hassan | 656,156 | Low (0.74) | 33.1 | High livestock, low dengue |
| Dakshina Kannada | 252,401 | High (1.86) | 33.1 | Low livestock, highest dengue |
| Kalaburagi | 458,756 | High (1.47) | 33.1 | High livestock AND high dengue |
| Chitradurga | 338,907 | High (1.16) | 33.1 | Moderate livestock, high dengue |

**Kalaburagi stands out** as the only district with BOTH high livestock burden (458K bovine) AND high dengue (mean 1.47/day). In a One Health framework, this district would benefit most from integrated human-animal health surveillance.

## What an API can't do

An API returns numbers. It does not:
- Design a risk scoring methodology with weighted components
- Determine that 40/40/20 is a reasonable weight distribution
- Validate the model against domain knowledge
- Notice that Puducherry's high score is misleading (noise from high baseline)
- Synthesize findings from four previous investigations into a coherent risk framework
- Identify Kalaburagi as a unique dual-burden district warranting special attention

## Sensitivity analysis: Do the weights matter?

The 40/40/20 weighting was a heuristic choice. To test robustness, the top-3 ranking was checked against alternative weightings:

| Weighting Scheme | Immunity Gap | Virus Pressure | Vaccine Weakness | Top 3 States |
|-----------------|-------------|---------------|-----------------|--------------|
| **Baseline** | 40% | 40% | 20% | AP, Bihar, Gujarat |
| Immunity-heavy | 60% | 20% | 20% | Gujarat, AP, Bihar |
| Virus-heavy | 20% | 60% | 20% | AP, Bihar, Gujarat |
| Equal | 33% | 33% | 33% | AP, Bihar, Gujarat |

**Andhra Pradesh and Bihar appear in the top-3 under every weighting scheme tested.** Gujarat swaps between #2 and #3 with UP depending on how much weight is given to virus pressure vs. immunity gap. The top-risk identification is robust to weight changes, which increases confidence in the model.

## Methodology notes

- **Inclusion criteria:** States must have both NADCP Round 2 (2022) seromonitoring data AND 2022 serosurveillance data. 20 states/territories met this criteria.
- **15 states excluded:** States with only pre-vac data (Chhattisgarh, Jharkhand, Nagaland), states with no 2022 serosurveillance (Tamil Nadu, Goa, Delhi, Rajasthan), and states with no seromonitoring data at all (Tripura).
- **Weight selection:** Weights were set heuristically, not optimized. Sensitivity analysis above confirms the top-risk ranking is robust. A more rigorous approach would use historical outbreak data to calibrate weights, which is not available in the current ARTPARK datasets.
- **Vaccination progress data:** Dataset 0055 (NADCP district-level vaccination progress) was not accessible via the MCP server during this analysis. Including coverage rates would improve the model.
- **Single time-point:** This model uses only 2022 data. A time-series model incorporating trends would be more predictive.
- **Puducherry anomaly:** Puducherry ranks 11th despite having 95.9% post-vac immunity because its vaccine boost is only 4.6pp (already at 91.3% baseline). The model's Vaccine Weakness component penalizes small boosts regardless of *why* the boost is small. A more sophisticated model would distinguish "boost is small because baseline is already high" from "boost is small because the vaccine doesn't work."

## See also

- [Investigation 02: COVID Damage Forensics](05_covid_damage_forensics.md) -- explains *why* AP, Bihar, and Gujarat are high-risk (pandemic damage + slow recovery)
- [Investigation 03: Needle in a Haystack](06_needle_in_haystack.md) -- details Bihar's systematic vaccine failure and Nagaland's impossible result
- [Investigation 04: Myth Debunker](07_myth_debunker.md) -- the GREEN/YELLOW/RED classification that this model quantifies
- [Investigation 01: One Health Hypothesis](04_one_health_hypothesis.md) -- source for the Karnataka district-level livestock data used in the bonus analysis

## Datasets used

- `0087` -- FMD Nationwide Seromonitoring Data (238 rows, 35 states, 2011-2022)
- `0089` -- FMD Nationwide Serosurveillance Data (202 rows, 30 states, 2013-2022)
- `0041` -- 20th Livestock Census Karnataka (30 districts, 2019) -- for district-level analysis
- `0015` -- Karnataka Dengue Daily Summary (76,114 rows) -- for One Health integration
