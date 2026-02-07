# Example 04: One Health Policy Intelligence

> **The question:** "Where should Karnataka prioritize its next FMD vaccination round?"

## Why this matters

This is the question a state veterinary officer actually needs answered. It requires combining **what we know about the disease** (seromonitoring trends) with **where the animals are** (livestock census) and **what the field data says** (serosurveillance). No single dataset answers it.

## What the AI did

1. Pulled Karnataka seromonitoring history (dataset 0087) — identified that post-COVID immunity crashed
2. Pulled Karnataka district livestock census (dataset 0041) — identified population hotspots
3. Pulled Karnataka serosurveillance (dataset 0089) — identified natural infection trends
4. Combined all three to generate prioritized recommendations

## The real data

### Current immunity status (dataset 0087)

From `4_get_data(dataset_id="0087", filters={"state.name": "Karnataka"})`.

The two most recent data points:

| Year | Round | Program | PreVac O% | PostVac O% | PreVac A% | PostVac A% |
|------|-------|---------|-----------|------------|-----------|------------|
| 2021 | 1 | NADCP | 16.3 | 45.2 | 12.3 | 33.3 |
| 2022 | 2 | NADCP | 50.0 | 85.5 | 45.2 | 84.1 |

The context: Pre-vac levels jumped from 16.3% to 50.0% (type O) between rounds 1 and 2, meaning Round 1 vaccination had lasting effect. Post-vac levels in Round 2 (85.5% O, 84.1% A) are good but still below the 2014–2015 peak of 95–97%.

### Current natural infection level (dataset 0089)

From `4_get_data(dataset_id="0089", filters={"state.name": "Karnataka"})`.

| Year | Seroprevalence % |
|------|-----------------|
| 2018 | 23.0 |
| 2021 | 20.72 |
| 2022 | 36.0 |

The jump from 20.72% to 36.0% between 2021 and 2022 indicates **increased virus circulation** — the vaccination gap let the pathogen regain ground.

In 2022 specifically: cattle seroprevalence = 37.5% (n=1,261), buffalo = 30.5% (n=402).

### Where the animals are (dataset 0041)

From `4_get_data(dataset_id="0041", table_name="ka-district-livestock-pop-2019")`. 30 rows. Summary stats from API: cattle mean = 282,300 per district, buffalo mean = 99,485.

**Top districts by total bovine population (cattle + buffalo):**

| District | Cattle | Buffalo | Total Bovine | Sheep |
|----------|--------|---------|-------------|-------|
| BELAGAVI | 549,540 | 844,171 | 1,393,711 | 757,679 |
| TUMAKURU | 431,251 | 142,047 | 573,298 | 1,290,008 |
| HASSAN | 548,185 | 107,971 | 656,156 | 199,387 |
| SHIVAMOGGA | 518,653 | 120,563 | 639,216 | 42,526 |
| MANDYA | 369,986 | 109,443 | 479,429 | 347,133 |
| MYSURU | 492,598 | 21,682 | 514,280 | 203,463 |

**Districts with largest buffalo populations** (relevant because buffalo show different FMD dynamics):

| District | Buffalo |
|----------|---------|
| BELAGAVI | 844,171 |
| BAGALKOTE | 234,340 |
| VIJAYAPURA | 177,079 |
| BALLARI | 159,107 |
| TUMAKURU | 142,047 |

**Districts with largest sheep populations** (sheep are also FMD-susceptible):

| District | Sheep |
|----------|-------|
| CHITRADURGA | 1,352,087 |
| TUMAKURU | 1,290,008 |
| BALLARI | 1,272,828 |
| KOPPAL | 625,367 |
| CHIKKABALLAPURA | 613,193 |

## The AI's synthesized recommendations

Combining all three datasets:

### Priority 1: BELAGAVI

- **Why:** 1.39M bovines (highest in state by far), including 844K buffalo — the largest buffalo concentration in Karnataka
- **Risk factor:** Borders Maharashtra (state_27), which had 22.3% bovine seroprevalence in 2022 (from dataset 0089), creating cross-border transmission risk
- **Buffalo relevance:** Given the cattle-buffalo seroprevalence gap discovered in Example 03, Belagavi's massive buffalo population needs specific monitoring

### Priority 2: TUMAKURU + CHITRADURGA corridor

- **Why:** Combined 2.6M sheep (1,290,008 + 1,352,087) plus 573K bovines in Tumakuru alone
- **Risk factor:** Sheep are FMD-susceptible but often overlooked in vaccination campaigns focused on bovines
- **Data gap:** Current seromonitoring data is at state level only — district-level data would be needed to confirm if these sheep populations are being reached

### Priority 3: State-wide Round 3 urgency

- **Why:** The 2022 serosurveillance showing 36% seroprevalence (up from 20.72% in 2021) indicates virus is actively circulating
- **Positive signal:** Round 2 post-vac levels (85.5% O, 84.1% A) show the vaccine works when administered
- **Gap to close:** Still below the 2014–2015 peak (95–97%), suggesting another 1–2 rounds needed to restore full herd immunity

## What an API can't do

No single API call — or even three calls — produces a prioritized action plan. The AI:
- Connected **temporal trends** (immunity crashed post-2018) with **geographic risk** (Belagavi's border location and herd size) and **species-specific findings** (the buffalo gap)
- Identified that Tumakuru/Chitradurga's **sheep** populations are a blind spot in bovine-focused FMD campaigns
- Translated raw numbers into **ranked priorities** with specific justifications

This is policy intelligence, not data retrieval.

## Going deeper

This example generates policy recommendations for Karnataka. The [Complex investigations](Complex/README.md) go further:

- [One Health Hypothesis](Complex/04_one_health_hypothesis.md) -- tests whether livestock density also predicts *dengue* in Karnataka districts (it doesn't; r = +0.01)
- [FMD Risk Model](Complex/08_risk_model.md) -- ranks 20 states by outbreak vulnerability using a composite scoring model, and includes a Karnataka district-level bonus analysis that identifies Kalaburagi as a dual-burden hotspot

## Datasets used

- `0087` — FMD Nationwide Seromonitoring Data (16 rows for Karnataka)
- `0089` — FMD Nationwide Serosurveillance Data (7 rows for Karnataka, 27 rows for 2022 national)
- `0041` — 20th Livestock Census 2019 (30 Karnataka district rows)
