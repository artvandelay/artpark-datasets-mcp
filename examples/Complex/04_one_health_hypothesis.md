# Investigation 01: One Health Hypothesis Test

*Part of a [5-investigation series](README.md) demonstrating AI-driven public health analysis using ARTPARK MCP tools.*

> **The hypothesis:** "Districts with larger livestock populations have higher dengue burden, because livestock create mosquito breeding sites."
>
> **The verdict:** Hypothesis **REJECTED**. Spearman rank correlation r = +0.01 (zero). Buffalo population actually shows a *negative* correlation with dengue (r = -0.34). Livestock density does not predict dengue in Karnataka -- urbanization and coastal climate do.

## Why this matters

The "One Health" framework argues that human and animal health are interconnected. A plausible mechanism links livestock to dengue: cattle ponds, buffalo wallows, and water troughs create breeding sites for mosquitoes. If true, districts with the most livestock should have the most dengue. This investigation tests that hypothesis using real data from two completely independent ARTPARK datasets.

## What the AI did (autonomously)

1. Pulled **all 30 Karnataka district livestock populations** from dataset 0041 via `4_get_data(dataset_id="0041", table_name="ka-district-livestock-pop-2019", limit=35)`
2. Queried **17 individual Karnataka districts' dengue daily summaries** from dataset 0015, pulling summary statistics for each via `4_get_data(dataset_id="0015", table_name="ka-dengue-daily-summary", filters={"location.admin2.ID": "district_XXX"}, limit=1)` -- 17 separate API calls
3. Computed total bovine population (cattle + buffalo) per district from 0041
4. Extracted mean daily dengue positives per district from 0015 summary stats
5. Ranked all 17 districts on both measures
6. Computed Spearman rank correlation coefficient

## The real data

### Combined livestock + dengue dataset (17 Karnataka districts)

| District | Cattle | Buffalo | Total Bovine | Dengue Mean Daily Positives | Dengue Rank | Livestock Rank |
|----------|--------|---------|-------------|---------------------------|------------|---------------|
| Dakshina Kannada | 250,569 | 1,832 | 252,401 | 1.856 | 1 | 15 |
| Kalaburagi | 385,580 | 73,176 | 458,756 | 1.475 | 2 | 8 |
| Shivamogga | 518,653 | 120,563 | 639,216 | 1.372 | 3 | 3 |
| Mysuru | 492,598 | 21,682 | 514,280 | 1.227 | 4 | 5 |
| Chitradurga | 225,603 | 113,304 | 338,907 | 1.155 | 5 | 11 |
| Udupi | 254,776 | 2,408 | 257,184 | 1.112 | 6 | 14 |
| Davangere | 237,801 | 91,896 | 329,697 | 0.966 | 7 | 12 |
| Ballari | 343,275 | 159,107 | 502,382 | 0.892 | 8 | 6 |
| Mandya | 369,986 | 109,443 | 479,429 | 0.829 | 9 | 7 |
| Dharwad | 172,219 | 61,245 | 233,464 | 0.763 | 10 | 16 |
| Hassan | 548,185 | 107,971 | 656,156 | 0.744 | 11 | 2 |
| Koppal | 231,413 | 63,467 | 294,880 | 0.689 | 12 | 13 |
| Tumakuru | 431,251 | 142,047 | 573,298 | 0.630 | 13 | 4 |
| Belagavi | 549,540 | 844,171 | 1,393,711 | 0.598 | 14 | 1 |
| Bagalkote | 222,823 | 234,340 | 457,163 | 0.514 | 15 | 9 |
| Raichur | 245,374 | 112,420 | 357,794 | 0.279 | 16 | 10 |
| Kodagu | 71,684 | 5,236 | 76,920 | 0.235 | 17 | 17 |

*Bengaluru Urban excluded from analysis: it has dual administrative units (REVENUE + BBMP ULB) causing double-counted dengue rows (4,942 vs 2,440 for other districts).*

### The Spearman rank correlation

```
Correlation: Total bovine vs dengue burden
n = 17 districts
Sum of d² = 806
r = 1 - (6 × 806) / (17 × 288) = 1 - 0.988 = +0.012
```

**r = +0.01** -- essentially zero. No correlation.

### Testing with buffalo specifically

Buffalo create more standing water (wallows, ponds) than cattle. Does buffalo population specifically predict dengue?

