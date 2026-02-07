# ARTPARK Public Data MCP Server

MCP (Model Context Protocol) server for accessing ARTPARK's public health datasets through AI assistants. Built with FastMCP 3.0, following the architecture of [esankhyiki-mcp](https://github.com/nso-india/esankhyiki-mcp).

**8 datasets** covering Dengue epidemiology, Livestock census, FMD vaccination & surveillance, and administrative geospatial data from [ARTPARK DSIH](https://health.artpark.ai/data/).

---

## Quick Start

```bash
# Clone with submodules
git clone --recurse-submodules <repo-url>
cd onehealth-artpark-mcp

# Create environment and install
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Run
python artpark_server.py
# → MCP:    http://localhost:8000/mcp
# → Health: http://localhost:8000/health
```

Or with Make:

```bash
make run          # Start MCP server
make test         # Run 40 tests (~2s)
make check        # Verify datasets + tools load
make docker-up    # Start server + Jaeger tracing
make help         # Show all commands
```

---

## Datasets

| ID | Name | Category | Rows | Tables |
|----|------|----------|------|--------|
| **0015** | Karnataka Dengue Daily Summary (2017-2024) | Epidemiology | 76,114 | 1 |
| **0034** | Local Government Directory Region IDs | Geospatial | 147,423 | 1 |
| **0041** | 20th Livestock Census (2019) | Census | 30+ per table | 4 (+11 state-level) |
| **0055** | FMD NADCP Vaccination Progress (Rounds 1-6) | Epidemiology | 930-588/round | 6 |
| **0059** | FMD NADCP Vaccination Schedule (Rounds 3-6) | Epidemiology | varies | 4 |
| **0086** | FMD Nationwide Vaccination Data | Epidemiology | varies | 1 |
| **0087** | FMD Nationwide Seromonitoring Data | Epidemiology | 238 | 1 |
| **0089** | FMD Nationwide Serosurveillance Data | Epidemiology | varies | 1 |

Data source: [dsih-artpark/publicdata](https://github.com/dsih-artpark/publicdata) | Docs: [publicdata.readthedocs.io](https://publicdata.readthedocs.io)

---

## MCP Tools (4-Step Workflow)

```
1_know_about_artpark_data  →  2_get_tables  →  3_get_metadata  →  4_get_data
```

| Step | Tool | Description |
|------|------|-------------|
| 1 | `1_know_about_artpark_data()` | Overview of all 8 datasets. Start here. |
| 2 | `2_get_tables(dataset_id)` | List tables (CSVs) in a dataset |
| 3 | `3_get_metadata(dataset_id, table_name)` | Column schema + filterable values (MANDATORY before step 4) |
| 4 | `4_get_data(dataset_id, table_name, filters)` | Fetch data with optional filters |

**Important:** Tools must be called in order. Skipping `3_get_metadata` means you won't know valid column names or filter values.

---

## What Can an AI Do With This?

The [`examples/Complex/`](examples/Complex/) folder contains five investigations that were **executed entirely by an AI** using this MCP server -- no human analyst, no Jupyter notebooks, no code written. Each one demonstrates a capability that goes beyond data retrieval:

| Investigation | What the AI Did | Key Finding |
|--------------|----------------|-------------|
| [One Health Hypothesis](examples/Complex/04_one_health_hypothesis.md) | Joined dengue + livestock data across 17 districts, computed Spearman correlation | Livestock doesn't predict dengue (r = +0.01) |
| [COVID Damage Forensics](examples/Complex/05_covid_damage_forensics.md) | Compared pre/post-COVID immunity for 19 states, ranked crash severity | Average -32.8pp immunity loss nationwide |
| [Needle in a Haystack](examples/Complex/06_needle_in_haystack.md) | Scanned 238 rows for 4 anomaly categories, crowned a winner | Nagaland 2021: vaccination *halved* immunity |
| [Myth Debunker](examples/Complex/07_myth_debunker.md) | Classified all 35 states as GREEN/YELLOW/RED using 2 datasets | Only 4 states (11%) show clear success |
| [FMD Risk Model](examples/Complex/08_risk_model.md) | Built a 3-component scoring formula, ranked 20 states | AP, Bihar, Gujarat are highest risk |

> Read the [full series README](examples/Complex/README.md) for the narrative arc connecting all five.

---

## Quick Examples

### 1. Dengue Outbreak Analysis in Karnataka

> "How many dengue cases were reported in Bengaluru Urban?"

```python
# Step 1: Find the right dataset
overview = await client.call_tool("1_know_about_artpark_data", {})
# → Dataset 0015: "Karnataka Dengue Daily Summary (2017-2024)"

# Step 2: See what tables are available
tables = await client.call_tool("2_get_tables", {
    "dataset_id": "0015",
    "user_query": "dengue cases by district"
})
# → Table: ka-dengue-daily-summary (28 columns)

# Step 3: Get column schema and filter values
meta = await client.call_tool("3_get_metadata", {
    "dataset_id": "0015",
    "table_name": "ka-dengue-daily-summary"
})
# → 76,114 rows, columns include daily.suspected, daily.positive.total, daily.deaths

# Step 4: Fetch Bengaluru data
data = await client.call_tool("4_get_data", {
    "dataset_id": "0015",
    "table_name": "ka-dengue-daily-summary",
    "filters": {"location.admin2.name": "Bengaluru Urban"},
    "limit": 50
})
# → 4,942 records, positive cases: min=0, max=1070, mean=7.49
```

### 2. Livestock Population Comparison Across Districts

> "Which Karnataka districts have the most cattle?"

```python
data = await client.call_tool("4_get_data", {
    "dataset_id": "0041",
    "table_name": "ka-district-livestock-pop-2019",
    "limit": 30
})
# Results (top 5 by cattle population):
#   BELAGAVI:   cattle=549,540  buffalo=844,171  sheep=757,679
#   HASSAN:     cattle=548,185  buffalo=107,971  sheep=199,387
#   SHIVAMOGGA: cattle=518,653  buffalo=120,563  sheep=42,526
#   MYSURU:     cattle=492,598  buffalo=21,682   sheep=203,463
#   TUMAKURU:   cattle=431,251  buffalo=142,047  sheep=1,290,008
```

### 3. FMD Vaccine Efficacy Tracking

> "How has FMD seromonitoring changed in Karnataka over the years?"

```python
data = await client.call_tool("4_get_data", {
    "dataset_id": "0087",
    "table_name": "seromonitoring",
    "filters": {"state.name": "KARNATAKA"},
    "limit": 20
})
# Results (antibody levels over time):
#   2011: PostVac A%=15.0, PostVac O%=56.0  (FMDCP)
#   2012: PostVac A%=27.0, PostVac O%=67.0  (FMDCP)
#   2013: PostVac A%=78.7, PostVac O%=62.1  (FMDCP)
#   → Shows improving seroconversion rates for type A
```

### 4. Administrative Region Lookup

> "Look up LGD codes for Indian administrative units"

```python
data = await client.call_tool("4_get_data", {
    "dataset_id": "0034",
    "table_name": "regionids",
    "filters": {"regionName": "PUNE"},
    "limit": 5
})
# → regionID: district_490, regionName: PUNE, parentID: state_27
# 147,423 total regions (states, districts, subdistricts, villages, ULBs)
```

### 5. FMD Vaccination Progress by Round

> "Show me the latest FMD vaccination round progress in Karnataka"

```python
data = await client.call_tool("4_get_data", {
    "dataset_id": "0055",
    "table_name": "round6",
    "filters": {"district.name": "Bengaluru Urban"},
    "limit": 10
})
# → 588 daily progress records for Round 6
# Sample: date=2024-11-28, cattle_vaccinated=9, buffalo_vaccinated=0
```

---

## Connecting from Code

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/mcp") as client:
        # Step 1: Discover datasets
        overview = await client.call_tool("1_know_about_artpark_data", {})
        print(overview.content[0].text)

        # Step 2-4: Follow the workflow...

asyncio.run(main())
```

### Connecting from Claude Desktop

Add to your Claude Desktop MCP config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "artpark": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Then ask Claude: *"What are the top dengue-affected districts in Karnataka?"*

### Connecting from Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "artpark-health": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

---

## Deployment

### Docker

```bash
docker build -t artpark-mcp .
docker run -d -p 8000:8000 --name artpark-server artpark-mcp
```

### Docker Compose (with Jaeger tracing)

```bash
docker-compose up -d
# Server: http://localhost:8000/mcp
# Jaeger UI: http://localhost:16686
```

---

## Architecture

```
artpark_server.py          # FastMCP server — 4 tools, LLM-optimized docstrings
artpark/
  client.py                # Local data reader — reads CSV + metadata.yaml
observability/
  telemetry.py             # OpenTelemetry middleware (from esankhyiki-mcp)
publicdata/                # Cloned data repo (dsih-artpark/publicdata)
  data/
    0015/                  # Each dataset: CSV files + metadata.yaml
    0034/
    0041/
    ...
```

### Design Principles (inherited from esankhyiki-mcp)

| Principle | Implementation |
|-----------|---------------|
| **Sequential workflow** | Numbered tool prefixes (`1_`, `2_`, `3_`, `4_`) enforce order |
| **LLM-optimized docstrings** | `RULES (MUST follow exactly)` blocks prevent hallucinated queries |
| **metadata.yaml as source of truth** | Column schemas from YAML, not hardcoded |
| **Response guidance** | `_next_step` and `_retry_hint` keys steer the LLM |
| **Case-insensitive filtering** | "Mysuru" matches "MYSURU" in the data |

---

## Credits

- **Data**: [ARTPARK Data Science Innovation Hub (DSIH)](https://health.artpark.ai/data/), IISc Bengaluru
- **Architecture**: Adapted from [nso-india/esankhyiki-mcp](https://github.com/nso-india/esankhyiki-mcp) (MoSPI MCP Server)
- **Framework**: [FastMCP 3.0](https://gofastmcp.com)
- **Protocol**: [Model Context Protocol](https://modelcontextprotocol.io)
