# Investigation 02: COVID Damage Forensics

*Part of a [5-investigation series](README.md) demonstrating AI-driven public health analysis using ARTPARK MCP tools.*

> **The question:** "How badly did the COVID-19 pandemic break India's FMD vaccination program? Quantify the damage, state by state."
>
> **The headline:** Nationwide average immunity crash: **-32.8 percentage points** across 19 comparable states. Only 1 state (Rajasthan) held steady. 4 states lost more than 50pp.

## Why this matters

India's FMD seromonitoring data has a **3-year gap**: no records exist for 2019-2020. The FMDCP program ended and the NADCP program began during the pandemic. But nobody has quantified the damage across all 35 states. The Karnataka example (previous reports) showed a dramatic immunity crash -- this investigation asks: was that the norm, or the exception?

## What the AI did (autonomously)

1. Pulled **all 238 seromonitoring records** via `4_get_data(dataset_id="0087", table_name="seromonitoring", limit=250)`
2. For each of 35 states, identified the **last pre-COVID round** (2018 or earlier) and the **first post-COVID round** (2021 NADCP)
3. Computed the "immunity crash" for type O: last pre-COVID post-vac% minus first post-COVID pre-vac%
4. Ranked all 19 states with both data points by crash severity
5. Identified which states maintained immunity and which are recovering

## The key metric: "Immunity Crash"

The crash measures how much vaccine-induced immunity was lost during the pandemic gap:

```
Immunity Crash = (Last pre-COVID post-vac O%) - (First post-COVID pre-vac O%)
```

A large negative number means the state lost most of its FMD protection during the gap. The post-vac level represents the *best* immunity achieved before COVID. The pre-vac level represents what remained when NADCP teams arrived in 2021.

## The real data

### All 19 states ranked by immunity crash (type O)

From `4_get_data(dataset_id="0087", table_name="seromonitoring", limit=250)`. Each row verified against raw data.

| Rank | State | Last Pre-COVID PostVac O% | Year | First Post-COVID PreVac O% | Year | Crash (pp) |
|------|-------|--------------------------|------|---------------------------|------|------------|
| 1 | **Haryana** | 94.1 (FMDCP R9) | 2015 | 24.2 (NADCP R1) | 2021 | **-69.9** |
| 2 | **Andhra Pradesh** | 75.7 (FMDCP R26) | 2018 | 9.0 (NADCP R1) | 2021 | **-66.7** |
| 3 | **Telangana** | 78.3 (FMDCP R25) | 2018 | 20.7 (NADCP R1) | 2021 | **-57.6** |
| 4 | **Delhi** | 92.0 (FMDCP R19) | 2015 | 39.5 (NADCP R1) | 2021 | **-52.5** |
| 5 | **Karnataka** | 64.8 (FMDCP R14) | 2018 | 16.3 (NADCP R1) | 2021 | **-48.5** |
| 6 | Maharashtra | 59.0 (FMDCP R24) | 2018 | 17.5 (NADCP R1) | 2021 | -41.5 |
| 7 | Tamil Nadu | 77.4 (FMDCP R22) | 2018 | 37.0 (NADCP R1) | 2021 | -40.4 |
| 8 | Odisha | 51.3 (FMDCP R3) | 2018 | 12.7 (NADCP R1) | 2021 | -38.6 |
| 9 | Kerala | 83.8 (FMDCP R21) | 2018 | 47.4 (NADCP R1) | 2021 | -36.4 |
| 10 | Chhattisgarh | 47.7 (FMDCP R2) | 2018 | 17.0 (NADCP R1) | 2021 | -30.7 |
| 11 | Gujarat | 48.7 (FMDCP R24) | 2018 | 18.8 (NADCP R1) | 2021 | -29.9 |
| 12 | Punjab | 39.0 (FMDCP R23) | 2018 | 11.5 (NADCP R1) | 2021 | -27.5 |
| 13 | Madhya Pradesh | 31.7 (FMDCP R2) | 2017 | 10.0 (NADCP R1) | 2021 | -21.7 |
| 14 | Uttar Pradesh | 30.8 (FMDCP R7) | 2018 | 9.9 (NADCP R1) | 2021 | -20.9 |
| 15 | A&N Islands | 40.4 (FMDCP R23) | 2018 | 19.8 (NADCP R1) | 2021 | -20.6 |
| 16 | Goa | 49.8 (FMDCP R14) | 2018 | 34.1 (NADCP R1) | 2021 | -15.7 |
| 17 | Uttarakhand | 18.7 (FMDCP R3) | 2018 | 4.2 (NADCP R1) | 2021 | -14.5 |
| 18 | *Rajasthan* | 45.0 (FMDCP R6) | 2018 | 44.9 (NADCP R1) | 2021 | *-0.1* |
| 19 | *Puducherry* | 73.6 (FMDCP R15) | 2018 | 84.1 (NADCP R1) | 2021 | *+10.5* |

