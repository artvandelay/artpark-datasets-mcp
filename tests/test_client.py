"""
Tests for artpark/client.py -- the local data reader.
Runs against the real publicdata/ CSV files in the repo.
"""

import pytest
from artpark.client import ARTPARKData


@pytest.fixture
def client():
    """Fresh client instance."""
    return ARTPARKData()


# =========================================================================
# Catalogue / Discovery
# =========================================================================

class TestCatalogue:
    def test_catalogue_finds_all_8_datasets(self, client):
        cat = client.get_catalogue()
        assert len(cat) == 8
        for did in ["0015", "0034", "0041", "0055", "0059", "0086", "0087", "0089"]:
            assert did in cat, f"Dataset {did} missing from catalogue"

    def test_catalogue_has_tables_for_each_dataset(self, client):
        cat = client.get_catalogue()
        for did, info in cat.items():
            assert len(info["tables"]) >= 1, f"Dataset {did} has 0 tables"
            assert len(info["csv_files"]) >= 1, f"Dataset {did} has 0 CSV files"

    def test_list_datasets_returns_summary(self, client):
        result = client.list_datasets()
        assert result["total_datasets"] == 8
        assert "0087" in result["datasets"]


# =========================================================================
# Dataset Tables
# =========================================================================

class TestGetDatasetTables:
    def test_0087_has_seromonitoring_table(self, client):
        result = client.get_dataset_tables("0087")
        names = [t["name"] for t in result["tables"]]
        assert "seromonitoring" in names

    def test_0041_has_4_tables(self, client):
        result = client.get_dataset_tables("0041")
        assert len(result["tables"]) == 4
        names = [t["name"] for t in result["tables"]]
        assert "ka-district-livestock-pop-2019" in names

    def test_0015_fallback_from_broken_yaml(self, client):
        """0015's metadata.yaml has a parse error. Client should fall back to CSV inference."""
        result = client.get_dataset_tables("0015")
        assert len(result["tables"]) >= 1
        names = [t["name"] for t in result["tables"]]
        assert "ka-dengue-daily-summary" in names
        # Should have inferred columns from CSV header
        table = result["tables"][0]
        assert table["num_columns"] >= 20

    def test_0055_has_csv_files(self, client):
        result = client.get_dataset_tables("0055")
        assert len(result["csv_files"]) == 6
        assert "round1.csv" in result["csv_files"]

    def test_nonexistent_dataset_returns_error(self, client):
        result = client.get_dataset_tables("9999")
        assert "error" in result


# =========================================================================
# Table Metadata (Schema + Filter Values)
# =========================================================================

class TestGetTableSchema:
    def test_seromonitoring_schema(self, client):
        result = client.get_table_schema("0087", "seromonitoring")
        assert "csv_summary" in result
        assert result["csv_summary"]["total_rows"] == 238
        assert result["csv_summary"]["total_columns"] == 14

    def test_seromonitoring_has_filter_values(self, client):
        result = client.get_table_schema("0087", "seromonitoring")
        fv = result["filter_values"]
        assert "state.name" in fv
        assert len(fv["state.name"]) >= 30  # 35 states

    def test_livestock_schema(self, client):
        result = client.get_table_schema("0041", "ka-district-livestock-pop-2019")
        assert result["csv_summary"]["total_rows"] == 30

    def test_dengue_schema_without_metadata_yaml(self, client):
        """0015 has broken YAML, but schema should still work from CSV."""
        result = client.get_table_schema("0015", "ka-dengue-daily-summary")
        assert "csv_summary" in result
        assert result["csv_summary"]["total_rows"] > 70000

    def test_nonexistent_table_returns_empty_schema(self, client):
        result = client.get_table_schema("0087", "nonexistent")
        # Should not crash; csv_summary should be empty
        assert result.get("csv_summary") == {} or "error" in result.get("csv_summary", {})


# =========================================================================
# Data Query
# =========================================================================

class TestQueryTable:
    def test_query_seromonitoring_all(self, client):
        result = client.query_table("0087", "seromonitoring", limit=300)
        assert result["total_rows_before_filter"] == 238
        assert result["total_rows_after_filter"] == 238
        assert result["rows_returned"] == 238

    def test_query_with_filter(self, client):
        result = client.query_table(
            "0087", "seromonitoring",
            filters={"state.name": "KARNATAKA"},
            limit=50,
        )
        assert result["total_rows_after_filter"] == 16
        assert result["rows_returned"] == 16

    def test_filter_is_case_insensitive(self, client):
        result = client.query_table(
            "0087", "seromonitoring",
            filters={"state.name": "karnataka"},  # lowercase
            limit=5,
        )
        assert result["total_rows_after_filter"] == 16

    def test_filter_comma_separated(self, client):
        result = client.query_table(
            "0087", "seromonitoring",
            filters={"state.name": "KARNATAKA,TAMIL NADU"},
            limit=50,
        )
        assert result["total_rows_after_filter"] > 16  # Karnataka has 16, TN adds more

    def test_filter_invalid_column_returns_error(self, client):
        result = client.query_table(
            "0087", "seromonitoring",
            filters={"nonexistent_column": "value"},
        )
        assert "error" in result
        assert "valid_columns" in result

    def test_query_respects_limit(self, client):
        result = client.query_table("0087", "seromonitoring", limit=5)
        assert result["rows_returned"] == 5
        assert result["total_rows_after_filter"] == 238

    def test_query_returns_summary_stats(self, client):
        result = client.query_table("0087", "seromonitoring", limit=5)
        assert "summary_stats" in result
        assert len(result["summary_stats"]) > 0

    def test_query_nonexistent_csv_returns_error(self, client):
        result = client.query_table("0087", "nonexistent_table")
        assert "error" in result

    def test_query_dengue_data(self, client):
        """Verify 0015 data is queryable even with broken metadata.yaml."""
        result = client.query_table(
            "0015", "ka-dengue-daily-summary",
            filters={"location.admin2.name": "Mysuru"},
            limit=5,
        )
        assert result["total_rows_after_filter"] > 0
        assert result["rows_returned"] <= 5


# =========================================================================
# CSV Path Resolution
# =========================================================================

class TestResolveCsvPath:
    def test_direct_match(self, client):
        path = client._resolve_csv_path("0087", "seromonitoring")
        assert path is not None
        assert path.endswith("seromonitoring.csv")

    def test_hyphen_underscore_normalization(self, client):
        path = client._resolve_csv_path("0015", "ka-dengue-daily-summary")
        assert path is not None

    def test_round_files(self, client):
        for i in range(1, 7):
            path = client._resolve_csv_path("0055", f"round{i}")
            assert path is not None, f"round{i} not found"

    def test_nonexistent_returns_none(self, client):
        path = client._resolve_csv_path("0087", "does_not_exist")
        assert path is None

    def test_nonexistent_dataset_returns_none(self, client):
        path = client._resolve_csv_path("9999", "anything")
        assert path is None
