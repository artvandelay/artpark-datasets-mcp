# Ambitious Investigation Ideas for ARTPARK MCP

Five investigation ideas designed to showcase what an AI can do with structured public health data that would be impractical or impossible through manual data analysis. Each idea is ranked by "wow factor" and comes with concrete instructions that can be handed to any LLM with ARTPARK MCP tool access.

> **Status:** All 5 ideas have been executed. See the [reports](README.md).

---

## Idea 1: "One Health Hypothesis Test" -- Does livestock density predict dengue hotspots?

**Why it's a showstopper:** This crosses the human-animal health boundary. You have dengue (human disease, dataset 0015) and livestock census (animal populations, dataset 0041) for the **same 30 Karnataka districts**. The One Health thesis says they're connected -- livestock means standing water, standing water means mosquitoes, mosquitoes mean dengue. Nobody has tested this with this data.

**Instructions for the AI:**

```
Using the ARTPARK MCP tools:

1. Pull ALL dengue data for Karnataka (dataset 0015, table ka-dengue-daily-summary). 
   Get total positive cases per district across all years.

2. Pull ALL livestock census data for Karnataka (dataset 0041, table 
   ka-district-livestock-pop-2019). Get total livestock (cattle + buffalo + 
   sheep + goat) per district.

3. For each of the 30 districts, compute:
   - Total dengue positives (summed across all dates)
   - Total livestock population
   - Livestock density rank vs dengue burden rank

4. Answer: Do districts with more livestock have more dengue? 
   Compute the Spearman rank correlation. Name the districts that 
   support or violate the hypothesis. If the correlation is weak, 
   explain what confounders might exist (urbanization, reporting bias, etc.)

5. Present findings as a data table + narrative verdict.
```

**Why it's hard without AI:** You'd need to join two completely different datasets, aggregate at the district level, compute a statistical measure, and reason about confounders -- all in one go.

---

## Idea 2: "COVID Damage Forensics" -- How badly did the pandemic break India's FMD program?

**Why it's a showstopper:** The Karnataka data shows a terrifying immunity crash between 2018 and 2021. But that's *one state*. There are 35 states in the seromonitoring data. This is a nationwide forensic audit of pandemic-era damage that nobody has published.

**Instructions for the AI:**

```
Using the ARTPARK MCP tools:

1. Pull ALL seromonitoring data (dataset 0087, no state filter). 238 rows, 
   35 states.

2. For EVERY state that has data in both 2018 (or latest pre-COVID year) 
   and 2021 (first post-COVID year), compute:
   - Pre-COVID post-vaccination O% (last available pre-2020 round)
   - Post-COVID pre-vaccination O% (first available 2021+ round)
   - The "immunity crash" = difference between these two numbers

3. Rank all states by severity of immunity crash.

4. Answer:
   - Which 5 states lost the most immunity?
   - Did ANY state maintain or improve immunity through COVID? (That would 
     mean they kept vaccinating)
   - What's the nationwide average immunity loss?
   - How many total livestock-rounds of immunity were lost? (Cross-reference 
     with dataset 0041 for animal counts)

5. Frame it as a "COVID Damage Report" with a headline finding.
```

---

## Idea 3: "Needle in a Haystack" -- Find the single most anomalous vaccination result in India

**Why it's a showstopper:** Classic AI detective work. Across 238 seromonitoring records (35 states, multiple years), find the ONE result that makes no sense -- where vaccination appears to have *decreased* immunity, or where a state's numbers defy all neighboring states.

**Instructions for the AI:**

