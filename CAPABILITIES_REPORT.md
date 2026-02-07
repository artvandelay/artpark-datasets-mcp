# ARTPARK MCP Server - Capabilities Report

**Generated:** February 7, 2026
**Server:** http://127.0.0.1:8000/mcp
**Data Source:** [dsih-artpark/publicdata](https://github.com/dsih-artpark/publicdata)
**Architecture:** Adapted from [nso-india/esankhyiki-mcp](https://github.com/nso-india/esankhyiki-mcp)

---

## Overview

This MCP server provides AI-ready access to **8 ARTPARK public health datasets** covering dengue epidemiology, livestock census, FMD vaccination & surveillance, and geospatial administrative data. It enables natural language queries through Claude, ChatGPT, Cursor, or any MCP-compatible client.

---

## Available Datasets

| ID | Name | Category | Rows | Tables | Status |
|----|------|----------|------|--------|--------|
| **0015** | Karnataka Dengue Daily Summary (2017-2024) | Epidemiology | 76,114 | 1 | Verified |
| **0034** | Local Government Directory Region IDs | Geospatial | 147,423 | 1 | Verified |
| **0041** | 20th Livestock Census (2019) | Census | 30+ per table | 4 (+11 state-level) | Verified |
| **0055** | FMD NADCP Vaccination Progress (Rounds 1-6) | Epidemiology | 930-588/round | 6 | Verified |
| **0059** | FMD NADCP Vaccination Schedule (Rounds 3-6) | Epidemiology | varies | 4 | Verified |
| **0086** | FMD Nationwide Vaccination Data | Epidemiology | varies | 1 | Verified |
| **0087** | FMD Nationwide Seromonitoring Data | Epidemiology | 238 | 1 | Verified |
| **0089** | FMD Nationwide Serosurveillance Data | Epidemiology | 202 | 1 | Verified |

---

## MCP Tools (4-Step Workflow)

```
1_know_about_artpark_data  →  2_get_tables  →  3_get_metadata  →  4_get_data
```

| Step | Tool | Description |
|------|------|-------------|
| 1 | `1_know_about_artpark_data()` | Overview of all 8 datasets. Start here. |
| 2 | `2_get_tables(dataset_id)` | List tables (CSVs) in a dataset |
| 3 | `3_get_metadata(dataset_id, table_name)` | Column schema + filterable values |
| 4 | `4_get_data(dataset_id, table_name, filters)` | Fetch data with optional filters |

---

## Verified Capabilities

### Single-Dataset Queries

| Query Type | Example | Dataset | Verified |
|-----------|---------|---------|----------|
| District-level dengue cases | "Dengue cases in Bengaluru Urban" | 0015 | Yes |
| Livestock population by district | "Cattle population in Belagavi" | 0041 | Yes |
| FMD seromonitoring by state | "Karnataka FMD antibody levels" | 0087 | Yes |
| Serosurveillance trends | "FMD seroprevalence in 2022" | 0089 | Yes |
| Administrative region lookup | "LGD code for Pune" | 0034 | Yes |

### Cross-Dataset Reasoning (demonstrated in examples/)

| Capability | Datasets Used | Report |
|-----------|--------------|--------|
| Hypothesis testing with statistical correlation | 0041 + 0015 | [One Health](examples/Complex/04_one_health_hypothesis.md) |
| Nationwide temporal forensic audit | 0087 | [COVID Forensics](examples/Complex/05_covid_damage_forensics.md) |
| Anomaly detection across 238 records | 0087 | [Needle in Haystack](examples/Complex/06_needle_in_haystack.md) |
| Multi-dataset classification of 35 states | 0087 + 0089 | [Myth Debunker](examples/Complex/07_myth_debunker.md) |
| Composite risk scoring model | 0087 + 0089 + 0041 + 0015 | [Risk Model](examples/Complex/08_risk_model.md) |

### Key Design Features

| Feature | Implementation | Benefit |
|---------|---------------|---------|
| Sequential workflow enforcement | Numbered tool prefixes (`1_`, `2_`, `3_`, `4_`) | Prevents LLM from skipping metadata |
| LLM-optimized docstrings | `RULES (MUST follow exactly)` blocks | Reduces hallucinated queries |
| Case-insensitive filtering | `str.lower()` comparison | "Mysuru" matches "MYSURU" |
| Response guidance | `_next_step` and `_retry_hint` keys | Steers LLM through workflow |
| Summary statistics | Auto-computed min/max/mean for numeric columns | LLM can reason without scanning rows |
| Filter value enumeration | Unique values returned in `3_get_metadata` | LLM uses exact values, not guesses |

---

## Known Limitations

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| Dataset 0055 merged table not directly accessible | Risk model couldn't include vaccination coverage | Used 0087 + 0089 instead |
| No district-level FMD data outside Karnataka | Risk model is state-level for most of India | Acknowledged in methodology |
| Summary stats cap at 10 numeric columns | Large tables may omit some stats | Increase cap in `client.py` if needed |
| `postvac.positive.asia1.pct` stored as string | May cause type errors in analysis | Cast to float before computation |

---

## Summary

| Metric | Value |
|--------|-------|
| Total Datasets | 8 |
| MCP Tools | 4 |
| Total data rows accessible | ~225,000+ |
| Cross-dataset investigations completed | 5 |
| Framework | FastMCP 3.0 + OpenTelemetry |
| Data source | ARTPARK DSIH, IISc Bengaluru |
