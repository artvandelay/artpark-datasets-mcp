# Example 01: Cross-Dataset Reasoning

> **The question:** "Is India's FMD vaccination program working? Show me the evidence."

## Why this matters

A traditional API lets you query one dataset at a time. You'd need to manually pull seromonitoring data, then livestock census data, then serosurveillance data, then write code to join and analyze them.

With an LLM connected via MCP, you ask **one question** and it autonomously navigates 3 datasets, cross-references findings, and builds a synthesized answer.

## What the AI did (autonomously)

1. Called `1_know_about_artpark_data()` to identify relevant datasets
2. Pulled **seromonitoring** data (dataset 0087) — 238 records across 35 states, 2011-2022
3. Pulled **serosurveillance** data (dataset 0089) — 202 records with DIVA test results
4. Pulled **Karnataka livestock census** (dataset 0041) — 30 district-level records
5. Cross-referenced the findings to build a multi-layered answer

## The real data (fetched live from the MCP server)

### From dataset 0087 (Seromonitoring) — Karnataka's trajectory

All data below is real, from `4_get_data(dataset_id="0087", table_name="seromonitoring", filters={"state.name": "Karnataka"})`. 16 rows returned.

| Year | Round | Program | PreVac O% | PostVac O% | PreVac A% | PostVac A% |
|------|-------|---------|-----------|------------|-----------|------------|
| 2011 | 1 | FMDCP | 40.0 | 56.0 | 15.0 | 40.0 |
| 2012 | 2 | FMDCP | 50.0 | 67.0 | 27.0 | 47.0 |
| 2012 | 3 | FMDCP | 54.8 | 60.3 | 29.2 | 41.8 |
| 2013 | 4 | FMDCP | 48.3 | 62.1 | 78.7 | 86.0 |
| 2013 | 5 | FMDCP | 33.0 | 59.0 | 52.0 | 68.0 |
| 2014 | 6 | FMDCP | 61.0 | 86.0 | 62.0 | 87.0 |
| 2014 | 7 | FMDCP | 83.0 | 97.0 | 88.0 | 94.0 |
| 2015 | 8 | FMDCP | 87.5 | 95.5 | 84.9 | 96.7 |
| 2015 | 9 | FMDCP | 73.5 | 87.8 | 65.3 | 86.0 |
| 2016 | 10 | FMDCP | 70.6 | 82.9 | 59.1 | 75.8 |
| 2016 | 11 | FMDCP | 67.9 | 82.0 | 63.0 | 78.0 |
| 2017 | 12 | FMDCP | 75.0 | 88.0 | 88.0 | 90.0 |
| 2017 | 13 | FMDCP | 52.5 | 69.7 | 45.8 | 61.2 |
| 2018 | 14 | FMDCP | 47.4 | 64.8 | 41.8 | 56.1 |
| 2021 | 1 | NADCP | 16.3 | 45.2 | 12.3 | 33.3 |
| 2022 | 2 | NADCP | 50.0 | 85.5 | 45.2 | 84.1 |

Summary stats from the API: prevac O% range = 16.3–87.5 (mean 56.9), postvac O% range = 45.2–97.0 (mean 74.3).

### From dataset 0041 (Livestock Census) — Karnataka's top 5 bovine districts

From `4_get_data(dataset_id="0041", table_name="ka-district-livestock-pop-2019")`. 30 rows returned.

| District | Cattle | Buffalo | Sheep | Goat |
|----------|--------|---------|-------|------|
| BELAGAVI | 549,540 | 844,171 | 757,679 | 701,741 |
| HASSAN | 548,185 | 107,971 | 199,387 | 129,058 |
| SHIVAMOGGA | 518,653 | 120,563 | 42,526 | 59,719 |
| MYSURU | 492,598 | 21,682 | 203,463 | 208,206 |
| TUMAKURU | 431,251 | 142,047 | 1,290,008 | 427,926 |

Summary stats from the API: cattle range = 71,684–549,540 (mean 282,300), buffalo range = 1,832–844,171 (mean 99,485).

### From dataset 0089 (Serosurveillance) — Karnataka over time

From `4_get_data(dataset_id="0089", table_name="serosurveillance", filters={"state.name": "Karnataka"})`. 7 rows returned.

| Year | Samples | Seropositive % | Test |
|------|---------|----------------|------|
| 2013 | 2,991 | 21.1 | DIVA |
| 2014 | 6,002 | 33.22 | DIVA |
| 2015 | 6,006 | 34.15 | DIVA |
| 2016 | 5,973 | 30.8 | DIVA |
| 2018 | 5,979 | 23.0 | DIVA |
| 2021 | 2,099 | 20.72 | DIVA |
| 2022 | 1,663 | 36.0 | DIVA |

In 2022, cattle-specific: 37.5% positive (n=1,261), buffalo-specific: 30.5% positive (n=402).

## The AI's synthesized insight

**No single API call produces this.** The AI connected:

1. **Seromonitoring** shows vaccination is working — post-vac antibody levels consistently exceed pre-vac levels (mean jump from 56.9% to 74.3% for type O)
2. **Serosurveillance** shows natural exposure remains significant (20–36% seropositive across years), meaning the virus is still circulating despite vaccination
3. **Livestock census** identifies that Belagavi alone has 1.39 million bovines (549K cattle + 844K buffalo) — more than most districts combined — making it the highest-risk district for any outbreak

The cross-dataset connection: *Karnataka's vaccination builds immunity (0087), but the virus persists in the population (0089), concentrated in districts with massive livestock density (0041).*

## Going deeper

This example demonstrates cross-dataset reasoning for Karnataka. The [Complex investigations](Complex/README.md) take it nationwide:

- [COVID Damage Forensics](Complex/05_covid_damage_forensics.md) -- extends this analysis to all 19 comparable states and quantifies the pandemic immunity crash
- [Myth Debunker](Complex/07_myth_debunker.md) -- classifies all 35 states as GREEN/YELLOW/RED using both seromonitoring and serosurveillance
- [FMD Risk Model](Complex/08_risk_model.md) -- builds a composite scoring model from the same three datasets used here

## Datasets used

- `0087` — FMD Nationwide Seromonitoring Data (238 rows, 14 columns)
- `0089` — FMD Nationwide Serosurveillance Data (202 rows, 11 columns)
- `0041` — 20th Livestock Census 2019 (30 rows for Karnataka districts)
