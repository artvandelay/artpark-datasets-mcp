"""
ARTPARK MCP Server
FastMCP server for accessing ARTPARK public health datasets.
Architecture mirrors nso-india/esankhyiki-mcp.

Datasets: 8 public datasets covering Epidemiology, Census, Geospatial
Source: https://github.com/dsih-artpark/publicdata
Docs: https://publicdata.readthedocs.io
"""

import sys
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from artpark.client import artpark_data
from observability.telemetry import TelemetryMiddleware


def log(msg: str):
    """Print to stderr to avoid interfering with stdio transport."""
    print(msg, file=sys.stderr)


# Initialize FastMCP server
mcp = FastMCP("ARTPARK Public Data Server")
mcp.add_middleware(TelemetryMiddleware())


VALID_DATASETS = [
    "0015", "0034", "0041", "0055", "0059", "0086", "0087", "0089",
]

# Human-readable dataset info (built from metadata.yaml scan)
DATASET_INFO = {
    "0015": {
        "name": "Karnataka Dengue Daily Summary (2017-2024)",
        "category": "Epidemiology",
        "description": "Day-wise summaries of tests, suspected cases, confirmed cases and deaths by district in Karnataka.",
        "tags": ["Dengue"],
        "use_for": "Dengue case counts, test positivity, death tracking, district-level outbreak analysis in Karnataka",
    },
    "0034": {
        "name": "Local Government Directory (LGD) Region IDs",
        "category": "Geospatial",
        "description": "Local Government Directory names and codes for all India - states, districts, subdistricts, villages, ULBs.",
        "tags": [],
        "use_for": "Mapping region IDs and names, administrative hierarchy lookups, geocoding",
    },
    "0041": {
        "name": "20th Livestock Census (2019)",
        "category": "Census and Surveys",
        "description": "District, Village and Ward-wise livestock population for Karnataka and Maharashtra, plus all-India district-level data.",
        "tags": ["Livestock"],
        "use_for": "Livestock population by species (cattle, buffalo, sheep, goat, pig, poultry) at district/village level",
    },
    "0055": {
        "name": "FMD - NADCP Vaccination Progress (Rounds 1-6)",
        "category": "Epidemiology",
        "description": "District-level daily vaccination and tagging progress reports for FMD vaccination rounds in Karnataka.",
        "tags": ["Foot and Mouth Disease", "Livestock"],
        "use_for": "FMD vaccination coverage, daily progress tracking, farmer coverage, tagging stats",
    },
    "0059": {
        "name": "FMD - NADCP Vaccination Schedule (Rounds 3-6)",
        "category": "Epidemiology",
        "description": "Village-level scheduled vaccination dates for cattle/buffalo and sheep/goat in Karnataka.",
        "tags": ["Foot and Mouth Disease", "Livestock"],
        "use_for": "Vaccination scheduling, village-level planning, cattle/buffalo/sheep/goat targets",
    },
    "0086": {
        "name": "FMD Nationwide Vaccination Data",
        "category": "Epidemiology",
        "description": "State and district-wise FMD vaccination counts and farmer beneficiary data from NDLM.",
        "tags": ["Foot and Mouth Disease", "Livestock"],
        "use_for": "National FMD vaccination coverage, state-wise comparisons, farmer reach",
    },
    "0087": {
        "name": "FMD Nationwide Seromonitoring Data",
        "category": "Epidemiology",
        "description": "All India state-level seromonitoring summaries showing pre/post vaccination antibody levels for FMD virus types A, O, Asia1.",
        "tags": ["Foot and Mouth Disease"],
        "use_for": "Vaccine efficacy assessment, seroconversion rates, FMD serotype tracking",
    },
    "0089": {
        "name": "FMD Nationwide Serosurveillance Data",
        "category": "Epidemiology",
        "description": "All India state-level serosurveillance summaries for FMD showing cattle/buffalo seroprevalence.",
        "tags": ["Foot and Mouth Disease", "Livestock"],
        "use_for": "FMD seroprevalence, cattle vs buffalo positivity, herd immunity assessment",
    },
}


# =========================================================================
# Tool 1: Discover datasets
# =========================================================================