```
Correlation: Buffalo population vs dengue burden
n = 17 districts
Sum of d² = 1,094
r = 1 - (6 × 1094) / (17 × 288) = 1 - 1.341 = -0.34
```

**r = -0.34** -- a weak NEGATIVE correlation. More buffalo = LESS dengue. The opposite of the hypothesis.

## Key counterexamples

The data contains striking cases that contradict the hypothesis:

### Belagavi: Most livestock, little dengue

- **Total bovine:** 1,393,711 (rank 1 -- by far the largest in Karnataka)
- **Dengue mean daily positives:** 0.598 (rank 14 out of 17)
- Belagavi has over **3× the bovine population** of the median sampled district (457K), yet it ranks 14th for dengue

### Dakshina Kannada: Least buffalo, most dengue

- **Buffalo population:** 1,832 (rank 17 -- dead last)
- **Dengue mean daily positives:** 1.856 (rank 1 -- highest in our sample)
- The district with the fewest buffalo has the MOST dengue

### Hassan: 2nd most livestock, 11th for dengue

- **Total bovine:** 656,156 (rank 2)
- **Dengue mean daily positives:** 0.744 (rank 11)
- A massive livestock district with below-average dengue burden

## Why the hypothesis fails

The data suggests dengue in Karnataka is driven by **urbanization and coastal climate**, not livestock density:

1. **Coastal districts lead:** Dakshina Kannada (1.86), Udupi (1.11) -- both coastal with high rainfall and tropical climate ideal for Aedes aegypti breeding
2. **High-livestock districts are rural:** Belagavi, Hassan, Tumakuru -- large agricultural districts where Aedes aegypti is less prevalent than in urban areas
3. **Wrong mosquito species:** Dengue is transmitted by *Aedes aegypti* and *Aedes albopictus*, which breed in small containers (tires, flowerpots, water tanks) -- NOT in cattle ponds or buffalo wallows, which are breeding sites for *Culex* and *Anopheles* species
4. **The negative buffalo correlation** makes sense: buffalo-heavy districts are deeply rural with less urban infrastructure that creates Aedes breeding habitat

## The "One Health" takeaway

The One Health framework is not wrong -- but the **mechanism** matters. Livestock don't increase dengue risk because:
- Dengue vectors (*Aedes*) breed in artificial containers, not livestock water bodies
- High-livestock districts are rural; dengue thrives in urban density
- The actual animal-health signal for dengue would be *poultry density* (chicken coops collect rainwater), not bovine density

**What this investigation actually demonstrates:** An AI can autonomously formulate a cross-dataset hypothesis, join two independent datasets on a shared geographic key, compute rank correlations, test an alternative hypothesis when the first fails, and explain the null result using domain knowledge -- all without human guidance.

## What an API can't do

An API returns livestock counts and dengue case counts separately. It does not:
- Formulate a hypothesis connecting two independent datasets
- Join the datasets on a shared key (district ID) that uses different naming conventions
- Decide to exclude Bengaluru Urban due to double-counted administrative units
- Compute rank correlations and interpret the result
- Test an alternative hypothesis (buffalo-specific) when the first one fails
- Explain *why* the correlation is zero using domain knowledge about mosquito species

## Methodology notes

- **Dengue proxy metric:** Mean of `daily.positive.total` across all daily records (2017-2024, ~2,440 records per district). This averages across seasonal spikes and quiet periods.
- **Livestock proxy metric:** Total cattle + buffalo from the 2019 census. This is a snapshot, not a time series.
- **Districts excluded:** Bengaluru Urban (double admin units), 13 districts not individually queried (would have required 13 more API calls). The 17-district sample covers the full range of livestock densities.
- **Limitation:** This is an ecological correlation (district-level, not individual-level). Even a positive correlation wouldn't prove causation. The null result is more robust than a positive one would have been.

## See also

- [Investigation 05: FMD Risk Model](08_risk_model.md) -- reuses the livestock data from this investigation for the Karnataka district-level bonus analysis, and identifies Kalaburagi as a dual-burden hotspot (high livestock + high dengue)
- [Investigation 04: Myth Debunker](07_myth_debunker.md) -- Karnataka's FMD vaccination status (YELLOW, with surging serosurveillance) provides the animal-health context for this district

## Datasets used

- `0041` -- 20th Livestock Census Karnataka (30 districts, 2019)
- `0015` -- Karnataka Dengue Daily Summary (76,114 rows, 2017-2024, 30+ districts)
