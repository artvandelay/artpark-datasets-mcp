# Complex Investigations: What an AI Can Do with Public Health Data

> Five investigations. Four datasets. 238 seromonitoring records, 202 serosurveillance records, 76,114 dengue daily records, 30 livestock district censuses. Zero human analysts. One AI with MCP tools.

## The pitch

These five reports demonstrate what happens when you give a Large Language Model direct access to ARTPARK's public health data through the MCP server. Each investigation goes far beyond "retrieve and display" -- the AI formulates hypotheses, cross-references independent datasets, computes statistics, builds scoring models, and writes narrative reports with defensible conclusions.

Every number in these reports was pulled live from the ARTPARK DataIO API via MCP tool calls. No data was hardcoded. No results were pre-computed. The AI did the analysis autonomously.

> **Short on time?** Read the [Executive Summary](EXECUTIVE_SUMMARY.md) -- all 5 findings on one page.

## The investigations at a glance

| # | Title | Datasets | Key Finding | MCP Calls |
|---|-------|----------|-------------|-----------|
| [01](04_one_health_hypothesis.md) | **One Health Hypothesis** | 0041 + 0015 | Livestock density does NOT predict dengue (r = +0.01). Buffalo shows *negative* correlation (r = -0.34). | ~20 |
| [02](05_covid_damage_forensics.md) | **COVID Damage Forensics** | 0087 | Nationwide avg immunity crash: **-32.8pp**. Haryana lost 69.9pp. Rajasthan lost 0.1pp. | 4 |
| [03](06_needle_in_haystack.md) | **Needle in a Haystack** | 0087 | Nagaland 2021: vaccination *halved* type O immunity (13.2% → 6.0%). Lowest post-vac in all of India. | 4 |
| [04](07_myth_debunker.md) | **Myth Debunker** | 0087 + 0089 | Only 4 of 35 states (11%) show clear vaccination success. 46% of India is untested. | 6 |
| [05](08_risk_model.md) | **FMD Risk Model** | 0087 + 0089 + 0041 + 0015 | Andhra Pradesh, Bihar, Gujarat are India's top-3 FMD outbreak risks. | 6 |

## The narrative arc

The investigations tell a connected story:

1. **Investigation 01** tests whether human disease (dengue) and animal health (livestock) are linked at the district level. They're not -- but the cross-dataset join demonstrates the AI's ability to reason across domains.

2. **Investigation 02** reveals the pandemic's hidden damage: a nationwide -32.8pp immunity crash that nobody has published. The 2019-2020 data gap in the seromonitoring record is itself a finding.

3. **Investigation 03** zooms to the micro level: the single most anomalous data point in 238 rows. Nagaland's impossible result raises questions about data quality, cold chains, and sampling methodology in remote states.

4. **Investigation 04** zooms back out and asks the uncomfortable question: is the program actually working? The answer -- only 4 states are clearly succeeding -- reframes the entire narrative from "vaccination is working" to "vaccination works *where it's been done consistently for a decade*."

5. **Investigation 05** synthesizes everything into a predictive model, ranking 19 states by outbreak vulnerability. The top-3 risk states (AP, Bihar, Gujarat) aren't surprising after reading Investigations 02-04, but the model gives them a quantified risk score that policy makers can act on.

## What makes this different from a data dashboard

A dashboard shows you data. These investigations show you *reasoning*:

- **Hypothesis testing** (Investigation 01): The AI didn't just show livestock and dengue numbers side by side. It formulated a hypothesis, computed a Spearman rank correlation, tested an alternative hypothesis when the first failed, and explained the null result using entomological domain knowledge.

- **Temporal reasoning** (Investigation 02): The AI identified which specific rows to compare for each state, handled the fact that "pre-COVID" means different years for different states, and noticed that Haryana's 6-year gap is qualitatively different from Karnataka's 3-year gap.

- **Anomaly detection** (Investigation 03): The AI defined four categories of anomaly, scanned 238 rows against all four criteria simultaneously, ranked findings by severity, and provided a mechanistic explanation for the winner (sample attrition bias).

- **Multi-source triangulation** (Investigation 04): The AI cross-referenced seromonitoring (vaccine response) with serosurveillance (natural infection) -- two independent measurements of the same phenomenon -- to classify states more accurately than either dataset alone could.

- **Model design** (Investigation 05): The AI designed a scoring formula, justified its weight choices, computed risk scores for 19 states, validated the model against domain knowledge, and identified edge cases where the model gives misleading results.

## Datasets used

| ID | Name | Rows | Used In |
|----|------|------|---------|
| `0087` | FMD Nationwide Seromonitoring | 238 | Investigations 02, 03, 04, 05 |
| `0089` | FMD Nationwide Serosurveillance | 202 | Investigations 04, 05 |
| `0041` | 20th Livestock Census (Karnataka) | 30 | Investigations 01, 05 |
| `0015` | Karnataka Dengue Daily Summary | 76,114 | Investigations 01, 05 |

## How to reproduce

Each investigation can be reproduced by giving an LLM access to the ARTPARK MCP server and asking the question at the top of each report. The AI will follow the mandatory 4-step MCP workflow (`1_know → 2_get_tables → 3_get_metadata → 4_get_data`) and arrive at comparable findings, though the narrative framing may differ.

## Caveats

- All data is from ARTPARK's public datasets. The AI has no access to unpublished data.
- Statistical analyses are exploratory, not confirmatory. No multiple testing corrections were applied.
- The risk model (Investigation 05) uses heuristic weights, not empirically calibrated ones.
- Sample sizes vary dramatically across states (Delhi: 50-234 animals, Tamil Nadu: 6,400). Small-sample results should be interpreted cautiously.
- The AI's domain knowledge about FMD virology and mosquito ecology comes from its training data, not from the ARTPARK datasets themselves.