@mcp.tool(name="1_know_about_artpark_data")
def know_about_artpark_data() -> Dict[str, Any]:
    """
    ============================================================
    RULES (MUST follow exactly):
    - MUST call this first before any other tool.
    - MUST follow this workflow in order:
      1. 1_know_about_artpark_data() -> find dataset (MANDATORY first step)
      2. 2_get_tables(dataset_id) -> list tables in dataset
      3. 3_get_metadata(dataset_id, table_name) -> get column schema + filter values (MANDATORY)
      4. 4_get_data(dataset_id, table_name, filters) -> fetch data (ONLY after step 3)
    - MUST NOT skip step 3. Filter column names come from metadata.
    - MUST NOT ask "Shall I proceed?" if the query is specific enough.
    - ALWAYS attempt to fetch data. NEVER refuse without trying the full workflow.
    ============================================================

    Step 1: Get overview of all 8 ARTPARK public health datasets.

    MUST call this first before any other tool.
    Covers: Dengue epidemiology, Livestock census, FMD vaccination & surveillance, Geospatial admin units.
    Data source: https://github.com/dsih-artpark/publicdata

    When to ask vs fetch:
    - VAGUE query (e.g., "health data") -> ask user to clarify
    - SPECIFIC query (e.g., "dengue cases in Karnataka") -> fetch directly
    """
    return {
        "total_datasets": len(DATASET_INFO),
        "source": "ARTPARK Data Science Innovation Hub (DSIH)",
        "documentation": "https://publicdata.readthedocs.io",
        "catalogue": "https://health.artpark.ai/data",
        "datasets": DATASET_INFO,
        "categories": {
            "Epidemiology": ["0015", "0055", "0059", "0086", "0087", "0089"],
            "Census and Surveys": ["0041"],
            "Geospatial": ["0034"],
        },
        "workflow": [
            "1. 1_know_about_artpark_data() -> find dataset (MANDATORY first step)",
            "2. 2_get_tables(dataset_id) -> list tables",
            "3. 3_get_metadata(dataset_id, table_name) -> get schema + filter values (MANDATORY before step 4)",
            "4. 4_get_data(dataset_id, table_name, filters) -> fetch data (MUST use values from step 3)",
        ],
        "rules": [
            "MUST NOT skip 3_get_metadata() -- column names and filter values differ per table",
            "MUST NOT guess column names or filter values -- use ONLY values from 3_get_metadata()",
            "Comma-separated values work for multiple filter matches (e.g., 'Bengaluru Urban,Mysuru')",
            "ALWAYS attempt the full workflow before saying data is unavailable",
        ],
        "_next_step": "Call 2_get_tables(dataset_id) with the dataset that matches the user's query.",
    }


# =========================================================================
# Tool 2: List tables in a dataset
# =========================================================================

@mcp.tool(name="2_get_tables")
def get_tables(
    dataset_id: str,
    user_query: Optional[str] = None,
) -> Dict[str, Any]:
    """
    ============================================================
    RULES (MUST follow exactly):
    - You MUST call 1_know_about_artpark_data() before this.
    - You MUST call 3_get_metadata() after this. MUST NOT skip to 4_get_data().
    - You MUST pass user_query for context.
    - ALWAYS call this tool. NEVER assume data is unavailable.
    ============================================================

    Step 2: List available tables (CSV files) for a specific dataset.

    Each dataset may have multiple tables. For example, dataset 0041 (Livestock Census)
    has 4 tables: ka-district, ka-village, mh-district, and all-india data.

    After this, pick the matching table and call 3_get_metadata().

    Args:
        dataset_id: Dataset ID - one of: 0015, 0034, 0041, 0055, 0059, 0086, 0087, 0089
        user_query: The user's original question. MUST always include this.
    """
    if dataset_id not in VALID_DATASETS:
        return {
            "error": f"Unknown dataset: {dataset_id}",
            "valid_datasets": VALID_DATASETS,
            "_user_query": user_query,
        }

    result = artpark_data.get_dataset_tables(dataset_id)
    result["_user_query"] = user_query
    result["_next_step"] = (
        "Call 3_get_metadata(dataset_id, table_name) with the table that matches the user's query. "
        "MUST NOT skip to 4_get_data()."
    )
    result["_retry_hint"] = (
        "If none of the tables above match the user's query, you may have picked the WRONG dataset. "
        "Go back to 1_know_about_artpark_data() and try a different dataset."
    )
    return result


# =========================================================================
# Tool 3: Get table metadata (schema + filter values)
# =========================================================================