### Headline findings

**Nationwide average immunity crash: -32.8 percentage points.**

Out of 19 states with comparable data:
- **17 states** lost immunity (negative crash)
- **1 state** held steady: Rajasthan (-0.1pp -- essentially zero loss)
- **1 state** actually *improved*: Puducherry (+10.5pp)
- **4 states** lost more than 50pp of type O immunity; Karnataka (-48.5pp) was the 5th-worst

> **Important caveat on Haryana and Delhi:** Their last FMDCP seromonitoring data was from **2015**, not 2018. The 6-year gap to 2021 NADCP means their crashes reflect both the pandemic AND 3 years of pre-pandemic inactivity. For the other 17 states, the gap was 3 years (2018 → 2021). Haryana's rank-1 position should be interpreted with this in mind. *→ Nagaland's data quality issues during this same period are explored in [Investigation 03](06_needle_in_haystack.md).*

### The 5 worst-hit states

#### 1. Haryana: -69.9pp crash (94.1% → 24.2%) ⚠️

Haryana had India's best FMD immunity in 2015 -- 94.1% post-vac for type O. By 2021, only 24.2% of animals had antibodies before the first NADCP round. **Caveat:** Haryana's last seromonitoring data was from **2015** (6 years before NADCP), making this the longest gap of any state. The 69.9pp loss reflects both the pandemic AND 3 years of pre-pandemic program inactivity. If only the 3-year pandemic window is considered, the true pandemic-attributable crash is likely 30-45pp.

#### 2. Andhra Pradesh: -66.7pp crash (75.7% → 9.0%)

Andhra Pradesh went from 75.7% post-vac immunity in 2018 to just 9.0% pre-vac in 2021. This is the most dramatic fall from a recent (2018) baseline. By 2021, 91% of Andhra's livestock had no detectable type O antibodies -- effectively unprotected.

#### 3. Telangana: -57.6pp crash (78.3% → 20.7%)

Telangana had been one of the stronger-performing states under FMDCP, with post-vac levels consistently above 75% in 2018. The crash to 20.7% suggests complete cessation of vaccination during the gap years.

#### 4. Delhi: -52.5pp crash (92.0% → 39.5%)

Delhi's small livestock population (n=200 in most rounds) makes these numbers less reliable, but the trend is clear: near-universal protection in 2015 collapsed to under 40% by 2021.

#### 5. Karnataka: -48.5pp crash (64.8% → 16.3%)

Karnataka's well-documented decline (covered in Examples 01-02) is confirmed as the 5th-worst nationally. The 2018 post-vac of 64.8% was already declining from earlier peaks of 97.0% (2014).

### The survivors: States that defied the pandemic

#### Rajasthan: -0.1pp (45.0% → 44.9%)

Rajasthan is the only state that maintained its immunity through the pandemic, losing just 0.1 percentage points. This could mean Rajasthan continued vaccinating through 2019-2020, or that the FMD virus was circulating naturally at high enough levels to maintain population immunity without vaccination.

#### Puducherry: +10.5pp (73.6% → 84.1%)

Puducherry actually *gained* 10.5 percentage points of immunity during the pandemic gap. With its tiny territory and small livestock population (sample sizes 248-960), this likely reflects ongoing local vaccination or very high viral circulation in a densely housed livestock population.

### The recovery: 2022 NADCP Round 2 results

Several states showed dramatic recovery after the first NADCP round. The "Recovery %" measures how much of the COVID crash each state has clawed back:

```
Recovery % = (2022 PostVac O% - 2021 PreVac O%) / (PreCOVID PostVac O% - 2021 PreVac O%) × 100
```

