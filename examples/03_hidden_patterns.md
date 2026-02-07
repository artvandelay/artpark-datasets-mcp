# Example 03: Hidden Pattern Discovery

> **The question:** "Are there any surprising differences in FMD across livestock types?"

## Why this matters

This is the kind of question you'd only ask if you already suspected something. But the AI found this pattern **without being prompted** — it noticed the cattle vs buffalo columns in the 2022 serosurveillance data and flagged the disparity as significant.

## What the AI did

1. Fetched all 2022 serosurveillance data from dataset 0089
2. Noticed that 2022 is the only year with separate cattle and buffalo columns (confirmed by the metadata comment: *"2022 has cattle and buffalo separated, while all the other years have them together as bovine"*)
3. Compared cattle vs buffalo seroprevalence across all 27 states
4. Flagged the systematic disparity as a policy-relevant finding

## The real data

From `4_get_data(dataset_id="0089", table_name="serosurveillance", filters={"metadata.year": "2022"})`. 27 rows returned. Summary stats from API: cattle seropositive mean = 22.7%, buffalo seropositive mean = 11.3%.

### States where both cattle AND buffalo were sampled (2022)

| State | Cattle Samples | Cattle Sero+% | Buffalo Samples | Buffalo Sero+% | Gap |
|-------|---------------|---------------|-----------------|----------------|-----|
| Andhra Pradesh | 4,867 | 34.7 | 4,962 | 10.9 | **23.8pp** |
| Bihar | 1,461 | 27.9 | 724 | 27.2 | 0.7pp |
| Chhattisgarh | 1,128 | 29.8 | 119 | 8.4 | **21.4pp** |
| Gujarat | 3,323 | 26.0 | 3,330 | 2.0 | **24.0pp** |
| Haryana | 2,095 | 11.5 | 4,949 | 2.4 | **9.1pp** |
| Himachal Pradesh | 1,667 | 14.0 | 757 | 4.4 | **9.6pp** |
| Jharkhand | 1,255 | 35.8 | 32 | 9.4 | **26.4pp** |
| Karnataka | 1,261 | 37.5 | 402 | 30.5 | 7.0pp |
| Kerala | 1,767 | 18.0 | 107 | 15.0 | 3.0pp |
| Madhya Pradesh | 1,798 | 19.6 | 1,030 | 9.5 | **10.1pp** |
| Maharashtra | 2,077 | 27.1 | 850 | 10.6 | **16.5pp** |
| Manipur | 1,046 | 23.1 | 168 | 19.6 | 3.5pp |
| Mizoram | 1,075 | 19.2 | 48 | 12.5 | 6.7pp |
| Odisha | 2,144 | 29.7 | 196 | 21.9 | 7.8pp |
| Punjab | 1,488 | 28.8 | 2,331 | 13.0 | **15.8pp** |
| Rajasthan | 70 | 17.1 | 110 | 3.6 | **13.5pp** |
| Telangana | 3,729 | 9.3 | 3,911 | 5.5 | 3.8pp |
| Uttar Pradesh | 1,338 | 13.3 | 1,990 | 4.1 | **9.2pp** |
| Uttarakhand | 1,579 | 17.0 | 540 | 4.8 | **12.2pp** |

### The discovery

**In 14 out of 19 states with both species sampled, cattle seroprevalence exceeded buffalo by more than 5 percentage points.** The most extreme cases:

- **Jharkhand**: cattle 35.8% vs buffalo 9.4% (26.4pp gap, though only 32 buffalo sampled)
- **Gujarat**: cattle 26.0% vs buffalo 2.0% (24.0pp gap, with large sample sizes: 3,323 and 3,330)
- **Andhra Pradesh**: cattle 34.7% vs buffalo 10.9% (23.8pp gap, largest combined sample: 9,829)
- **Chhattisgarh**: cattle 29.8% vs buffalo 8.4% (21.4pp gap)

The **only state where buffalo seroprevalence was close to cattle was Bihar** (27.9% vs 27.2%) and **Karnataka** had the highest buffalo seroprevalence at 30.5%.

### Why this matters for policy

The DIVA test detects **natural infection** (not vaccine-induced antibodies). Lower buffalo seroprevalence could mean:

1. Buffalo are genuinely less exposed or less susceptible to FMD
2. Buffalo immune response differs (lower sensitivity to the DIVA test)
3. Buffalo are in different husbandry systems with less pathogen contact

Any of these has implications for vaccination strategy — a one-size-fits-all approach may not work for mixed cattle-buffalo herds.

## What an API can't do

An API returns these 27 rows with the cattle/buffalo columns. It does not:
- Recognize that buffalo seroprevalence being systematically lower is noteworthy
- Calculate the gap across all states and identify the pattern
- Flag Gujarat's 13:1 ratio (26% vs 2%) as the most extreme case
- Connect the finding to policy implications about differential vaccination strategies
- Note that Bihar is an anomaly worth investigating separately

## Going deeper

This example discovered the cattle-buffalo disparity. The [Complex investigations](Complex/README.md) explore related patterns:

- [Myth Debunker](Complex/07_myth_debunker.md) -- uses serosurveillance data (including this cattle/buffalo split) alongside seromonitoring to classify states as GREEN/YELLOW/RED
- [FMD Risk Model](Complex/08_risk_model.md) -- incorporates serosurveillance (virus pressure) as one of three risk components

## Datasets used

- `0089` — FMD Nationwide Serosurveillance Data (27 rows for 2022, with cattle/buffalo breakdown)
