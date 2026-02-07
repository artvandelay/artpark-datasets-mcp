# Why This MCP Server Matters

**A CSV API gives you rows. An LLM + MCP gives you insight.**

These examples show what becomes possible when an AI assistant like Claude has live access to ARTPARK's public health datasets through MCP — capabilities that were **never possible** with a traditional data API alone.

---

## What's Different?

| Traditional API | LLM + MCP Server |
|----------------|-----------------|
| Returns rows matching a filter | **Reasons** about what the numbers mean |
| One dataset at a time | **Connects** findings across datasets automatically |
| You write the analysis code | **Discovers** patterns you didn't think to look for |
| Static query → static answer | **Builds narratives** that explain *why* something matters |
| Requires domain expertise upfront | **Surfaces** domain insights for non-experts |

### The key unlock:

> You can ask a **question in plain English** that spans multiple datasets, time periods, and domains — and get back a **synthesized analysis** with policy implications, not just a JSON blob.

---

## All Examples

### Foundations (single-conversation demos)

| # | Title | Question | Datasets | Key Demo |
|---|-------|----------|----------|----------|
| [01](01_cross_dataset_reasoning.md) | **Cross-Dataset Reasoning** | *"Is India's FMD vaccination program working?"* | 0087 + 0089 + 0041 | Joins 3 datasets autonomously |
| [02](02_temporal_narrative.md) | **Temporal Narrative** | *"Tell me the story of Karnataka's FMD vaccination journey."* | 0087 + 0089 | Constructs narrative arc from numbers |
| [03](03_hidden_patterns.md) | **Hidden Pattern Discovery** | *"Any surprising differences in FMD across livestock types?"* | 0089 | Discovers cattle-buffalo disparity |
| [04](04_policy_intelligence.md) | **One Health Policy Intelligence** | *"Where should Karnataka prioritize its next FMD vaccination?"* | 0087 + 0089 + 0041 | Generates ranked policy recommendations |

### Advanced (autonomous multi-step investigations)

| # | Title | Question | Datasets | Key Finding |
|---|-------|----------|----------|-------------|
| [05](Complex/04_one_health_hypothesis.md) | **One Health Hypothesis** | *"Does livestock density predict dengue?"* | 0041 + 0015 | No correlation (r = +0.01) |
| [06](Complex/05_covid_damage_forensics.md) | **COVID Damage Forensics** | *"How badly did COVID break India's FMD program?"* | 0087 | -32.8pp avg crash, 19 states |
| [07](Complex/06_needle_in_haystack.md) | **Needle in a Haystack** | *"Find the most anomalous result in India's FMD data."* | 0087 | Nagaland: vaccination halved immunity |
| [08](Complex/07_myth_debunker.md) | **Myth Debunker** | *"Is India's FMD program a nationwide success?"* | 0087 + 0089 | Only 4/35 states GREEN |
| [09](Complex/08_risk_model.md) | **FMD Risk Model** | *"Rank every state by FMD outbreak risk."* | 0087 + 0089 + 0041 + 0015 | AP, Bihar, Gujarat highest risk |

> **Executive summary of all 5 advanced investigations:** [Complex/EXECUTIVE_SUMMARY.md](Complex/EXECUTIVE_SUMMARY.md)
>
> **Full series with methodology and cross-references:** [Complex/README.md](Complex/README.md)

---

## The Pitch for 60+ More Datasets

ARTPARK DSIH has **60+ datasets** spanning human health, animal health, climate, and geospatial data. Only 8 are currently connected to this MCP server.

Imagine what becomes possible with more:

- **"Is there a correlation between monsoon rainfall patterns and dengue outbreaks in Karnataka districts?"** *(climate + epidemiology)*
- **"Which districts have both high livestock density and high human disease burden?"** *(census + epidemiology + geospatial)*
- **"How did COVID lockdowns affect FMD vaccination coverage, and has it recovered?"** *(vaccination progress + temporal analysis)*
- **"Map the overlap between FMD seroprevalence hotspots and livestock trade routes."** *(serosurveillance + geospatial + census)*

Each new dataset doesn't just add one more query — it creates **combinatorial connections** with every existing dataset. 8 datasets give you 28 possible pairings. 60 datasets give you **1,770**.

That's the power of LLM + structured data access. Not querying — **thinking**.

---

## Advanced: Complex Multi-Dataset Investigations

The examples above show single-conversation capabilities. The [`Complex/`](Complex/) folder takes it further -- five autonomous investigations where the AI:

- **Tests a cross-domain hypothesis** (dengue + livestock correlation)
- **Conducts a nationwide forensic audit** (COVID immunity crash across 19 states)
- **Hunts anomalies** across 238 records to find the single most suspicious data point
- **Debunks a policy myth** using two independent datasets
- **Builds a predictive risk model** combining all available data

Each investigation is a full markdown report with data tables, statistical analysis, methodology notes, and cross-references to the other investigations.

> **Start here:** [Complex/README.md](Complex/README.md)

---

## How to Reproduce These Examples

1. Start the MCP server: `python artpark_server.py`
2. Connect from Claude Desktop, Cursor, or any MCP client
3. Ask the questions shown in each example
4. Watch the AI navigate the 4-step workflow autonomously

The responses will vary slightly (LLMs are non-deterministic), but the **cross-dataset reasoning** is consistent and reproducible.