| State | Pre-COVID Peak | 2021 Pre-Vac | 2022 Post-Vac | Recovery % | Verdict |
|-------|---------------|-------------|--------------|-----------|---------|
| Odisha | 51.3% | 12.7% | **89.9%** | **200%** | Surpassed pre-COVID peak |
| Karnataka | 64.8% | 16.3% | **85.5%** | **143%** | Surpassed pre-COVID peak |
| Maharashtra | 59.0% | 17.5% | **76.3%** | **142%** | Surpassed pre-COVID peak |
| Haryana | 94.1% | 24.2% | **68.8%** | **64%** | Partial recovery |
| Andhra Pradesh | 75.7% | 9.0% | **41.5%** | **49%** | Slow -- still half-way |
| Gujarat | 48.7% | 18.8% | **40.6%** | **73%** | Moderate -- approaching peak |

**Odisha, Karnataka, and Maharashtra didn't just recover -- they surpassed their pre-COVID peaks.** This is the strongest evidence that the NADCP program is working where implemented well.

**Andhra Pradesh is India's biggest recovery laggard** -- after two NADCP rounds, it has recovered less than half its lost immunity. This drives its #1 position in the risk model (*→ see [Investigation 05](08_risk_model.md)*).

**Gujarat's recovery is deceptively high** at 73%, but only because its pre-COVID peak was already low (48.7%). Its absolute 2022 level of 40.6% is dangerously inadequate.

### The bigger picture: Program transition damage

The data reveals that the immunity crash wasn't purely a COVID effect. Two compounding factors:

1. **The FMDCP → NADCP transition**: The FMDCP program ended before NADCP started. Some states (like Haryana) had their last FMDCP seromonitoring in 2015, meaning there was already a multi-year gap *before* COVID hit.

2. **Different program structures**: FMDCP round numbers varied wildly by state (e.g., Gujarat was on Round 24, while Chhattisgarh was on Round 2). The NADCP standardized to Round 1 for all states, but this meant experienced states lost their accumulated momentum.

## What an API can't do

An API returns 238 rows of seromonitoring data. It does not:
- Identify which two rows to compare for each state (last pre-COVID vs first post-COVID)
- Handle the complexity that "pre-COVID" means different years for different states
- Recognize that Haryana's 6-year gap is different from Karnataka's 3-year gap
- Notice that Rajasthan and Puducherry are outliers that defied the pattern
- Synthesize the recovery trajectory from 2022 data as evidence the program is bouncing back
- Frame the findings as a "damage report" with policy implications

## Methodology notes

- "Last pre-COVID" = the chronologically last round with post-vac data in 2018 or earlier. For states with multiple 2018 rounds, the highest round number was used.
- "First post-COVID" = NADCP Round 1 (2021) pre-vac data. For states without 2021 data, they were excluded from the ranking.
- 16 states/territories lacked the data pairing needed for comparison and were excluded: Assam, Arunachal Pradesh, Bihar, Chandigarh, Dadra & Nagar Haveli, Himachal Pradesh, Jammu & Kashmir, Jharkhand, Lakshadweep, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, Tripura, and West Bengal. Most are new NADCP entrants; Himachal Pradesh and West Bengal had some FMDCP history but lacked the specific pre-COVID post-vac/post-COVID pre-vac pair required.
- Haryana and Delhi's last pre-COVID data was from 2015, not 2018, making their crashes reflect a longer gap.
- Sample sizes vary dramatically (Delhi: 200, Tamil Nadu: 6,400), which affects reliability.

## See also

- [Investigation 03: Needle in a Haystack](06_needle_in_haystack.md) -- several anomalies in the seromonitoring data (Nagaland's impossible result, Bihar's vaccine failure) occurred during the same post-COVID period documented here
- [Investigation 04: Myth Debunker](07_myth_debunker.md) -- the COVID crash explains why most YELLOW states peaked years ago and are now in decline
- [Investigation 05: FMD Risk Model](08_risk_model.md) -- the top-3 risk states (AP, Bihar, Gujarat) are all slow-recovery states from this investigation

## Datasets used

- `0087` -- FMD Nationwide Seromonitoring Data (238 rows, 14 columns, 35 states, 2011-2022)
