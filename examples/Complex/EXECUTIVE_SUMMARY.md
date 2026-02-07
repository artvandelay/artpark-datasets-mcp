# AI-Driven Public Health Intelligence: Five Investigations Using ARTPARK Data

**What:** An AI assistant autonomously analyzed 4 public health datasets (225,000+ records) from ARTPARK's DataIO platform, producing 5 investigative reports without human coding or manual analysis.

**How:** The AI accessed data through an MCP (Model Context Protocol) server, following a structured 4-step workflow to discover, explore, and query datasets via natural language.

---

## Key Findings

### 1. India lost 33 percentage points of FMD vaccine immunity during COVID

The pandemic created a 3-year gap (2019-2020) in India's FMD vaccination program. Across 19 states with comparable data, the average post-vaccination immunity for FMD type O dropped from ~65% to ~32%. Five states lost more than 50 percentage points. Only Rajasthan maintained its immunity through the gap.

*Data: 238 seromonitoring records, 35 states, 2011-2022*

### 2. Only 4 of 35 Indian states show clear FMD vaccination success

The claim that "India's FMD vaccination program is a nationwide success" is false. Only Tamil Nadu, Kerala, Haryana, and Goa (11%) demonstrate strong, sustained vaccination results. Ten states (31%) show mediocre or declining performance. Twenty states (57%) are either failing or too new to assess.

*Data: 238 seromonitoring + 202 serosurveillance records cross-referenced*

### 3. Nagaland's vaccination made immunity worse, not better

In the most anomalous result in the entire dataset, Nagaland's 2021 NADCP Round 1 showed type O immunity *dropping* from 13.2% to 6.0% after vaccination -- the lowest post-vaccination percentage in all of India. A 42% sample attrition between pre- and post-vaccination testing is the likely explanation.

*Data: Anomaly scan across all 238 seromonitoring records*

### 4. Andhra Pradesh, Bihar, and Gujarat are India's highest FMD outbreak risks

A composite risk model combining immunity gaps (40% weight), virus pressure from serosurveillance (40%), and vaccine weakness (20%) identifies these three states as critically vulnerable. The ranking is robust across alternative weight schemes.

*Data: Seromonitoring + serosurveillance + livestock census*

### 5. Livestock density does NOT predict dengue in Karnataka

Testing the "One Health" hypothesis that livestock create mosquito breeding habitat, the AI found zero correlation (Spearman r = +0.01) between district-level bovine populations and dengue burden across 17 Karnataka districts. Belagavi has 6x the median livestock but ranks 14th for dengue. The explanation: dengue is transmitted by *Aedes* mosquitoes that breed in urban containers, not rural livestock water bodies.

*Data: 30 district livestock records + 76,114 daily dengue records*

---

## What This Demonstrates

| Capability | Example |
|-----------|---------|
| **Cross-dataset reasoning** | Joined dengue (human health) with livestock census (animal health) on shared district keys |
| **Temporal forensics** | Identified the COVID immunity crash by comparing 2018 and 2021 data across 19 states |
| **Anomaly detection** | Scanned 238 records against 4 anomaly categories to find the single most suspicious result |
| **Hypothesis testing** | Formulated, tested, and rejected a hypothesis with statistical correlation |
| **Predictive modeling** | Built a 3-component risk score, computed it for 20 states, validated against domain knowledge |

---

## Data Sources

All data from [ARTPARK Data Science Innovation Hub](https://health.artpark.ai/data/), IISc Bengaluru. Accessed via the ARTPARK MCP Server.

| Dataset | Records | Coverage |
|---------|---------|----------|
| FMD Seromonitoring (0087) | 238 | 35 states, 2011-2022 |
| FMD Serosurveillance (0089) | 202 | 30 states, 2013-2022 |
| Karnataka Dengue Summary (0015) | 76,114 | 30+ districts, 2017-2024 |
| Livestock Census (0041) | 30 | Karnataka districts, 2019 |

---

*Full reports with data tables, methodology, and cross-references: [examples/Complex/](README.md)*
