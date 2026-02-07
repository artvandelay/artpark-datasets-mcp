# Example 02: Temporal Narrative Construction

> **The question:** "Tell me the story of Karnataka's FMD vaccination journey over the past decade."

## Why this matters

An API returns rows. An LLM constructs a **narrative arc** — identifying phases, turning points, and anomalies across time. No human prompted it to look for "the COVID disruption" or "the program transition." It found these from the data.

## What the AI did (autonomously)

1. Fetched all 16 Karnataka seromonitoring records from dataset 0087
2. Noticed the data spans two programs (FMDCP rounds 1–14, NADCP rounds 1–2)
3. Identified three distinct phases from the numbers alone
4. Fetched Karnataka serosurveillance (dataset 0089) to corroborate with field-level seroprevalence

## The real data

All data from `4_get_data(dataset_id="0087", table_name="seromonitoring", filters={"state.name": "Karnataka"})`.

### Phase 1: The Ramp-Up (2011–2013, FMDCP Rounds 1–5)

| Year | Round | PreVac O% | PostVac O% | PreVac A% | PostVac A% |
|------|-------|-----------|------------|-----------|------------|
| 2011 | 1 | 40.0 | 56.0 | 15.0 | 40.0 |
| 2012 | 2 | 50.0 | 67.0 | 27.0 | 47.0 |
| 2012 | 3 | 54.8 | 60.3 | 29.2 | 41.8 |
| 2013 | 4 | 48.3 | 62.1 | 78.7 | 86.0 |
| 2013 | 5 | 33.0 | 59.0 | 52.0 | 68.0 |

The AI observed: Pre-vaccination antibody levels climbing from round to round (15% to 52% for type A), meaning previously vaccinated animals are retaining some immunity between rounds. The program is building cumulative herd protection.

### Phase 2: Peak Immunity (2014–2017, FMDCP Rounds 6–12)

| Year | Round | PreVac O% | PostVac O% | PreVac A% | PostVac A% |
|------|-------|-----------|------------|-----------|------------|
| 2014 | 6 | 61.0 | 86.0 | 62.0 | 87.0 |
| 2014 | 7 | 83.0 | 97.0 | 88.0 | 94.0 |
| 2015 | 8 | 87.5 | 95.5 | 84.9 | 96.7 |
| 2015 | 9 | 73.5 | 87.8 | 65.3 | 86.0 |
| 2016 | 10 | 70.6 | 82.9 | 59.1 | 75.8 |
| 2016 | 11 | 67.9 | 82.0 | 63.0 | 78.0 |
| 2017 | 12 | 75.0 | 88.0 | 88.0 | 90.0 |

The peak: **Round 7 (2014) hit 97% post-vac for type O and 94% for type A.** Round 8 (2015) achieved 96.7% for type A. These are near-complete seroconversion rates.

### Phase 3: Decline and Reset (2017–2022, FMDCP→NADCP transition)

| Year | Round | Program | PreVac O% | PostVac O% | PreVac A% | PostVac A% |
|------|-------|---------|-----------|------------|-----------|------------|
| 2017 | 13 | FMDCP | 52.5 | 69.7 | 45.8 | 61.2 |
| 2018 | 14 | FMDCP | 47.4 | 64.8 | 41.8 | 56.1 |
| 2021 | 1 | NADCP | 16.3 | 45.2 | 12.3 | 33.3 |
| 2022 | 2 | NADCP | 50.0 | 85.5 | 45.2 | 84.1 |

The cliff: Between 2018 (FMDCP Round 14) and 2021 (NADCP Round 1), there's a **3-year gap with no data**. Pre-vaccination levels crashed from 47.4% to 16.3% for type O and from 41.8% to 12.3% for type A. This coincides with both the FMDCP→NADCP program transition and the COVID-19 pandemic.

The recovery: By NADCP Round 2 (2022), post-vaccination levels rebounded to 85.5% (O) and 84.1% (A).

### Corroboration from serosurveillance (dataset 0089)

From `4_get_data(dataset_id="0089", table_name="serosurveillance", filters={"state.name": "Karnataka"})`. 7 rows.

| Year | Seroprevalence % |
|------|-----------------|
| 2013 | 21.1 |
| 2014 | 33.22 |
| 2015 | 34.15 |
| 2016 | 30.8 |
| 2018 | 23.0 |
| 2021 | 20.72 |
| 2022 | 36.0 |

This confirms the narrative: seroprevalence (natural virus exposure) peaked at 34.15% in 2015, dipped to 20.72% by 2021, then jumped to 36% in 2022. The 2022 spike suggests renewed virus circulation — possibly a consequence of the vaccination gap.

## What an API can't do

An API would return these 16 + 7 rows. It would not:
- Segment them into three narrative phases
- Identify the 3-year data gap as meaningful (2019–2020 missing)
- Connect the gap to the FMDCP→NADCP transition and COVID
- Notice that pre-vac levels climbing between rounds indicates cumulative immunity
- Cross-reference with a second dataset to corroborate the narrative

## Going deeper

This example tells Karnataka's story. The [Complex investigations](Complex/README.md) tell India's story:

- [COVID Damage Forensics](Complex/05_covid_damage_forensics.md) -- extends this temporal analysis to 19 states and quantifies the pandemic crash state by state, including recovery rates
- [Needle in a Haystack](Complex/06_needle_in_haystack.md) -- scans all 238 rows for the anomalies that this kind of temporal analysis might miss

## Datasets used

- `0087` — FMD Nationwide Seromonitoring Data (16 rows for Karnataka)
- `0089` — FMD Nationwide Serosurveillance Data (7 rows for Karnataka)