@mcp.tool(name="3_get_metadata")
def get_metadata(
    dataset_id: str,
    table_name: str,
) -> Dict[str, Any]:
    """
    ============================================================
    RULES (MUST follow exactly):
    - You MUST call this before 4_get_data(). MUST NOT skip this step.
    - You MUST use the column names and filter_values returned here in 4_get_data().
    - MUST NOT guess column names or filter values.
    - If user asked for a breakdown that's not available, tell them what IS available.
    ============================================================

    Step 3: Get the data dictionary (column schema) and available filter values for a table.

    Returns:
    - data_dictionary: Column names with descriptions, comments, access flags
    - csv_summary: Row count, column count, data types
    - filter_values: Unique values for key columns (districts, states, years, etc.)
      Use these in 4_get_data() filters.

    Args:
        dataset_id: Dataset ID (e.g., "0015", "0041")
        table_name: Table name from step 2 (e.g., "ka-dengue-daily-summary", "ka-district-livestock-pop-2019")
    """
    if dataset_id not in VALID_DATASETS:
        return {"error": f"Unknown dataset: {dataset_id}", "valid_datasets": VALID_DATASETS}

    result = artpark_data.get_table_schema(dataset_id, table_name)
    result["_next_step"] = (
        "Call 4_get_data(dataset_id, table_name, filters) using ONLY the column names "
        "and filter_values returned above. MUST NOT guess any values."
    )
    return result


# =========================================================================
# Tool 4: Fetch data
# =========================================================================

@mcp.tool(name="4_get_data")
def get_data(
    dataset_id: str,
    table_name: str,
    filters: Optional[Dict[str, str]] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    """
    ============================================================
    RULES (MUST follow exactly):
    - You MUST have called 3_get_metadata() before this. No exceptions.
    - You MUST use ONLY column names and filter values from 3_get_metadata().
    - MUST NOT guess column names. Column names in ARTPARK data use dot notation
      (e.g., "location.admin2.name", "daily.positive.total") and differ per table.

    Before calling, verify:
    - Did I call 3_get_metadata() for this table? If no -> call it first.
    - Are all filter column names from 3_get_metadata()? If no -> fix them.
    ============================================================

    Step 4: Fetch data from an ARTPARK dataset table.

    Args:
        dataset_id: Dataset ID (e.g., "0015", "0041")
        table_name: Table name (e.g., "ka-dengue-daily-summary")
        filters: Column-value pairs to filter rows. Use values from 3_get_metadata().
                 Comma-separated values filter for multiple matches.
                 Example: {"location.admin2.name": "Bengaluru Urban", "metadata.ISOWeek": "2023-W01"}
        limit: Max rows to return (default 50). Use higher values for complete data.
    """
    if dataset_id not in VALID_DATASETS:
        return {"error": f"Unknown dataset: {dataset_id}", "valid_datasets": VALID_DATASETS}

    result = artpark_data.query_table(dataset_id, table_name, filters=filters, limit=limit)

    # If no data found, hint to retry
    if isinstance(result, dict) and result.get("total_rows_after_filter", 1) == 0:
        result["_hint"] = (
            "No data for this filter combination. Try these fixes: "
            "1) Check spelling of filter values against 3_get_metadata() output. "
            "2) Remove optional filters one at a time. "
            "3) The breakdown you need may already appear in the response without that filter."
        )

    return result


# =========================================================================
# Health check (useful for Docker, load balancers, uptime monitoring)
# =========================================================================

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint for Docker/orchestration health probes."""
    from starlette.responses import JSONResponse
    catalogue = artpark_data.get_catalogue()
    return JSONResponse({
        "status": "healthy",
        "server": "ARTPARK Public Data MCP Server",
        "datasets": len(catalogue),
        "tools": 4,
    })


# =========================================================================
# Entrypoint
# =========================================================================

if __name__ == "__main__":
    # Verify datasets on startup
    catalogue = artpark_data.get_catalogue()
    n_datasets = len(catalogue)
    n_tables = sum(len(info["tables"]) for info in catalogue.values())

    log("\n" + "=" * 70)
    log("ARTPARK Public Data MCP Server")
    log("=" * 70)
    log(f"Datasets:   {n_datasets} ({n_tables} tables)")
    log(f"Tools:      4 (1_know → 2_tables → 3_metadata → 4_data)")
    log(f"Framework:  FastMCP 3.0 + OpenTelemetry")
    log(f"Data:       https://github.com/dsih-artpark/publicdata")
    log("-" * 70)
    log(f"MCP:        http://localhost:8000/mcp")
    log(f"Health:     http://localhost:8000/health")
    log("=" * 70 + "\n")

    mcp.run(transport="http", port=8000)
