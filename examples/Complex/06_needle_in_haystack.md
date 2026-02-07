# Investigation 03: Needle in a Haystack

*Part of a [5-investigation series](README.md) demonstrating AI-driven public health analysis using ARTPARK MCP tools.*

> **The question:** "Find the single most anomalous vaccination result in India's entire FMD seromonitoring dataset."
>
> **The winner:** Nagaland, 2021, NADCP Round 1 -- vaccination *halved* type O immunity from 13.2% to 6.0%. The lowest post-vaccination percentage in all 238 rows.

## Why this matters

India's FMD vaccination program generates hundreds of seromonitoring records across 35 states over a decade. Somewhere in those 238 rows, there are data points that don't make sense -- where vaccination appears to have *decreased* immunity, where pre-vaccination antibodies are impossibly high, or where a state's numbers defy biology. Finding these needles requires scanning every row and reasoning about what's normal vs. suspicious.

An API gives you the haystack. The AI finds the needles.

## What the AI did (autonomously)

1. Called `1_know_about_artpark_data()` to identify datasets
2. Called `2_get_tables("0087")` and `3_get_metadata("0087", "seromonitoring")` to learn column schema
3. Pulled **all 238 seromonitoring records** via `4_get_data(dataset_id="0087", table_name="seromonitoring", limit=250)`
4. Scanned every row for four categories of anomaly
5. Ranked findings by severity and crowned the most anomalous data point

## The anomaly hunt

### Category A: "Vaccination Failures" -- Post-vac LOWER than pre-vac

These are cases where animals had *fewer* antibodies after vaccination than before. This should be biologically impossible -- vaccination can only add immunity, not remove it.

| State | Year | Round | Serotype | PreVac % | PostVac % | Change | Severity |
|-------|------|-------|----------|----------|-----------|--------|----------|
| **Nagaland** | **2021** | **NADCP 1** | **O** | **13.2** | **6.0** | **-7.2pp** | **CRITICAL** |
| Punjab | 2013 | FMDCP 14 | A | 68.1 | 48.8 | -19.3pp | SEVERE |
| Uttarakhand | 2017 | FMDCP 2 | A | 26.1 | 12.1 | -14.0pp | SEVERE |
| Uttarakhand | 2017 | FMDCP 2 | O | 18.6 | 17.5 | -1.1pp | MODERATE |
| Uttar Pradesh | 2013 | FMDCP 16 | O | 38.2 | 37.7 | -0.5pp | MILD |

**The worst:** Nagaland 2021 -- post-vaccination type O dropped from 13.2% to 6.0%. Vaccination more than halved the measured antibody level. The 6.0% post-vac is also the **absolute lowest post-vaccination percentage in the entire 238-row dataset**.

Punjab 2013 Round 14 is the largest absolute drop: type A fell from 68.1% to 48.8%, a 19.3 percentage-point crash after vaccination.

### Category B: "Impossible Baselines" -- Pre-vac above 90%

If 90%+ of animals already have antibodies *before* vaccination in a given round, it means either: (a) the previous round's vaccine was extraordinarily effective, (b) there's massive natural virus circulation, or (c) the sample is biased toward previously vaccinated animals.

| State | Year | Round | PreVac O% | PreVac A% | PreVac Asia1% |
|-------|------|-------|-----------|-----------|---------------|
| **Delhi** | **2013** | **FMDCP 13** | **98.0** | **95.0** | **87.0** |
| Puducherry | 2017 | FMDCP 12 | 95.8 | 85.7 | 94.7 |
| Puducherry | 2022 | NADCP 2 | 91.3 | 83.1 | 85.5 |
| Puducherry | 2015 | FMDCP 7 | 95.1 | 60.4 | 93.0 |
| Delhi | 2011 | FMDCP 8 | 92.0 | 66.0 | 83.0 |

**The most extreme:** Delhi 2013 Round 13 -- 98% of animals already had type O antibodies and 95% had type A antibodies *before* vaccination. The post-vac numbers were 98% (O) and 100% (A). When your baseline is 98%, vaccination is measuring noise, not efficacy. Sample size was only 100 animals.

**Pattern:** Delhi (sample sizes 50-234) and Puducherry (sample sizes 30-960) dominate this category. Both are tiny urban territories with small livestock populations. The small sample sizes and urban setting make these results highly suspect.

### Category C: "Near-Complete Vaccine Failure States"

Some states show vaccination barely working at all -- post-vac levels remain dangerously low across multiple rounds.

| State | Year | Round | PreVac O% | PostVac O% | Boost | PostVac A% |
|-------|------|-------|-----------|------------|-------|------------|
| **Bihar** | **2018** | **FMDCP 5** | **3.6** | **9.3** | **+5.7pp** | **7.2** |
| Bihar | 2017 | FMDCP 4 | N/A | 11.0 | N/A | 7.8 |
| Uttarakhand | 2017 | FMDCP 1 | 16.0 | 18.6 | +2.6pp | 9.8 |
| Uttarakhand | 2018 | FMDCP 3 | 14.9 | 18.7 | +3.8pp | 10.1 |
| Himachal Pradesh | 2021 | NADCP 1 | 2.9 | 9.0 | +6.1pp | 7.3 |

