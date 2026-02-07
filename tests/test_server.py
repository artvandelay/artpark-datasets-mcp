"""
Tests for artpark_server.py -- the MCP tool layer.
Tests the tool functions directly (no HTTP, no MCP protocol overhead).
"""

import pytest
import asyncio
import artpark_server


# =========================================================================
# Tool 1: Know about data
# =========================================================================

class TestKnowAboutData:
    def test_returns_8_datasets(self):
        result = artpark_server.know_about_artpark_data()
        assert result["total_datasets"] == 8

    def test_returns_all_dataset_ids(self):
        result = artpark_server.know_about_artpark_data()
        for did in ["0015", "0034", "0041", "0055", "0059", "0086", "0087", "0089"]:
            assert did in result["datasets"]

    def test_returns_workflow_guidance(self):
        result = artpark_server.know_about_artpark_data()
        assert "workflow" in result
        assert "_next_step" in result

    def test_dataset_info_has_required_fields(self):
        result = artpark_server.know_about_artpark_data()
        for did, info in result["datasets"].items():
            assert "name" in info, f"Dataset {did} missing 'name'"
            assert "category" in info, f"Dataset {did} missing 'category'"
            assert "use_for" in info, f"Dataset {did} missing 'use_for'"


# =========================================================================
# Tool 2: Get tables
# =========================================================================

class TestGetTables:
    def test_valid_dataset(self):
        result = artpark_server.get_tables("0087", user_query="FMD data")
        assert "tables" in result
        assert result["dataset_id"] == "0087"
        assert "_next_step" in result

    def test_invalid_dataset(self):
        result = artpark_server.get_tables("9999", user_query="test")
        assert "error" in result
        assert "valid_datasets" in result

    def test_user_query_is_echoed(self):
        result = artpark_server.get_tables("0087", user_query="my question")
        assert result["_user_query"] == "my question"


# =========================================================================
# Tool 3: Get metadata
# =========================================================================

class TestGetMetadata:
    def test_returns_schema(self):
        result = artpark_server.get_metadata("0087", "seromonitoring")
        assert "csv_summary" in result
        assert "filter_values" in result
        assert "_next_step" in result

    def test_invalid_dataset(self):
        result = artpark_server.get_metadata("9999", "anything")
        assert "error" in result


# =========================================================================
# Tool 4: Get data
# =========================================================================

class TestGetData:
    def test_basic_query(self):
        result = artpark_server.get_data("0087", "seromonitoring", limit=5)
        assert result["rows_returned"] == 5
        assert result["total_rows_before_filter"] == 238
        assert "data" in result

    def test_with_filter(self):
        result = artpark_server.get_data(
            "0087", "seromonitoring",
            filters={"state.name": "KARNATAKA"},
            limit=50,
        )
        assert result["total_rows_after_filter"] == 16
        for row in result["data"]:
            assert row["state.name"].upper() == "KARNATAKA"

    def test_empty_filter_result_has_hint(self):
        result = artpark_server.get_data(
            "0087", "seromonitoring",
            filters={"state.name": "NONEXISTENT_STATE"},
            limit=5,
        )
        assert result["total_rows_after_filter"] == 0
        assert "_hint" in result

    def test_invalid_dataset(self):
        result = artpark_server.get_data("9999", "anything")
        assert "error" in result