```
Using the ARTPARK MCP tools:

1. Pull ALL 238 seromonitoring records (dataset 0087, no filters).

2. Scan every row. Flag anomalies:
   a. "Vaccination failure": post-vac % LOWER than pre-vac % (for type O or A)
   b. "Impossible recovery": pre-vac % above 90% (suggesting near-universal 
      prior exposure or data error)  
   c. "Outlier state": a state whose trajectory dramatically differs from 
      all neighbors in the same round
   d. "Suspicious consistency": identical percentages across different 
      serotypes (suggesting data was copied rather than measured)

3. For each anomaly found, explain:
   - What the numbers are
   - Why it's suspicious
   - What the most likely explanation is (data error? sampling bias? 
     genuine biological phenomenon?)

4. Crown the single most anomalous data point in the entire dataset and 
   explain why.
```

---

## Idea 4: "Myth Debunker" -- Is India's FMD vaccination program actually working nationwide?

**Why it's a showstopper:** The existing examples only look at Karnataka and conclude "vaccination is working." But is that true for ALL of India? This is the contrarian take -- find the states where the program is *failing* and nobody is talking about it.

**Instructions for the AI:**

```
Using the ARTPARK MCP tools:

1. Pull ALL seromonitoring data (dataset 0087, 238 rows, 35 states).
2. Pull ALL serosurveillance data (dataset 0089, 202 rows).

3. For each state, compute a "program effectiveness score":
   - Average (post-vac % minus pre-vac %) across all rounds -- the 
     "vaccination boost"
   - Trend: is the boost getting bigger or smaller over time?
   - Serosurveillance check: is natural infection going down over the years?

4. Classify every state:
   - GREEN: vaccination boost is strong AND natural infection declining
   - YELLOW: vaccination boost is moderate OR mixed trends
   - RED: vaccination boost is weak OR natural infection increasing despite 
     vaccination

5. The myth to test: "India's FMD vaccination program is a nationwide 
   success." 
   
   Verdict: How many states are GREEN vs RED? Name the failures. Is the 
   program working for India, or just for a few star states like Karnataka?
```

---

## Idea 5: "Build a District Risk Model" -- Predict the next FMD outbreak hotspot

**Why it's a showstopper:** The AI doesn't just query data -- it builds an actual scoring model, combining all available signals into a single risk number per district/state. This is the "AI as epidemiologist" demo.

**Instructions for the AI:**

```
Using the ARTPARK MCP tools, build an FMD outbreak risk score:

1. Pull the latest seromonitoring data per state (dataset 0087) -- 
   get most recent post-vac O% and A%
2. Pull 2022 serosurveillance per state (dataset 0089) -- get 
   seroprevalence (natural infection rate)
3. Pull Karnataka livestock census (dataset 0041) -- get total 
   bovine population per district
4. Pull vaccination progress data (dataset 0055) -- get completion rates

5. Define a risk score formula:
   Risk = (Natural_Infection_Rate × Livestock_Density) / Vaccination_Immunity
   
   Where:
   - Natural infection = seroprevalence from 0089
   - Livestock density = total bovines from 0041
   - Vaccination immunity = latest post-vac % from 0087

6. Rank districts/states by risk score.

7. Present: "The 5 highest-risk locations for an FMD outbreak in India" 
   with the data behind each ranking.

8. Bonus: If Karnataka is the only state with district-level livestock 
   data, do the district-level model for Karnataka and state-level for 
   the rest of India. Acknowledge the data limitation.
```

---

## Execution results

All 5 ideas were built and the reports are available:

| Idea | Report | Key Finding |
|------|--------|-------------|
| 1. One Health | [04_one_health_hypothesis.md](04_one_health_hypothesis.md) | Hypothesis rejected (r = +0.01) |
| 2. COVID Forensics | [05_covid_damage_forensics.md](05_covid_damage_forensics.md) | -32.8pp avg nationwide crash |
| 3. Needle in Haystack | [06_needle_in_haystack.md](06_needle_in_haystack.md) | Nagaland 2021: vaccination halved immunity |
| 4. Myth Debunker | [07_myth_debunker.md](07_myth_debunker.md) | Only 4/35 states GREEN |
| 5. Risk Model | [08_risk_model.md](08_risk_model.md) | AP, Bihar, Gujarat highest risk |