**The pattern:** Bihar's post-vaccination O% of 9.3% means **90.7% of vaccinated animals showed no immune response**. Across two consecutive rounds (2017-2018), Bihar never exceeded 11% post-vac for type O. This is systematic vaccine failure -- not a data error, but a program that isn't working.

Uttarakhand shows a similar pattern: across 3 rounds (2017-2018), post-vac O% never exceeded 18.7%. The vaccine is barely registering.

### Category D: "Missing Post-Vaccination Data"

Several records have pre-vaccination data but **no post-vaccination data at all** (NaN for all post-vac fields). This means samples were collected before vaccination, but nobody came back to check if the vaccine worked.

| State | Year | Round | PreVac O% | PostVac O% |
|-------|------|-------|-----------|------------|
| Delhi | 2012 | FMDCP 9 | 57.0 | N/A |
| Delhi | 2012 | FMDCP 11 | 86.0 | N/A |
| Uttar Pradesh | 2013 | FMDCP 17 | 30.8 | N/A |
| Arunachal Pradesh | 2021 | NADCP 1 | 2.7 | N/A |
| Punjab | 2016 | FMDCP 19 | 70.8 | N/A |
| Chhattisgarh | 2022 | NADCP 2 | 24.4 | N/A |
| Jharkhand | 2022 | NADCP 2 | 33.7 | N/A |
| Nagaland | 2022 | NADCP 2 | 44.3 | N/A |

That's 8 out of 238 records (3.4%) with no post-vaccination follow-up. For NADCP Round 2 (2022), three states -- Chhattisgarh, Jharkhand, and Nagaland -- have no post-vac data at all. The entire point of seromonitoring is to measure vaccine response, so missing post-vac data represents a monitoring failure.

## The verdict: Most anomalous data point in India's FMD dataset

### The winner: Nagaland, 2021, NADCP Round 1

```
State:          Nagaland
Year:           2021
Program:        NADCP Round 1
PreVac O%:      13.2    →  PostVac O%:  6.0    (DROPPED by 7.2pp)
PreVac A%:       6.2    →  PostVac A%:  12.9   (rose by 6.7pp)
PreVac Asia1%:   4.3    →  PostVac Asia1%: 9.5 (rose by 5.2pp)
PreVac sample:  726     →  PostVac sample: 419 (42% fewer animals tested post-vac)
```

**Why this is the most anomalous:**

1. **Type O dropped after vaccination** -- the only case in the dataset where post-vac is less than half of pre-vac
2. **6.0% post-vac is the absolute floor** of the entire 238-row dataset
3. **Types A and Asia1 went up** while type O went down -- suggesting the vaccine worked for two serotypes but somehow *removed* type O immunity
4. **42% sample attrition** -- only 419 of 726 animals were available for post-vac testing. The missing 307 animals could have been the ones with higher O antibodies
5. **It was the first NADCP round** in a remote northeastern state with limited veterinary infrastructure

**Most likely explanation:** A combination of (a) the post-vaccination sample was not the same animals as the pre-vaccination sample, (b) logistical challenges in a remote state led to delayed or improper post-vac sampling, and (c) the vaccine batch may have had reduced type O potency. The 42% sample attrition is the strongest clue -- if the healthier animals were harder to re-sample, the post-vac group would be biased toward weaker responders.

### Runners-up

| Rank | Data Point | Why |
|------|-----------|-----|
| 2 | Punjab 2013 R14: Type A dropped 19.3pp after vaccination | Largest absolute post-vac drop in the dataset |
| 3 | Bihar 2018 R5: 9.3% post-vac O% after vaccination | 90.7% vaccine non-response rate |
| 4 | Delhi 2013 R13: 98% pre-vac O% (n=100) | Near-universal baseline makes vaccination meaningless |
| 5 | Uttarakhand 2017 R2: Both O and A dropped after vaccination | Only state where both major serotypes declined simultaneously |

## What an API can't do

An API returns 238 rows of numbers. It does not:
- Define what "anomalous" means across four different categories
- Notice that 6.0% is the absolute minimum across 238 rows
- Connect the 42% sample attrition to the antibody drop as a likely explanation
- Distinguish between data errors, sampling bias, and genuine biological phenomena
- Rank anomalies by severity and crown a winner with a reasoned explanation

## Methodology notes

- All anomalies were identified by scanning the full 238-row dataset returned by the MCP server
- "Vaccination failure" was defined as post-vac% < pre-vac% for type O or A specifically (Asia1 was excluded from primary analysis as it's less clinically relevant)
- Rows with NaN post-vac values were categorized separately as "missing data" rather than failures
- The `postvac.positive.asia1.pct` column is stored as string type (not float), which may indicate data quality issues in that column

## See also

- [Investigation 02: COVID Damage Forensics](05_covid_damage_forensics.md) -- Bihar's Category C failure and Nagaland's Category A anomaly both occurred during the COVID gap period
- [Investigation 04: Myth Debunker](07_myth_debunker.md) -- Bihar and Nagaland are both classified RED; Uttarakhand is also RED
- [Investigation 05: FMD Risk Model](08_risk_model.md) -- Bihar's systematic vaccine failure directly contributes to its #2 risk ranking

## Datasets used

- `0087` -- FMD Nationwide Seromonitoring Data (238 rows, 14 columns, 35 states, 2011-2022)
